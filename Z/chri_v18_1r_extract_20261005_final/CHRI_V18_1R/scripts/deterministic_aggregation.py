"""Minimal V18.1R-only deterministic replacements for grouped CUDA reductions."""
import torch

def endpoint(net,pairs,side):
    raw,group,counts=net.structure.tokens(pairs,side)
    latent=net.encoder(raw)
    sums=torch.segment_reduce(latent,'sum',lengths=counts)
    mean=sums/counts.clamp_min(1).to(latent.dtype)[:,None]
    maximum=torch.segment_reduce(latent,'max',lengths=counts)
    maximum=torch.where(counts[:,None]>0,maximum,torch.zeros_like(maximum))
    return latent,counts,torch.cat((mean,maximum),1)

def representation(net,pairs,b,need_relation=True,max_interactions=131072):
    eu,cu,pu=net.endpoint(pairs,0);ev,cv,pv=net.endpoint(pairs,1)
    z=torch.cat(((b-net.b_mean)/net.b_std,pu,pv),1)
    if not need_relation:return z,None
    sizes=cu*cv;count=int(sizes.sum().item())
    if not count:return z,torch.zeros((len(pairs),32),device=pairs.device,dtype=b.dtype)
    pair_offset=sizes.cumsum(0)-sizes
    local=torch.arange(count,device=pairs.device)-pair_offset[torch.repeat_interleave(torch.arange(len(pairs),device=pairs.device),sizes)]
    groups=torch.repeat_interleave(torch.arange(len(pairs),device=pairs.device),sizes)
    ou=cu.cumsum(0)-cu;ov=cv.cumsum(0)-cv
    iu=ou[groups]+torch.div(local,cv[groups],rounding_mode='floor')
    iv=ov[groups]+local%cv[groups]
    sum_chunks=[];max_chunks=[];start_row=0;running=0
    for row in range(len(pairs)):
        n=int(sizes[row].item())
        if row>start_row and running+n>max_interactions:
            start_pos=int(pair_offset[start_row].item());stop_pos=int(pair_offset[row].item())
            left,right,g=eu[iu[start_pos:stop_pos]],ev[iv[start_pos:stop_pos]],groups[start_pos:stop_pos]
            m=net.relation(torch.cat((left+right,(left-right).abs(),left*right),1))
            lengths=sizes[start_row:row]
            sum_chunks.append(torch.segment_reduce(m,'sum',lengths=lengths))
            max_chunks.append(torch.segment_reduce(m,'max',lengths=lengths))
            start_row=row;running=0
        running+=n
    if start_row<len(pairs):
        start_pos=int(pair_offset[start_row].item());stop_pos=count
        left,right,g=eu[iu[start_pos:stop_pos]],ev[iv[start_pos:stop_pos]],groups[start_pos:stop_pos]
        m=net.relation(torch.cat((left+right,(left-right).abs(),left*right),1))
        lengths=sizes[start_row:]
        sum_chunks.append(torch.segment_reduce(m,'sum',lengths=lengths))
        max_chunks.append(torch.segment_reduce(m,'max',lengths=lengths))
    sums=torch.cat(sum_chunks,0);maximum=torch.cat(max_chunks,0)
    maximum=torch.where(sizes[:,None]>0,maximum,torch.zeros_like(maximum))
    mean=sums/sizes.clamp_min(1).to(sums.dtype)[:,None]
    return z,torch.cat((mean,maximum),1)

def install(net):
    net.endpoint=lambda pairs,side:endpoint(net,pairs,side)
    net.representation=lambda pairs,b,need_relation=True:representation(net,pairs,b,need_relation)
    return net
