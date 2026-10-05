# Hash reconciliation

Official NCN/NCNC identity: GraphPKU/NeuralCommonNeighbor@11d597013750da17ce7468e344bec756a7af39a4. The V17.4 backbone adapter hash is read from its audit record and equals the V17.3 benchmark adapter hash. The V17.4 orchestration runner is separately recorded; it wraps the unchanged adapter and was not misclassified as that adapter.

V17.3 and V17.4 frozen R-HSPE configuration hashes match. All 37 runtime Python source hashes and the ranking evaluator hash match. V17.3 selected checkpoints exist; all 50 V17.4 final checkpoints and all 12 feature caches hash-match their manifests. Full file lists, input arrays, data paths, split/candidate hashes and checkpoint hashes are retained in SOURCE_HASHES.json and REMOTE_HASH_VERIFICATION.json.

The only R-HSPE source variant difference is audit tolerance 2e-7 to 5e-7 and audit metadata; method/training AST is unchanged. No unresolved implementation or artifact mismatch was found.

The adapter hash is the V17.4 audit's backbone_adapter_sha256 (which matches the V17.3 benchmark adapter); the separate V17.4 orchestration runner has its own SHA and is recorded separately. R-HSPE config comparison uses V17.4 AUDIT.json frozen_config_sha256, not the unrelated parent DCDLP common-config digest.
