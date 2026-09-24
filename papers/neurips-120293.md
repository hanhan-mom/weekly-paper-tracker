# Latent Chain-of-Thought for Visual Reasoning

Source: https://neurips.cc/virtual/2025/poster/120293
First opened: 2026-09-15

AI-generated from selected main-body sections; verify against the full paper.

## Summary points

- LaCoT formulates visual chain-of-thought as latent-variable inference and trains a GFlowNet-based rationale sampler with reference-guided exploration rather than relying on teacher-forced traces or KL-constrained reward maximization.
- It approximates token-level rewards by computing rewards at intervals and interpolating intermediate values; the reported ablation shows that a smaller interval improved overall average performance from 45.6 to 47.0, while requiring more training time.
- The experiments and qualitative examples report more accurate or diverse reasoning than SFT and GRPO, but multi-rationale inference adds computational cost, training required substantial GPU time, evaluation was limited to models up to 7B parameters, and hallucination remains unaddressed.

## Main takeaway

The excerpts support LaCoT as a probabilistic approach that improves visual reasoning by learning diverse latent rationales, with added training and inference costs and unresolved scalability and hallucination limitations.

## My notes
