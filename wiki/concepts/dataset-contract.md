---
title: Dataset Contract
type: concept
tags: [dataset, synthetic, integrity]
related:
  - "[[Aegis-JKN Overview]]"
  - "[[Verifier Dashboard]]"
  - "[[Academic Paper]]"
sources:
  - docs/datasets/klaim-aegis-jkn-dataset.json
  - docs/DATA_SCHEMA.md
---

# Dataset Contract

The canonical Aegis-JKN source is a read-only JSON array of 300 synthetic claims. The baseline SHA-256 is recorded in `docs/DATA_SCHEMA.md`. The dashboard carries a byte-identical copy for static local operation.

## Important limits

The records contain precomputed risk, score, channel contribution, and explanatory prose. They do not contain production IDs, INA-CBG tariff comparisons, graph edge lists, or numeric feature-level SHAP values. Components must display those boundaries rather than invent unsupported values.
