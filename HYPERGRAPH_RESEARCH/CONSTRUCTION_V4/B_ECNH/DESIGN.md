# ECNH implementation and screen

For each undirected observed edge `(u,v)` in the current message graph, compute `CN(u,v)`. Skip empty intersections; sort remaining common neighbors by `(message_graph_degree, node_id)` and keep at most 16. Build `{u,v} ∪ CN(u,v)` and append it to the existing raw stars. The builder only sees the already target-masked edge list.

B1 and B2 are matched one-to-one to the unique B3 additions after removing true groups that collide with Raw stars and deduplicating repeated groups. The first deterministic supporting observed edge represents each unique true group. The controls therefore preserve the actual B3 added-hyperedge count and exact size multiset while B1 samples from all nodes excluding endpoints and B2 samples from `N(u) ∪ N(v) \ {u,v}`. Control samples retry to avoid duplicate/raw collisions; any remaining collision is recorded in statistics.

See `../01_NOVELTY_SEARCH.md` for the focused novelty assessment. The exact formula was not found in the searched primary sources, but edge-centric hypergraph representation and common-neighbor-aware link prediction are established. Do not claim either broad idea as new.
