import pytest
from src.tw369.painleve.painleve2_solver import PainleveIISolver

class TestPainleveIISolver:
    def test_initialization(self):
        solver = PainleveIISolver(alpha=0.5)
        assert solver.alpha == 0.5

    def test_rk45_step(self):
        solver = PainleveIISolver(alpha=0.0)
        x, u, v = 0.0, 1.0, 0.0
        h = 0.01
        
        x_next, u_next, v_next = solver.rk45_step(x, u, v, h)
        
        assert x_next == x + h
        # For small h, u should change slightly
        assert u_next != u
        assert abs(u_next - u) < 0.1

    def test_solve_basic(self):
        solver = PainleveIISolver(alpha=0.0)
        results = solver.solve(x0=0.0, u0=0.1, v0=0.0, x_end=1.0, h=0.1)
        
        assert len(results) > 0
        assert results[0] == (0.0, 0.1)
        assert results[-1][0] >= 1.0

    def test_solve_blowup_protection(self):
        # Painlevé II can blow up for certain initial conditions
        # We check if the solver stops when u > 50
        solver = PainleveIISolver(alpha=0.0)
        # Large initial u should trigger blowup quickly
        results = solver.solve(x0=0.0, u0=60.0, v0=0.0, x_end=1.0)
        
        # Should return initial state and maybe one step before breaking
        # But if u0 > 50, it might break immediately in the loop
        # The loop checks clamp safety after step.
        # So it will do at least one step if u0 is not checked before loop.
        # The implementation checks:
        # x, u, v = self.rk45_step(x, u, v, h)
        # if abs(u) > 50: break
        
        # If we start with u0=60, the first step will likely result in u > 50.
        # So we expect results to contain at least the initial point.
        
        assert len(results) >= 1
        assert results[0][1] == 60.0
        
        # If it took steps, the last one should be the one that triggered break or just before?
        # The code appends AFTER the check.
        # if abs(u) > 50: break
        # out.append((x, u))
        # So if it breaks, the blowing up value is NOT appended.
        
        # So if u0=60, and next step is > 50, it breaks and doesn't append.
        # So only (0, 60) should be there.
        assert len(results) == 1
