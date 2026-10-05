# Artifact inventory

V17.3 results: 45/45 complete, 0 failures; frozen audit PASS. V17.4 state COMPLETE; source state PASS; integration FROZEN.

| Remote artifact | Count | Verification |
|---|---:|---|
| V17.3 selected checkpoints | 30 | 30 present |
| V17.4 final checkpoints | 50 | 50 SHA matches |
| V17.4 feature caches | 12 | 12 SHA matches |

| Dataset | Nodes × features | Train/valid/test positives | Frozen input SHA | Test candidates SHA | Neg/query |
|---|---:|---:|---|---|---:|
| Cora | 2708 × 1433 | fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8/263/527 | 51eb7c621a1db083fcef492018bb03a70381ee5e185561bb44c29315fe886be4 | c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1 | 20 |
| Pubmed | 19717 × 500 | 2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1/2216/4432 | 1f14420934cfa1790b7ce735cedf3d9c5512419e4753cdda17cc68f29400b560 | b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2 | 20 |
| Citeseer | 3327 × 3703 | a3a8ecda0bb59b7d6b51efb8bd0087f9f19a710bda2b9ebedec5a2c20aa32ec2/227/455 | c23e76f70bd189bb445802bd42622fbef7dc46e2ff0b140d30129cae4295075e | efe1753a1b17cbfd1139a2a5311d736c1aa1932f86ba1ae08cbc651a9f9b4b6a | 20 |

Full raw/processed file paths and hashes, per-array hashes, checkpoint digests, and cache digests are preserved in REMOTE_HASH_VERIFICATION.json and SOURCE_HASHES.json. The recorded Cora original-raw folder is incomplete; both versions used the same identified processed input cache, so the compared model input and split are hash-identical.
