"""Train-visible, target-masked raw-star descriptors. No labels or test IO."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch_scatter import scatter_mean, scatter_max


def array_hash(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(str(a.shape).encode()); h.update(str(a.dtype).encode()); h.update(a.tobytes())
    return h.hexdigest()


def build_structure(x, train, destination):
    n = len(x)
    train = np.sort(np.asarray(train, np.int64), axis=1)
    adj = [set() for _ in range(n)]
    for u, v in train:
        assert u != v
        adj[u].add(int(v)); adj[v].add(int(u))
    degree = np.array([len(a) for a in adj], np.int64)
    rng = np.random.RandomState(18018)
    projection = rng.normal(size=(x.shape[1], 16)).astype(np.float32) / np.sqrt(x.shape[1])
    projected = np.asarray(x @ projection, np.float32)
    active = degree > 0
    mean = projected[active].mean(0); std = projected[active].std(0).clip(1e-6)
    node = (projected - mean) / std
    members = [np.array(sorted({i, *adj[i]}), np.int64) if adj[i] else np.empty(0, np.int64) for i in range(n)]

    def descriptor(mem):
        if not len(mem):
            return np.zeros(33, np.float32)
        return np.r_[node[mem].mean(0), node[mem].max(0), np.log1p(len(mem))].astype(np.float32)

    raw = np.stack([descriptor(m) for m in members])
    width = int(degree.max()) + 1
    incident = np.full((n, width), -1, np.int64)
    for i in range(n):
        if adj[i]:
            centers = sorted({i, *adj[i]})
            incident[i, :len(centers)] = centers
    keys = train[:, 0] * n + train[:, 1]
    order = np.argsort(keys); train = train[order]; keys = keys[order]
    masked = np.zeros((len(train), 2, 33), np.float32)
    for row, (u, v) in enumerate(train):
        for side, (center, removed) in enumerate(((u, v), (v, u))):
            remaining = members[center][members[center] != removed]
            masked[row, side] = descriptor(remaining) if len(remaining) > 1 else 0

    # Independent reconstruction oracle, including degree-one hyperedge disappearance.
    sample = np.random.RandomState(18019).choice(len(train), min(256, len(train)), replace=False)
    for row in sample:
        u, v = map(int, train[row]); reduced = list(adj)
        reduced[u] = adj[u] - {v}; reduced[v] = adj[v] - {u}
        for side, endpoint in enumerate((u, v)):
            oracle_inc = {endpoint, *reduced[endpoint]} if reduced[endpoint] else set()
            cached_inc = set(incident[endpoint][incident[endpoint] >= 0]) - {v if side == 0 else u}
            if degree[endpoint] == 1:
                cached_inc.discard(endpoint)
            assert cached_inc == oracle_inc
            mem = np.array(sorted({endpoint, *reduced[endpoint]}), np.int64) if reduced[endpoint] else np.empty(0, np.int64)
            assert np.allclose(masked[row, side], descriptor(mem), atol=1e-6)
        assert v not in ({u, *reduced[u]}) and u not in ({v, *reduced[v]})
    destination = Path(destination); destination.parent.mkdir(parents=True, exist_ok=True)
    np.savez(destination, raw=raw, incident=incident, degree=degree, keys=keys, masked=masked,
             projection=projection, normalization_mean=mean, normalization_std=std)
    return dict(nodes=n, active_hyperedges=int(active.sum()), max_incident=width,
                train_pairs=len(train), target_mask_oracle_samples=len(sample), target_mask_oracle='PASS',
                descriptor='mean/max of fixed 16d projected node attributes + log1p(size)',
                descriptor_normalization='training-incident nodes only; no labels',
                train_pair_hash=array_hash(train), projected_node_hash=array_hash(node))


class Structure:
    def __init__(self, path, device='cuda'):
        with np.load(path) as z:
            self.raw = torch.tensor(z['raw'], device=device)
            self.incident = torch.tensor(z['incident'], device=device)
            self.degree = torch.tensor(z['degree'], device=device)
            self.keys = torch.tensor(z['keys'], device=device)
            self.masked = torch.tensor(z['masked'], device=device)
        self.n = len(self.degree)

    def tokens(self, pairs, side):
        pairs = pairs.sort(dim=1).values
        node, other = pairs[:, side], pairs[:, 1-side]
        key = pairs[:, 0]*self.n + pairs[:, 1]
        row = torch.searchsorted(self.keys, key).clamp(max=len(self.keys)-1)
        target = self.keys[row] == key
        centers = self.incident[node]
        valid = centers >= 0
        valid &= ~((centers == other[:, None]) & target[:, None])
        valid &= ~((centers == node[:, None]) & target[:, None] & (self.degree[node, None] == 1))
        group, col = valid.nonzero(as_tuple=True)
        edge = centers[group, col]
        raw = self.raw[edge].clone()
        modify = target[group] & (edge == node[group])
        raw[modify] = self.masked[row[group[modify]], side]
        counts = torch.bincount(group, minlength=len(pairs))
        return raw, group, counts


class RelationPredictor(nn.Module):
    """Nested predictors with exactly matched downstream decoder width.

    Shared latent encoder never sees B/C. R consumes only endpoint set latents.
    """
    def __init__(self, structure, seed, arm, b_mean, b_std, fixed=None, i1=None):
        super().__init__()
        self.structure = structure; self.arm = arm; self.i1 = i1
        self.register_buffer('b_mean', torch.tensor(b_mean, dtype=torch.float32))
        self.register_buffer('b_std', torch.tensor(b_std, dtype=torch.float32))
        # Each component has its own initialization stream: arms do not move decoder RNG.
        with torch.random.fork_rng():
            torch.manual_seed(18000 + seed)
            self.encoder = nn.Sequential(nn.Linear(33, 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU())
        with torch.random.fork_rng():
            torch.manual_seed(18100 + seed)
            self.relation = nn.Sequential(nn.Linear(48, 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU())
        with torch.random.fork_rng():
            torch.manual_seed(18200 + seed)
            self.decoder = nn.Sequential(nn.Linear(353, 64), nn.ReLU(), nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1))
            nn.init.zeros_(self.decoder[-1].weight); nn.init.zeros_(self.decoder[-1].bias)
            self.z_decoder = nn.Sequential(nn.Linear(321, 64), nn.ReLU(), nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1))
            nn.init.zeros_(self.z_decoder[-1].weight); nn.init.zeros_(self.z_decoder[-1].bias)
        with torch.random.fork_rng():
            torch.manual_seed(18300 + seed)
            self.nuisance = nn.Sequential(nn.Linear(321, 32), nn.ReLU(), nn.Linear(32, 32))
            self.correction = nn.Sequential(nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 1))
            nn.init.zeros_(self.correction[-1].weight); nn.init.zeros_(self.correction[-1].bias)
        if fixed is not None:
            self.encoder.load_state_dict(fixed['encoder']); self.relation.load_state_dict(fixed['relation'])
            self.encoder.requires_grad_(False); self.relation.requires_grad_(False)
        if arm == 'A1':
            self.relation.requires_grad_(False)
        # Unused downstream heads are removed from the optimizer and parameter count.
        self.is_module = arm.startswith('M') or arm.startswith('O')
        if self.is_module:
            self.decoder.requires_grad_(False)
        else:
            self.z_decoder.requires_grad_(False); self.nuisance.requires_grad_(False); self.correction.requires_grad_(False)
        if arm in ('M0', 'O0', 'O1'):
            self.nuisance.requires_grad_(False); self.correction.requires_grad_(False)
        if i1 is not None:
            i1.requires_grad_(False)

    def endpoint(self, pairs, side):
        raw, group, counts = self.structure.tokens(pairs, side)
        latent = self.encoder(raw)
        mean = scatter_mean(latent, group, dim=0, dim_size=len(pairs))
        maximum = scatter_max(latent, group, dim=0, dim_size=len(pairs))[0]
        maximum[counts == 0] = 0
        return latent, counts, torch.cat((mean, maximum), 1)

    def representation(self, pairs, b, need_relation=True):
        eu, cu, pu = self.endpoint(pairs, 0); ev, cv, pv = self.endpoint(pairs, 1)
        z = torch.cat(((b-self.b_mean)/self.b_std, pu, pv), 1)
        if not need_relation:
            return z, None
        sizes = cu*cv
        groups = torch.repeat_interleave(torch.arange(len(pairs), device=pairs.device), sizes)
        count = len(groups)
        if not count:
            return z, torch.zeros((len(pairs), 32), device=pairs.device)
        pair_offset = sizes.cumsum(0)-sizes
        local = torch.arange(count, device=pairs.device)-pair_offset[groups]
        ou = cu.cumsum(0)-cu; ov = cv.cumsum(0)-cv
        iu = ou[groups] + torch.div(local, cv[groups], rounding_mode='floor')
        iv = ov[groups] + local % cv[groups]
        # Chunk the operator along interaction records; no truncation/subsampling.
        sums = torch.zeros((len(pairs),16),device=pairs.device)
        maximum = torch.zeros_like(sums)
        for start in range(0, count, 131072):
            stop = start+131072
            left, right, g = eu[iu[start:stop]], ev[iv[start:stop]], groups[start:stop]
            m = self.relation(torch.cat((left+right, (left-right).abs(), left*right),1))
            part = torch.zeros_like(sums).index_add(0,g,m)
            mx = scatter_max(m,g,dim=0,dim_size=len(pairs))[0]
            sums = sums+part; maximum = torch.maximum(maximum,mx)
        return z, torch.cat((sums/sizes.clamp_min(1)[:,None],maximum),1)

    def prediction(self, z, r, baseline):
        if not self.is_module:
            return baseline+self.decoder(torch.cat((z,r),1)).flatten()
        result = baseline+self.z_decoder(z).flatten()
        if self.arm not in ('M0','O0','O1'):
            residual = r-self.nuisance(z).detach() if self.arm in ('M2','M3','O3_CRIB','O2_CRIB') else r
            result = result+self.correction(residual).flatten()
        return result

    def forward(self, pairs, b, donor=None):
        need = self.arm not in ('A1','A4','M0','O0','O1')
        z, r = self.representation(pairs,b,need)
        nuisance_loss = null_loss = b.new_zeros(())
        if self.arm in ('A1','M0','O0','O1'):
            r = b.new_zeros((len(pairs),32))
        elif self.arm == 'A4':
            # Parameter-matched branch sees null compatibility inputs, with trainable biases.
            m = self.relation(b.new_zeros((len(pairs),48)))
            r = torch.cat((m,m),1)
        elif self.arm in ('A3','M4'):
            _, r = self.representation(donor,b,True)
        if self.is_module and self.arm not in ('M0','O0','O1'):
            prediction = self.nuisance(z)
            nuisance_loss = (prediction-r.detach()).square().mean()
            if self.arm in ('M3','O3_CRIB','O2_CRIB') and self.training:
                _, null_r = self.representation(donor,b,True)
                null_loss = self.correction(null_r-prediction.detach()).square().mean()
        score = self.prediction(z,r,b[:,0])
        if self.i1 is not None:
            score = score+self.i1(pairs)
        return score,nuisance_loss,null_loss


def heuristic_rows(train, n, pairs):
    """Label-free, target-masked degree/overlap/motif diagnostics."""
    adj=[set() for _ in range(n)]
    for u,v in train:
        adj[u].add(int(v));adj[v].add(int(u))
    deg=np.array([len(a) for a in adj])
    output=[]
    for u,v in pairs:
        u,v=int(u),int(v); target=v in adj[u]
        nu=adj[u]-{v};nv=adj[v]-{u};shared=nu&nv
        du,dv=len(nu),len(nv)
        eu={u,*nu} if nu else set();ev={v,*nv} if nv else set()
        se=np.array([deg[c]+1-int(target and c in (u,v)) for c in eu],float)
        sf=np.array([deg[c]+1-int(target and c in (u,v)) for c in ev],float)
        output.append([du,dv,len(eu),len(ev),len(eu&ev),
                       se.mean() if len(se) else 0,se.std() if len(se) else 0,
                       sf.mean() if len(sf) else 0,sf.std() if len(sf) else 0,
                       len(shared),sum(1/np.log(max(deg[w],2)) for w in shared),
                       sum(1/max(deg[w],1) for w in shared),
                       sum(len(adj[a]&nv) for a in nu)])
    return np.log1p(np.array(output,np.float32))
