# Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models

Source: https://github.com/deepseek-ai/Engram/blob/main/Engram_paper.pdf
First opened: 2026-09-18

AI-generated from selected main-body sections; verify against the full paper.

## Summary points

- Engram adds conditional memory to MoE models, using compressed suffix n-grams and multi-head hashing for deterministic embedding-table lookups, then filtering retrieved values through hidden-state-dependent gates and a lightweight causal convolution.
- The paper reports that splitting a fixed parameter budget between MoE computation and Engram memory follows a U-shaped allocation pattern, with its 27B hybrid outperforming iso-parameter, iso-FLOPs MoE baselines across knowledge, reasoning, code, math, and long-context benchmarks.
- The authors attribute the gains to offloading static local-pattern reconstruction from early Transformer layers, freeing depth and attention for global reasoning; deterministic addressing also permits host-memory prefetching, with a reported overhead below 3% for a 100B-parameter table.

## Main takeaway

The excerpts support conditional lookup memory as a complementary form of sparsity that can improve model quality and expand capacity beyond GPU memory when combined with MoE computation.

## My notes
