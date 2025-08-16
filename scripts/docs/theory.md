# Theory ↔ Code Map (UAM v0.9: PX1 + Tri-piece Guardrail)

This document links the Chapter 12 equations to their implementation points.

## Core mappings

- Law of Temporal Projection  
  **Equation**: t(w) = T · exp(β · tan w)  
  **Code**: `theory/uam_model.py` → used implicitly by the redshift inversion.

- Unified Redshift & Time Dilation  
  **Equation**: 1+z = [sec²(w_obs)/sec²(w_emit)] · exp[β (tan w_obs − tan w_emit)]  
  **Code**: `UAMModel.get_w_emit(z)` (PX1 inversion).

- Expansion rate (low-z, PX1 path)  
  **Form**: E(w) consistent with PX1 mapping; H(z) = H0 · E(z)  
  **Code**: `UAMModel.E(z)`, `UAMModel.get_Hubble(z)`.

- Distances  
  **Equations**:  
  χ(z) = (c/H0) ∫₀ᶻ dz′/E(z′),  D_M=χ,  D_L=(1+z)D_M,  D_A=D_M/(1+z)  
  **Code**: `UAMModel.get_comoving_angular_distance`, `get_luminosity_distance`, `get_angular_diameter_distance`.

- BAO observables  
  **Equations**: D_M/ r_d,  D_H/ r_d with D_H = c/H(z)  
  **Code**: `UAMModel.get_bao_DM_over_rd`, `get_bao_DH_over_rd`.

## High-z guardrail (CMB scaffold)

- Single source of truth: `theory/guardrail.json`  
  Keys: `mapping`, `z_switch`, `z_star`, `p_mid`, `p_early`, `rs_proxy_Mpc`.

- Usage: For repo quickstart, we keep PX1 intact for z≤2 and only **report** the guardrail values (full tri-piece integration code lives in the notebooks/scripts used to generate the saved JSON artifacts in `results/`).

## Status tags

- **Deduced**: Ω_m,UAM = π³/100  
- **Modeled**: PX1 low-z mapping; tri-piece exponents p_mid, p_early (scaffold only)  
- **Falsifiable**: BAO magnitudes, SN Hubble diagram, CMB acoustic scale (ℓ_A)

For derivational detail, see Chapter 12 of *Reason’s Arc* and the validation checklist mapping in `docs/methods.md`.

