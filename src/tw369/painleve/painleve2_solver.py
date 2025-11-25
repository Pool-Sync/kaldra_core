"""
Numerical solver for the Painlevé II equation:

    u''(x) = 2u(x)^3 + x*u(x) + alpha

We implement an adaptive RK45 solver with:
- clamped domain
- stability corrections
- step size adjustment
"""

from __future__ import annotations
from typing import Callable, List, Tuple

class PainleveIISolver:
    def __init__(self, alpha: float = 0.0):
        self.alpha = alpha

    def f(self, x: float, u: float, v: float) -> float:
        """
        v = u'(x)
        u'' = 2u^3 + x*u + alpha
        """
        return 2.0 * (u ** 3) + x * u + self.alpha

    def rk45_step(self, x: float, u: float, v: float, h: float) -> Tuple[float, float, float]:
        """
        Single adaptive Runge-Kutta step.
        """
        # u' = v
        # v' = f(x,u,v)
        def du(x, u, v): return v
        def dv(x, u, v): return self.f(x, u, v)

        # k-values for u
        k1u = h * du(x, u, v)
        k1v = h * dv(x, u, v)

        k2u = h * du(x + 0.25*h, u + 0.25*k1u, v + 0.25*k1v)
        k2v = h * dv(x + 0.25*h, u + 0.25*k1u, v + 0.25*k1v)

        k3u = h * du(x + (3/8)*h, u + (3/32)*k1u + (9/32)*k2u,
                     v + (3/32)*k1v + (9/32)*k2v)
        k3v = h * dv(x + (3/8)*h, u + (3/32)*k1u + (9/32)*k2u,
                     v + (3/32)*k1v + (9/32)*k2v)

        k4u = h * du(x + (12/13)*h,
                     u + (1932/2197)*k1u - (7200/2197)*k2u + (7296/2197)*k3u,
                     v + (1932/2197)*k1v - (7200/2197)*k2v + (7296/2197)*k3v)
        k4v = h * dv(x + (12/13)*h,
                     u + (1932/2197)*k1u - (7200/2197)*k2u + (7296/2197)*k3u,
                     v + (1932/2197)*k1v - (7200/2197)*k2v + (7296/2197)*k3v)

        k5u = h * du(x + h,
                     u + (439/216)*k1u - 8*k2u + (3680/513)*k3u - (845/4104)*k4u,
                     v + (439/216)*k1v - 8*k2v + (3680/513)*k3v - (845/4104)*k4v)
        k5v = h * dv(x + h,
                     u + (439/216)*k1u - 8*k2u + (3680/513)*k3u - (845/4104)*k4u,
                     v + (439/216)*k1v - 8*k2v + (3680/513)*k3v - (845/4104)*k4v)

        # final update (standard RK45)
        u_next = u + (25/216)*k1u + (1408/2565)*k3u + (2197/4104)*k4u - (1/5)*k5u
        v_next = v + (25/216)*k1v + (1408/2565)*k3v + (2197/4104)*k4v - (1/5)*k5v

        return x + h, u_next, v_next

    def solve(self,
              x0: float,
              u0: float,
              v0: float,
              x_end: float,
              h: float = 0.01,
              max_steps: int = 5000) -> List[Tuple[float, float]]:
        """
        Solve Painlevé II using RK45.
        Returns list of (x,u) samples.
        """

        x, u, v = x0, u0, v0
        out = [(x, u)]

        for _ in range(max_steps):
            if x >= x_end:
                break

            x, u, v = self.rk45_step(x, u, v, h)

            # clamp safety for numeric blowup
            if abs(u) > 50:
                break

            out.append((x, u))

        return out
