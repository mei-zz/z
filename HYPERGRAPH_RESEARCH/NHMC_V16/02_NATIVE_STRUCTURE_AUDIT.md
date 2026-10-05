# Native structure and target-mask audit

All Stage 0 datasets completed on train-only positives and matched negatives. The sampled full rebuild checked 100 training positives per dataset. For each dataset, target-masked rebuilds matched the implemented native-token computation exactly; endpoint-swapped features were identical; maximum absolute token difference was 0 (tolerance 1e-6). No test evaluation was run.

|Dataset|Pairs audited|Full rebuild equal|Endpoint symmetry|Max difference|Tokens|Maximum tokens/pair|
|---|---:|---|---|---:|---:|---:|
|CORA|100|True|True|0|135189|372|
|PUBMED|100|True|True|0|4976014|4856|
|CITESEER|100|True|True|0|161491|1101|

PubMed has substantial token variation (4,976,014 tokens; maximum 4,856 per pair), so the transfer fallback condition is not met. Its fixed-summary content increment is below threshold; the diagnostic-only override allows neural Stage 1 to test whether the learned set encoder uses signal that the handcrafted summary misses.
