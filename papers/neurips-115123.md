# Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning

Source: https://neurips.cc/virtual/2025/poster/115123
First opened: 2026-09-20

AI-generated from selected main-body sections; verify against the full paper.

## Summary points

- The excerpts report that most chain-of-thought tokens have low generation entropy, while a small high-entropy subset acts as decision forks that steer reasoning; experimentally lowering entropy at these forks hurt performance, while moderate increases helped.
- During RLVR, entropy patterns largely remained those of the base model, with training changes concentrated on already high-entropy tokens rather than the low-entropy majority.
- Restricting policy-gradient updates to the highest-entropy 20% of tokens matched or exceeded full-token training in the tested Qwen models, especially larger ones, whereas optimizing the lowest-entropy 80% sharply degraded results; the authors caution that the optimal fraction and findings may not generalize beyond their settings.

## Main takeaway

In the tested mathematical RLVR settings, reasoning gains were driven primarily by a small set of high-entropy decision-point tokens, making selective optimization more effective than updating every token.

## My notes
