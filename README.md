    # UAM (Unified Angular Mathematics) – PX1 + Tri-piece Guardrail (v0.9)

    This export contains a curated, reproducible snapshot of the UAM validation pipeline:
    - `theory/uam_model.py` – PX1 (z<=2) + tri-piece high-z closure (guardrail.json)
    - `results/*.json`      – small-z, BAO, and CMB anchor artifacts
    - `env/requirements*.txt` – reproducible environment
    - `notebooks/`          – quickstart and validation notebooks (if present)
    - `scripts/`            – runnable scripts (if present)

    ## Quickstart (Colab or Codespaces)
    1. `pip install -r env/requirements.txt`
    2. Open `notebooks/00_quickstart.ipynb` and run all cells.
    3. Artifacts will be written under `results/`.

    ## Guardrail parameters (single source of truth)
    See `theory/guardrail.json`:
    ```json
    {
  "mapping": "px1",
  "z_switch": 2.0,
  "z_star": 1090.0,
  "p_mid": 1.503892,
  "p_early": 2.0,
  "rs_proxy_Mpc": 147.0
}
    ```
    These ensure:
    - SN/BAO: PX1 mapping is unchanged (validated)
    - CMB: physical anchor via D_A(z*) and finite r_s, with continuity at z_switch and z_star

    ## Notes
    - No raw data is included; use scripts or notebook cells to fetch licensed datasets.
    - This is the v0.9 export; a DOI can be minted on release.
