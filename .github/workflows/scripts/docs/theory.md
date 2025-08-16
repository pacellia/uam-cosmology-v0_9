# Theory ↔ Code Map (Chapter 12 ↔ `theory/uam_model.py`)

Status tags: Deduced / Modeled / Falsifiable / Under revision

1) Law of Temporal Projection — Modeled  
   Code: `UAMModel.get_w_emit()` inversion residual uses the unified redshift law consistent with this relation.

2) Unified Redshift & Time Dilation — Deduced  
   Code: `UAMModel.get_w_emit()` root-finds w_emit(z) from the calibrated residual noted in the file docstring.

3) Expansion Rate E(z) (PX1 ≤ z_switch) — Modeled (β-calibrated)  
   Code: `UAMModel.E(z)`; low-z branch implements PX1 mapping validated on SN/BAO.

4) Distance Ladder — Modeled  
   Code: `get_comoving_angular_distance`, `get_luminosity_distance`, `get_angular_diameter_distance`.

5) BAO Observables — Modeled  
   Code: `get_bao_DM_over_rd`, `get_bao_DH_over_rd`.

6) CMB Acoustic Scale Guardrail — Modeled (provisional)  
   Code: high-z handling inside `E(z)` uses `theory/guardrail.json` (z_switch, z_star, p_mid, p_early); ℓ_A checked in quickstart.

7) Ω_m,UAM = π^3/100 — Deduced (geometric)  
   Implemented as a narrative/constraint; not numerically fitted in PX1 guardrail path.

Notes:
- All provisional items (mid/early high-z exponents, r_s proxy) are declared in `theory/guardrail.json` and surfaced in results JSONs.
