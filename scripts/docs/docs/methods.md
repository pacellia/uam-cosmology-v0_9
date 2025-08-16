# Methods & Validation Checklist (UAM v0.9)

This repository is organized for a single, simple reviewer path. Each checklist item points to a script/notebook and the artifact it writes in `results/`.

## Quickstart (sanity)

- **Small-z slope**: D_L(z)/z → c/H0 at z→0  
  Run: `scripts/run_quickstart.py`  
  Artifact: console output

- **BAO magnitude sanity**: D_M/rd, D_H/rd = O(10–30) at z≈0.35–1.5  
  Run: `scripts/run_quickstart.py`  
  Artifact: console output

## Cosmology scaffold

- **CMB anchor (ℓ_A)**: Guardrail parameters in `theory/guardrail.json` are calibrated so that ℓ_A ≈ 300 using the tri-piece closure (PX1 preserved for z≤2).  
  Artifacts: `results/*guardrail*.json` (committed when generated).

## Equation status & consistency

- **Foundational**: Redshift inversion and E(z) continuity (PX1).  
  Verified by quickstart output and unit checks in scripts.

- **Deduced parameter**: Ω_m,UAM = π³/100 (used narratively; not fit).  
  Verified by code comments and absence of Ω_m fitting in scripts.

## Data policy

- No raw survey data is committed.  
- Use a data-fetch script (to be added in a future commit) or load local copies.  
- BAO/SN examples in quickstart are **sanity only** (not formal likelihoods).

## Reproducibility

- Environments pinned in `env/requirements.txt` (and lock file).  
- Guardrail is a single JSON source shared across scripts/notebooks.  
- Results saved as JSON with parameters & version notes.

## What is provisional (v0.9)

- Tri-piece high-z closure is a **scaffold** to match ℓ_A while we finalize the strong-z β-derived mapping and compute r_s self-consistently.  
- Full MCMC/likelihood integration (e.g., Cobaya) is deferred to a later release.

## Next release (v1.0 goals)

- Replace guardrail with β-derived strong-z E(w).  
- Implement UAM r_s with microphysics and cs(z).  
- Add formal SN/BAO/CMB likelihoods and ΛCDM baseline scripts.

