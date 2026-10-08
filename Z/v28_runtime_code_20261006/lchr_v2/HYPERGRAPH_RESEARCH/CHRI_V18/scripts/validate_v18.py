"""Prelaunch checks for masking, invariance, separation, paired controls, and gradients."""
import json
import tempfile
from pathlib import Path

import numpy as np
import torch

from chri_features import Structure, RelationPredictor, build_structure


def main():
    device='cuda' if torch.cuda.is_available() else 'cpu'
    with tempfile.TemporaryDirectory(prefix='chri_mask_check_') as folder:
        graph=np.array([[0,1],[1,2],[2,3],[2,4],[3,4],[4,5],[6,7]],np.int64)
        x=np.random.RandomState(1).normal(size=(8,12)).astype(np.float32)
        path=Path(folder)/'structure.npz'
        meta=build_structure(x,graph,path)
        structure=Structure(path,device)
        pairs=torch.tensor([[0,1],[0,3],[1,4],[2,4],[6,7]],device=device)
        # The last pair consists of two degree-one nodes: both masked incident sets vanish.
        for side in (0,1):
            raw,group,count=structure.tokens(pairs,side)
            assert int(count[-1])==0
            assert torch.isfinite(raw).all()
        baseline=torch.randn(len(pairs),257,device=device)
        donor=pairs.flip(0)
        nets={a:RelationPredictor(structure,0,a,np.zeros(257),np.ones(257)).to(device) for a in ('A1','A2','A3','A4')}
        for arm,net in nets.items():
            net.eval();score,_,_=net(pairs,baseline,donor)
            assert torch.equal(score,baseline[:,0]),f'ZERO_INITIALIZATION_FAILED {arm}'
            assert all(torch.equal(a,b) for a,b in zip(net.decoder.parameters(),nets['A1'].decoder.parameters()))
        net=nets['A2']
        z,r=net.representation(pairs,baseline,True)
        _,r_changed=net.representation(pairs,baseline+100,True)
        relation_repeat_error=float((r-r_changed).abs().max())
        # CUDA scatter sums may change their floating-point addition order.
        assert torch.allclose(r,r_changed,atol=2e-6,rtol=2e-6),'BACKBONE_ENTERS_RELATION_ENCODER'
        original=structure.incident.clone()
        structure.incident=structure.incident.flip(1)
        z2,r2=net.representation(pairs,baseline,True)
        assert torch.allclose(z,z2,atol=2e-6,rtol=2e-6)
        assert torch.allclose(r,r2,atol=2e-6,rtol=2e-6)
        structure.incident=original
        # Same endpoint with two absent targets must have identical independent P.
        absent=torch.tensor([[0,3],[0,4]],device=device)
        pu=net.endpoint(absent,0)[2]
        assert torch.equal(pu[0],pu[1]),'INDEPENDENT_ENDPOINT_ENCODER_USES_OTHER_ENDPOINT'
        for arm,model in nets.items():
            # Open the final head in this scratch model to exercise latent gradients.
            torch.nn.init.normal_(model.decoder[-1].weight,std=.01)
            model.train();score,_,_=model(pairs,baseline,donor)
            loss=torch.nn.functional.binary_cross_entropy_with_logits(score,torch.tensor([1.,0.,0.,1.,1.],device=device))
            loss.backward()
            assert torch.isfinite(loss)
            assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
        result={'state':'PASS','device':device,'checks':['raw-star removal oracle','degree-one disappearance',
            'independent endpoint P','B excluded from R','token-order invariance','zero initialization',
            'paired decoder initialization','finite backward gradients for true/shuffle/null/Z'],
            'target_mask_oracle':meta['target_mask_oracle'],
            'relation_repeat_max_abs_error':relation_repeat_error,'test_accessed':False}
        print(json.dumps(result,indent=2))


if __name__=='__main__':main()
