import os, json, math, time, sys
from math import pi
from pathlib import Path

# --- repo sanity ---
root = Path(".").resolve()
theory = root / "theory"
results = root / "results"
results.mkdir(exist_ok=True, parents=True)

# --- import model ---
sys.path.insert(0, str(theory))
from uam_model import UAMModel  # assumes this file already exists in theory/

# --- load guardrail (single source of truth) ---
guardrail_path = theory / "guardrail.json"
if not guardrail_path.exists():
    # fail soft but clear
    print("ERROR: theory/guardrail.json not found.")
    sys.exit(1)

with open(guardrail_path, "r") as f:
    guard = json.load(f)

H0 = float(guard.get("H0", 70.0))  # default if not present
rd = float(guard.get("rs_proxy_Mpc", 147.0))
mapping = guard.get("mapping", "px1")
z_switch = float(guard.get("z_switch", 2.0))
z_star = float(guard.get("z_star", 1090.0))

# --- minimal provider stub for the model ---
class _Provider:
    def __init__(self, H0, rd, mapping):
        self._params = {"H0": float(H0), "rd": float(rd), "mapping": str(mapping)}
    def get_param(self, key):
        return self._params[key]

# --- construct model ---
model = UAMModel()
model.provider = _Provider(H0, rd, mapping)
model.initialize()

C_KM_S = 299792.458

# --- small-z slope check ---
z_small = 0.01
Dl_small = model.get_luminosity_distance(z_small)
slope = Dl_small / z_small
target = C_KM_S / H0

# --- BAO checks ---
bao_z = [0.35, 0.57, 0.70, 1.00, 1.50]
bao = []
for z in bao_z:
    dm_over = model.get_bao_DM_over_rd(z)
    dh_over = model.get_bao_DH_over_rd(z)
    bao.append({"z": z, "DM_over_rd": dm_over, "DH_over_rd": dh_over})

# --- CMB anchor (uses model's high-z guardrail; DA = DM/(1+z*)) ---
DM_star = model.get_comoving_angular_distance(z_star)
DA_star = DM_star / (1.0 + z_star)
ell_A = pi * DA_star / rd

# --- print console summary ---
print(f"Small-z slope D_L(0.01)/0.01 = {slope:.2f} Mpc  (c/H0≈{target:.2f})")
for row in bao:
    print(f"BAO z={row['z']:.2f}:  D_M/rd={row['DM_over_rd']:6.2f}   D_H/rd={row['DH_over_rd']:6.2f}")
print(f"ell_A (DA-based) = {ell_A:.2f}  |  D_A(z*) = {DA_star:.2f} Mpc  |  D_M(z*) = {DM_star:.2f} Mpc")

# --- write artifact ---
artifact = {
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "guardrail": guard,
    "H0": H0,
    "rd_proxy_Mpc": rd,
    "small_z": {"z": z_small, "DL_over_z_Mpc": float(slope), "target_c_over_H0_Mpc": float(target)},
    "bao": bao,
    "cmb": {"z_star": z_star, "DA_Mpc": float(DA_star), "DM_Mpc": float(DM_star), "ell_A": float(ell_A)},
}
out = results / "quickstart_smoke.json"
with open(out, "w") as f:
    json.dump(artifact, f, indent=2)
print(f"Saved: {out}")
