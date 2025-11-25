"""
Painlevé II Filter implementation for TW369.
Applies the PainleveIISolver to smooth the instability index.
"""

from src.tw369.painleve.painleve2_solver import PainleveIISolver

def painleve_filter(instability_index: float) -> float:
    """
    Applies Painlevé II filtering to the instability index.
    
    Process:
    1. Map instability_index to solver domain x.
    2. Run PainleveIISolver.
    3. Extract final u value.
    4. Clamp result to [-1, 1].
    """
    
    # 1. Map input to domain parameters
    # We map the instability index to an initial condition u0
    # and solve over a short interval to get the filtered response.
    # This mapping is heuristic based on the "Engine Upgrade" specs.
    
    solver = PainleveIISolver(alpha=0.0)
    
    # Mapping strategy:
    # x0 is fixed at 0
    # u0 is the input instability_index (scaled if necessary, here 1:1)
    # v0 is 0 (assuming starting from rest)
    # x_end is a small step forward to allow the dynamics to act
    
    x0 = 0.0
    u0 = instability_index
    v0 = 0.0
    x_end = 1.0 # Integration window size
    h = 0.05    # Step size
    
    # 2. Run Solver
    results = solver.solve(x0, u0, v0, x_end, h=h)
    
    if not results:
        return instability_index # Fallback
        
    # 3. Extract final u value
    _, u_final = results[-1]
    
    # 4. Clamp result
    if u_final > 1.0:
        return 1.0
    if u_final < -1.0:
        return -1.0
        
    return u_final
