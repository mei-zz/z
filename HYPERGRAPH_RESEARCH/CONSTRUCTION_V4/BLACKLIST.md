# V4 blacklist and scope guard

## Rejected historical directions (do not reactivate in this sprint)

PCHR, LCHR, SSHC, RAHC, HSA, ARHC, PMHE, and ARPM are already rejected. The V3 operator experiments found no structural signal. They remain closed for this construction-only sprint.

## Prohibited changes in V4

- Hypergraph convolution or incidence aggregation math.
- Anchor/member or pair-moment operators.
- Hyperedge scalar weights or learned attention.
- Candidate routing or Top-K selection.
- Model, loss, decoder, optimizer, feature encoder, or training-budget changes between arms.
- Validation/test/future labels in graph construction.
- Test scoring before a registered candidate GO.
- Candidate D or any follow-on candidate after the three registered candidates.

## Candidate gate

ECPH, ECNH, and OWH are rejected. The registered search is complete with `NO_CONSTRUCTION_SIGNAL`. Do not invent Candidate D or reactivate a rejected candidate within this sprint.
