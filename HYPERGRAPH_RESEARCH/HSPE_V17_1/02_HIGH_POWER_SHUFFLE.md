# Global hyperedge-size-label shuffle

Raw-star hyperedge identity is its center. Permute size labels across all nonempty train-visible hyperedge identities, preserving the complete global label multiset. Incidence, shared supports, candidate token identities/order/counts and support counts remain frozen.

Training permutation seeds: Cora17110101, PubMed17110201. Validation uses independent fixed seeds Cora17110102, PubMed17110202. Permutations do not depend on model seed or labels.

For train-positive target masking, first compute effective size labels of the target-masked graph (subtract one from endpoint-centered hyperedge labels), then permute those labels by the same fixed donor identity mapping. This preserves the full target-masked label multiset. Tokens are enumerated only from the true masked incidence graph; no token is added or removed by a permuted label.

Reconstruct every token's hyperedge identities and compare original descriptors, token offsets and support counts against the V17 cache before creating shuffled/rank features. All original-descriptor differences must be <=2e-6. No overlap features are introduced.

Informative pair: any existing token descriptor changes. Power adequate iff fraction >=50%; zero-token candidates cannot change and their fraction determines a measurable upper bound. Low power is reported and does not block primary efficacy.

## Completed feature preflight

Original descriptors exactly matched the V17 cache (maximum error 0); all counts, support and token topology matched. Global size multiset was preserved exactly. Cora train informative fraction 48.9862%, validation 11.8957% (nonempty validation ceiling 11.9138%). PubMed train 45.8501%, validation 10.0228% (nonempty validation ceiling 10.0228%). All splits are LOW_SHUFFLE_POWER under the absolute >=50% criterion. Almost every nonempty candidate changes, but the empty-token population limits attainable power. No control definition is changed in response.
