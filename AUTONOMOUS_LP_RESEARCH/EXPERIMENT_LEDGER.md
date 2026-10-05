# Experiment Ledger

No new autonomous-loop experiment has been accepted yet.

## Imported evidence

- DCDLP Degree/CN Disentanglement — STOP; see `BLACKLIST.md`.
- MPLP-VC — STOP; true variance/confidence was not better than shuffled on the decisive audit and did not yield stable prediction gain.
- NCN-CNDP — STOP; 24 runs, only 3/6 seed wins.
- HL-GNN-PDG — STOP; gate collapse and +37.6% GPU memory.
- CECG — STOP; controlled P4 < P3 on five Cora HeaRT seeds.
- R1-07 Neighbor-Role Transition Matrix — Stage0/Stage1 positive but Stage2 STOP; TrueRole mean AUC 0.59832 versus Parent 0.67529 and no True > Shuffled ranking gain.
- R2-01 Block-Cut Route Profile — Stage0/Stage1 positive but Stage2 STOP; TrueRoute mean AUC 0.58291 versus Parent 0.57989, but Proxy 0.67453 and ranking metrics declined.
- R3-01 Non-Backtracking Continuation Profile — Stage0 support passed and Stage1 showed a small balanced AUC increment, but Stage2 STOP; TrueNB mean AUC 0.64378 versus Parent 0.65716, ShuffledNB 0.64527, and Proxy 0.69053, with lower AP/MRR/Hits@10/Hits@50 than Parent.
- R4-01 Boundary Matching/Cover Profile — Stage0 passed; Stage1 STOP before GPU integration because TrueMatch AUC 0.47080 exceeded DangerousControls 0.45285 and ShuffledMatch 0.46111 while AP 0.49119 was below both controls.
- R4-03 Boundary Expansion Deficit — Stage0/Stage1 passed and Stage2 ran; STOP because TrueExpand aggregate AUC 0.69625 exceeded Parent 0.64783, but MRR/Hits@10 declined versus Parent and TrueExpand lost Proxy on MRR/Hits@10/50/100.
- R4-07 Neighbor Signature Alignment Profile — Stage0 passed; Stage1 STOP because TrueAlign lost DangerousControls, ShuffledAlign, and Proxy on both AUC and AP.
- R4-08 Fixed Laplacian Spectral Band Profile — Stage0 passed; Stage1 STOP because TrueSpectral AUC 0.45710 was below Proxy 0.45983, even though AP was slightly higher.
- R1-03 Internally Vertex-Disjoint Short-Path Profile — Stage0/Stage1 passed and Stage2 ran; STOP because TrueDisjoint AUC 0.60764 lost Parent 0.61262 and Proxy 0.66675, while AP lost ShuffledDisjoint.
- R4-12 Exclusive-Neighborhood Cohesion Profile — Stage0/Stage1 passed and Stage2 ran; STOP because TrueCohesion lost Proxy on all aggregate ranking metrics despite a large Parent gain.
- R4-13 Multi-Scale Community Boundary Profile — Stage0/Stage1 passed and Stage2 ran; STOP because TrueCommunity lost Parent on all aggregate ranking metrics and lost Proxy on AUC/AP/MRR/Hits@10.

## Protocol lock for new attempts

- Use the parent’s official data split and evaluation protocol.
- Select ideas using train/validation structural probes only; do not use test labels to tune the idea.
- Compare Base, Base + TrueCandidate, Base + ShuffledCandidate, and Base + SimpleProxy where applicable.
- Keep the same random seed, negative candidates, ordering, optimizer, learning rate, dropout, epochs, early stopping, backbone, hidden size, and evaluation protocol across variants.
- Record raw per-seed results, runtime, memory, and extraction cost.
