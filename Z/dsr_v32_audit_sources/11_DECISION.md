# DSR V32 decision

DYNAMIC_ROUTING_GAIN: REPLICATED
MULTI_SOURCE_GAIN: EXPLORATORY
BEATS_DUP_GRAPH: YES
ROUTER_CORRESPONDENCE: SUPPORTED
ROUTER_COLLAPSE: {'cora': False, 'pubmed': False}
CITESEER_TRANSFER: IMPROVED
CITESEER_TRANSFER_EFFECTS: {'A6_DSR_minus_NCNC_mrr': {'mean': 0.006628526066852047, 'std': 0.015091195566287238, 'wins': 2, 'n': 3, 'per_seed': [-0.01067522174350366, 0.017063492063492114, 0.013497307880567688]}, 'A6_DSR_minus_R_only_mrr': 0.027820755684191883, 'A1_R_only_minus_NCNC_mrr': -0.021192229617339835, 'A1_R_only_minus_NCNC_per_seed': [-0.01788932433205559, -0.025201034892664897, -0.020486329627299016], 'A6_DSR_minus_NCNC_per_seed': [-0.01067522174350366, 0.017063492063492114, 0.013497307880567688]}
phase_A_nominated: {'cora': ['A4'], 'pubmed': ['A7', 'A4']}
replicated_contrasts: [('pubmed', 'A4')]
test_opened: False
innovation1_modified: False
novelty_status: NOT_AUDITED

Novelty is not evaluated in this performance sprint. Mixture-of-experts and softmax gating are established methods. Positive performance would show a result relative to these controls, not a novelty proof.
