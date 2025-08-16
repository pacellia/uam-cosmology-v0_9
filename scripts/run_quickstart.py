import json, os, sys
from math import pi
import numpy as np

# --- import your model ---
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "theory"))
from uam_model import UAMModel  # assumes theory/uam_model.py exists

# ---- load guardrail (single source of truth) ----
GR_PATH = os.path.join(os.path.dirname(__file__), "..", "theory", "guardrail.json")
with open(GR_PATH, "r") as f:
    guard = json.load(f)

H0 = 70.0
rd = float(guard.get("rs_proxy_Mpc", 147.0))

# minimal provider stub for the model
class _Provider:
    def __init__(self, H0, rd, mapping):
        self._params = {"H0": float(H0), "rd": float(rd), "mapping": str(mapping)}
    def get_param(self, key):
        return self._params[key]

# build model
m = UAMModel()
m.provider = _Provider(H0, rd, guard.get("mapping", "px1"))
m.initialize()

# ---- quick checks ----
C = 299792.458

def small_z_check(z=0.01):
    DL = m.get_luminosity_distance(z)
    return DL / z

def bao_row(z):
    DM_over = m.get_comoving_angular_distance(z) / rd
    DH_over = (C / m.get_Hubble(z)) / rd
    return z, DM_over, DH_over

print("=== UAM quickstart: PX1 + guardrail metadata ===")
print(json.dumps(guard, indent=2))

# small-z slope
z_small = 0.01
slope = small_z_check(z_small)
print(f"\nSmall-z slope D_L({z_small})/{z_small} = {slope:.2f} Mpc  (c/H0≈{C/H0:.2f})")

# BAO magnitudes (sanity: expect O(10–30))
for zb in [0.35, 0.57, 0.70, 1.00, 1.50]:
    z, dm_over, dh_over = bao_row(zb)
    print(f"BAO z={z:>4}:  D_M/rd={dm_over:7.2f}   D_H/rd={dh_over:7.2f}")

print("\nOK. Results should match your earlier PX1 numbers.")

