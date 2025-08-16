import numpy as _np

# Optional Cobaya Theory base; fall back to a stub for standalone use
try:
    from cobaya.theory import Theory as _CobayaTheory
except Exception:
    class _CobayaTheory:
        pass

class UAMModel(_CobayaTheory):
    """UAM cosmology (PX1 mapping) for SN/BAO regime."""

    def initialize(self):
        self.c_km_s = 299792.458
        self.PI2 = _np.pi / 2.0
        self.EPS = 1e-9
        self._exp_clip = 700.0
        self.mapping = getattr(self, "mapping", None) or self._get_param_or("mapping", "px1")
        self._w_cache = {}
        self._E_cache = {}
        self._H_cache = {}
        self._DM_cache = {}
        self._DL_cache = {}

    def _get_param_or(self, name, default):
        prov = getattr(self, "provider", None)
        if prov is None:
            return default
        try:
            return prov.get_param(name)
        except Exception:
            return default

    # --------- Redshift inversion (PX1): solve g(w)=0 for w in (-pi/2, pi/2)
    # (1+z) = sec^2(w) * exp(tan w)
    # g(w) = ln(1+z) - [ ln(sec^2 w) + tan w ] = 0
    def get_w_emit(self, z):
        if isinstance(z, (list, tuple, _np.ndarray)):
            arr = _np.asarray(z, dtype=float)
            return _np.array([self.get_w_emit(zi) for zi in arr], dtype=float)

        z = float(z)
        key = round(z, 12)
        if key in self._w_cache:
            return self._w_cache[key]
        if z < 0.0:
            raise ValueError("z must be >= 0")
        if z == 0.0:
            self._w_cache[key] = 0.0
            return 0.0

        ln1pz = _np.log1p(z)
        a = -self.PI2 + self.EPS
        b =  self.PI2 - self.EPS

        def g(w):
            c = _np.cos(w)
            if not _np.isfinite(c) or c == 0.0:
                return _np.inf
            ln_sec2 = -2.0 * _np.log(_np.abs(c))
            return ln1pz - (ln_sec2 + _np.tan(w))

        ga, gb = g(a), g(b)
        if not (_np.isfinite(ga) and _np.isfinite(gb) and ga * gb <= 0.0):
            grid = _np.linspace(a, b, 2001)
            prev_w, prev_g = grid[0], g(grid[0])
            found = False
            for w in grid[1:]:
                gw = g(w)
                if _np.isfinite(prev_g) and _np.isfinite(gw) and prev_g * gw <= 0.0:
                    a, b, ga, gb = prev_w, w, prev_g, gw
                    found = True
                    break
                prev_w, prev_g = w, gw
            if not found:
                a, b = -1.45, 1.45
                ga, gb = g(a), g(b)
                if not (_np.isfinite(ga) and _np.isfinite(gb) and ga * gb <= 0.0):
                    raise ValueError(f"Cannot bracket w_emit for z={z}: g(a)={ga}, g(b)={gb}")

        from scipy.optimize import brentq
        w_emit = brentq(g, a, b, xtol=1e-12, rtol=1e-12, maxiter=300)
        self._w_cache[key] = float(w_emit)
        return float(w_emit)

    # --------- Expansion E(z) and H(z) for PX1
    # E = (2 tan w + sec^2 w) / (exp(tan w) * sec^2 w), with w = w_emit(z)
    def E(self, z):
        if isinstance(z, (list, tuple, _np.ndarray)):
            arr = _np.asarray(z, dtype=float)
            return _np.array([self.E(zi) for zi in arr], dtype=float)

        z = float(z)
        key = round(z, 12)
        if key in self._E_cache:
            return self._E_cache[key]

        w = self.get_w_emit(z)
        cw = _np.cos(w)
        if cw == 0.0 or not _np.isfinite(cw):
            val = _np.inf
        else:
            sec2 = 1.0 / (cw * cw)
            tw = _np.tan(w)
            num = 2.0 * tw + sec2
            den = _np.exp(_np.clip(tw, -self._exp_clip, self._exp_clip)) * sec2
            val = num / den
            if not _np.isfinite(val) or val <= 0.0:
                val = _np.inf

        self._E_cache[key] = float(val)
        return float(val)

    def get_Hubble(self, z):
        H0 = float(self._get_param_or("H0", 70.0))
        if isinstance(z, (list, tuple, _np.ndarray)):
            return H0 * self.E(z)
        z = float(z)
        key = (round(z, 12), H0)
        if key in self._H_cache:
            return self._H_cache[key]
        Hz = H0 * self.E(z)
        self._H_cache[key] = float(Hz)
        return float(Hz)

    # --------- Distances (flat)
    # D_M = (c/H0) * integral_0^z [dz' / E(z')];  D_L = (1+z) D_M;  D_A = D_M / (1+z)
    def _integrand_1_over_E(self, zp):
        ez = self.E(zp)
        if not _np.isfinite(ez) or ez <= 0.0:
            return 0.0
        return 1.0 / ez

    def get_comoving_angular_distance(self, z):
        if isinstance(z, (list, tuple, _np.ndarray)):
            arr = _np.asarray(z, dtype=float)
            return _np.array([self.get_comoving_angular_distance(zi) for zi in arr], dtype=float)

        z = float(z)
        if z <= 0.0:
            return 0.0
        key = (round(z, 12), float(self._get_param_or("H0", 70.0)))
        if key in self._DM_cache:
            return self._DM_cache[key]

        from scipy.integrate import quad
        I, _ = quad(self._integrand_1_over_E, 0.0, z, epsabs=1e-8, epsrel=1e-6, limit=300)
        DM = (self.c_km_s / float(self._get_param_or("H0", 70.0))) * I
        self._DM_cache[key] = float(DM)
        return float(DM)

    def get_luminosity_distance(self, z):
        if isinstance(z, (list, tuple, _np.ndarray)):
            arr = _np.asarray(z, dtype=float)
            return _np.array([self.get_luminosity_distance(zi) for zi in arr], dtype=float)
        z = float(z)
        if z <= 0.0:
            return 0.0
        key = (round(z, 12), float(self._get_param_or("H0", 70.0)))
        if key in self._DL_cache:
            return self._DL_cache[key]
        DM = self.get_comoving_angular_distance(z)
        DL = (1.0 + z) * DM
        self._DL_cache[key] = float(DL)
        return float(DL)

    def get_angular_diameter_distance(self, z):
        z = float(z)
        if z <= 0.0:
            return 0.0
        return self.get_comoving_angular_distance(z) / (1.0 + z)

    # --------- BAO helpers
    def get_DH(self, z):
        Hz = self.get_Hubble(z)
        if not _np.isfinite(Hz) or Hz <= 0.0:
            return 0.0
        return self.c_km_s / Hz

    def get_bao_DM_over_rd(self, z):
        rd = float(self._get_param_or("rd", 147.0))
        return self.get_comoving_angular_distance(z) / rd

    def get_bao_DH_over_rd(self, z):
        rd = float(self._get_param_or("rd", 147.0))
        return self.get_DH(z) / rd
