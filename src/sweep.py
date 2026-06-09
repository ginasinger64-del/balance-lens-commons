import numpy as np

# ----------------------------------------------------------------------
# Minimal resource-coupled replicator sim.
# Well-mixed mean field: payoff depends only on (strategy, R), so every
# agent of a strategy is identical -> track fractions, not 30 agents.
#
# LOAD-BEARING CHOICES (stated, not hidden):
#  - Payoffs:  defect = 12*(R/Rmax)^alpha   (coupled)
#              coop   = 5                    (flat, no harvest from R)
#              repair = 2                    (flat)  <-- dominated by coop
#  - Resource: logistic self-regen + harvest by defectors + restore by repair
#       R <- R + g*R*(1-R/Rmax) - delta*frac_D*N + rho*frac_R*N   (clamped)
#  - Selection: imitate strategy with highest LAST-5-TURN AVERAGE payoff
#       (recent payoff, NOT lifetime accumulation)
#  - revision rate beta per turn, plus small mutation eps for ergodicity
# ----------------------------------------------------------------------

Rmax = 100.0
N    = 30
g    = 0.10      # logistic regen rate
delta= 1.20      # depletion per defector per turn (as fraction of pop)
rho  = 1.50      # restoration per repairer
beta = 0.30      # fraction of pop revising strategy each turn
eps  = 0.01      # mutation
T    = 4000      # turns
burn = 2000      # discard for time-averages

def payoffs(R, alpha):
    return {
        'D': 12.0 * (R/Rmax)**alpha,
        'C': 5.0,
        'R': 2.0,
    }

def run(alpha, seed=0):
    rng = np.random.default_rng(seed)
    frac = {'C': 1/3, 'D': 1/3, 'R': 1/3}
    R = Rmax
    hist = {'C': [], 'D': [], 'R': []}     # recent payoff windows
    fD_trace, R_trace = [], []
    for t in range(T):
        pay = payoffs(R, alpha)
        for k in hist:
            hist[k].append(pay[k])
            if len(hist[k]) > 5:
                hist[k].pop(0)
        recent = {k: float(np.mean(hist[k])) for k in hist}
        # resource update
        regen = g * R * (1 - R/Rmax)
        R = R + regen - delta*frac['D']*N/N*Rmax/Rmax*N*0  # placeholder removed below
        R = max(0.0, min(Rmax, R + (-delta*frac['D'] + rho*frac['R'])*N*0 ))
        # (clean re-do of resource line below)
        break
    return None

# the placeholder above got messy; redo run cleanly
def run(alpha, seed=0):
    rng = np.random.default_rng(seed)
    frac = np.array([1/3, 1/3, 1/3])  # order: C, D, R
    keys = ['C','D','R']
    R = Rmax
    win = {k: [] for k in keys}
    fD_trace, R_trace, fR_trace = [], [], []
    for t in range(T):
        pay = payoffs(R, alpha)
        for k in keys:
            win[k].append(pay[k])
            if len(win[k]) > 5: win[k].pop(0)
        recent = np.array([np.mean(win[k]) for k in keys])
        # --- resource dynamics ---
        regen   = g * R * (1 - R/Rmax)
        harvest = delta * frac[1] * N      # defectors
        restore = rho   * frac[2] * N      # repairers
        R = min(Rmax, max(0.0, R + regen - harvest + restore))
        # --- selection: revise toward best recent-avg payoff ---
        best = np.argmax(recent)
        new = frac.copy()
        # beta of the population moves toward 'best'
        moved = beta * (1 - frac[best])
        new = new * (1 - beta) 
        new[best] += beta * 1.0
        # renormalize via imitation of best (proportional pull to best)
        # simpler transparent rule: shift mass beta*frac_i from each i to best
        frac2 = frac.copy()
        flow_to_best = beta * np.array([frac[i] if i!=best else 0 for i in range(3)])
        frac2 = frac - flow_to_best
        frac2[best] += flow_to_best.sum()
        # mutation
        frac2 = (1-eps)*frac2 + eps*np.array([1/3,1/3,1/3])
        frac = frac2/frac2.sum()
        fD_trace.append(frac[1]); R_trace.append(R); fR_trace.append(frac[2])
    fD = np.array(fD_trace[burn:]); Rt = np.array(R_trace[burn:])
    return {
        'alpha': alpha,
        'mean_fD': fD.mean(),
        'std_fD': fD.std(),
        'mean_R': Rt.mean(),
        'std_R': Rt.std(),
        'min_R': Rt.min(),
        'final_repair': fR_trace[-1],
        'Rstar_pred': Rmax*(5/12)**(1/alpha),
    }

print(f"{'alpha':>6} {'mean_fD':>8} {'std_fD':>7} {'mean_R':>7} {'std_R':>6} {'min_R':>6} {'R*pred':>7} {'regime'}")
for a in [0.5,1,1.5,2,2.5,3,3.5,4,5,6]:
    r = run(a)
    osc = r['std_fD'] > 0.05
    if r['mean_fD'] > 0.6:
        regime = 'DEFECT dominates'
    elif osc:
        regime = 'OSCILLATION'
    else:
        regime = 'coop-stable'
    print(f"{a:>6.1f} {r['mean_fD']:>8.3f} {r['std_fD']:>7.3f} "
          f"{r['mean_R']:>7.1f} {r['std_R']:>6.2f} {r['min_R']:>6.1f} "
          f"{r['Rstar_pred']:>7.1f}  {regime}")
