"""Verify the stabilization contracts without modifying any historical artifact."""
import json
import tempfile
from pathlib import Path

import numpy as np
import torch
from stability181 import StablePredictor,v,OUT
from chri_features import build_structure,Structure


def main():
    device='cuda'
    with tempfile.TemporaryDirectory(prefix='chri181_contracts_') as folder:
        graph=np.array([[0,1],[1,2],[2,3],[2,4],[3,4],[4,5],[6,7]],np.int64)
        x=np.random.RandomState(1).normal(size=(8,12)).astype(np.float32)
        path=Path(folder)/'structure.npz';build_structure(x,graph,path)
        structure=Structure(path,device)
        pairs=torch.tensor([[0,1],[0,3],[1,4],[2,4],[6,7]],device=device)
        donors=pairs.flip(0);b=torch.randn(len(pairs),257,device=device)
        nets={name:StablePredictor(structure,0,name,np.zeros(257),np.ones(257)).to(device)
              for name in ('V1','V2','V3','V3_NULL','V3_SHUFFLE')}
        counts={name:sum(p.numel() for p in net.parameters() if p.requires_grad) for name,net in nets.items()}
        assert counts['V3']==counts['V3_NULL']==counts['V3_SHUFFLE']
        reference_decoder=[p.detach().clone() for p in nets['V1'].decoder.parameters()]
        for name,net in nets.items():
            net.eval();part=net.components(pairs,b,donors)
            assert torch.equal(part['score'],b[:,0]),'INITIAL_BASELINE_CHANGED '+name
            assert not torch.count_nonzero(part['correction'])
            if name.startswith('V3'):
                assert torch.allclose(part['gate'],torch.full_like(part['gate'],1/(1+np.exp(2))),atol=1e-7)
            assert all(torch.equal(a,z) for a,z in zip(net.decoder.parameters(),reference_decoder))
            net.train();net.zero_grad(set_to_none=True)
            part=net.components(pairs,b,donors);part['nuisance_loss'].backward()
            assert any(p.grad is not None and torch.count_nonzero(p.grad) for p in net.nuisance.parameters())
            assert all(p.grad is None for module in (net.encoder,net.relation,net.decoder,net.correction) for p in module.parameters()),'NUISANCE_GRADIENT_ENTERS_SUPERVISED_ENCODER'
            net.zero_grad(set_to_none=True)
            if net.variant=='V1':torch.nn.init.normal_(net.decoder[-1].weight,std=.01)
            else:torch.nn.init.normal_(net.correction[-1].weight,std=.01)
            score,nuisance,conditional_null=net(pairs,b,donors)
            assert float(conditional_null)==0,'FORBIDDEN_CONDITIONAL_NULL_REGULARIZATION'
            loss=torch.nn.functional.binary_cross_entropy_with_logits(score,torch.tensor([1.,0.,0.,1.,1.],device=device))
            loss.backward()
            assert all(p.grad is None for p in net.nuisance.parameters()),'PREDICTION_LABEL_GRADIENT_ENTERS_NUISANCE'
            assert torch.isfinite(loss)
            assert all(torch.isfinite(p.grad).all() for p in net.parameters() if p.grad is not None)
        try:v.sealed_input('cora',True)
        except AssertionError:pass
        else:raise AssertionError('TEST_ACCESS_NOT_BLOCKED')
        result={'state':'PASS','device':'cuda','parameter_counts':counts,
                'checks':['exact initial baseline equality','zero correction head','conservative gate init',
                          'paired decoder init','V3 NULL/SHUFFLE parameter equality','nuisance gradient isolation',
                          'no label gradient into nuisance','finite prediction gradients','no conditional-null regularizer','test permanently sealed'],
                'test_opened':False}
        (OUT/'VALIDATION_CHECKS.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result,indent=2))


if __name__=='__main__':main()
