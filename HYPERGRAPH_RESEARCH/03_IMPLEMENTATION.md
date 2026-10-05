# 03 — implementation

## Module

New file: `src/dcdlp/models/hypergraph.py`.

For the target-masked message graph (G_m=(V,E_m)), the branch constructs one closed-neighborhood hyperedge per non-isolated center:

\[
 e_c = \{c\}\cup N_{G_m}(c).
\]

The raw incidence message is

\[
 r_v = \frac{1}{d_H(v)}\sum_{e\ni v}\frac{1}{|e|}\sum_{u\in e}h_u.
\]

The proposed complement is

\[
 r_v^\perp = r_v - \frac{r_v^\top h_v}{\|h_v\|_2^2+\epsilon}h_v,
 \qquad h'_v=h_v+W r_v^\perp.
\]

The same `W` is used by the raw, complement, pairwise and shuffled controls. The `pairwise` control replaces the set summary with an ordinary co-membership average; `shuffled` rolls the node assignment of the hypergraph message while preserving its marginal values.

## Switches

`DCDLP` accepts `hypergraph_mode` in `disabled`, `raw`, `complement`, `pairwise`, and `shuffled` (`src/dcdlp/models/dcdlp.py:11-56`). `disabled` does not instantiate the branch, preserving the original parameterization. The CLI exposes the switch at `src/dcdlp/cli.py:210-215`; `TrainConfig` and checkpoint restoration carry it through `src/dcdlp/train.py:41-88`, `src/dcdlp/train.py:498-508`, and `src/dcdlp/evaluate.py:227-238`.

## Leakage and protocol behavior

The branch runs after `mask_pair_edges` and receives only `message_edges` (`src/dcdlp/models/dcdlp.py:68-88`). Therefore each forward pass rebuilds incidence from the currently allowed message graph. No validation/test label, target label, candidate score or future edge is used. The current LPShift limitation remains unchanged: the loader still cannot represent the official extra context edges, so this branch was not evaluated on LPShift.

## Cost

- The incidence pass avoids materializing a dense (H\) matrix and iterates over closed-neighborhood memberships.
- For hidden dimension 16, the added `message_linear` contributes 256 parameters. The Cora screen used 24,478 parameters for `disabled` and 24,734 for every enabled mode.
- Because the implementation rebuilds star incidence per forward batch, it is suitable for a low-cost falsification screen, not yet for large-scale LPShift. A future adapter should cache split-level incidence while preserving per-target masking or use a sparse incremental update.

## Tests

`tests/test_hypergraph_module.py` checks all four enabled modes for finite shape-preserving output and checks the disabled DCDLP output contract. Together with the existing branch/output/split tests, the final run passed 20 tests.

