# Methods & Validation Checklist

This repo provides a minimal, reproducible path to verify:
- Small-z slope: D_L(z)/z → c/H0
- BAO magnitudes: D_M/rd and D_H/rd are O(10–30) at z≈0.3–1.5
- CMB anchor: ℓ_A ≈ 300 via D_A(z*) and r_s proxy

How to run:
1) `pip install -r env/requirements.txt`
2) `python scripts/run_quickstart.py`
3) Inspect `results/quickstart_smoke.json`

Checklist mapping:
- Temporal/Redshift equations → see `theory/uam_model.py` (w(z) inversion, E(z))
- Distances/BAO → `run_quickstart.py` produces magnitudes and saves JSON
- CMB acoustic scale → `run_quickstart.py` computes ℓ_A from D_A(z*) and r_s proxy

Provisional components:
- High-z guardrail exponents (p_mid, p_early) and r_s proxy are placeholders; recorded in `theory/guardrail.json`.
- PX1 remains the validated low-z mapping; future releases will replace guardrail with first-principles strong-z derivation and UAM r_s.
