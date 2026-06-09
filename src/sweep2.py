import numpy as np

Rmax = 100.0
g     = 0.20      # logistic regen rate
delta = 0.15      # depletion per unit defector-fraction (scale-matched to regen)
rho   = 0.20      # restoration per unit repair-fraction
eps   = 0.005     # mutation floor
T     = 6000
burn  = 3000

def payoffs(R, alpha):
    return np.array([5.0,                      # C flat
                     12.0*(R/Rmax)**alpha,     # D coupled
                     2.0])                      # R flat (dominated by C)

def run(alpha, couple_repair=False, seed=0):
    keys = ['C','D','R']
    frac = np.array([1/3,1/3,1/3])
    R = Rmax
    win = []
    fD_tr, R_tr = [], []
    for t in range(T):
        p = payoffs(R, alpha)
        if couple_repair:
            # repair pays MORE as resource is scarcer: 2 + 8*(1-R/Rmax)
            p[2] = 2.0 + 8.0*(1.0 - R/Rmax)
        win.append(p)
        if len(win) > 5: win.pop(0)
        recent = np.mean(win, axis=0)
        # resource dynamics
        regen   = g * R * (1 - R/Rmax)
        harvest = delta * frac[1] * Rmax
        restore = rho   * frac[2] * Rmax
        R = min(Rmax, max(0.0, R + regen - harvest + restore))
        # discrete replicator on recent payoff
        avg = np.dot(frac, recent)
        frac = frac * (recent/avg)
        frac = (1-eps)*frac + eps*(1/3)
        frac = frac/frac.sum()
        fD_tr.append(frac[1]); R_tr.append(R)
    fD = np.array(fD_tr[burn:]); Rt = np.array(R_tr[burn:])
    return dict(alpha=alpha, mfD=fD.mean(), sfD=fD.std(),
                mR=Rt.mean(), sR=Rt.std(), minR=Rt.min(),
                Rstar=Rmax*(5/12)**(1/alpha))

def regime(r):
    if r['mfD'] > 0.5:            return 'DEFECT dominates'
    if r['sfD'] > 0.04 or r['sR']>4: return 'OSCILLATION'
    return 'coop-stable'

print("=== repair FLAT (dominated) — defect vs coop only ===")
print(f"{'a':>4} {'mean_fD':>8} {'sd_fD':>6} {'mean_R':>7} {'sd_R':>6} {'min_R':>6} {'R*':>6}  regime")
for a in [0.5,1,1.5,2,2.5,3,4,5,6,8]:
    r = run(a, couple_repair=False)
    print(f"{a:>4.1f} {r['mfD']:>8.3f} {r['sfD']:>6.3f} {r['mR']:>7.1f} {r['sR']:>6.2f} {r['minR']:>6.1f} {r['Rstar']:>6.1f}  {regime(r)}")

print()
print("=== repair COUPLED (pays more as R falls) — can a restoring strategy survive? ===")
print(f"{'a':>4} {'mean_fD':>8} {'sd_fD':>6} {'mean_R':>7} {'sd_R':>6} {'min_R':>6} {'R*':>6}  regime")
for a in [0.5,1,1.5,2,2.5,3,4,5,6,8]:
    r = run(a, couple_repair=True)
    print(f"{a:>4.1f} {r['mfD']:>8.3f} {r['sfD']:>6.3f} {r['mR']:>7.1f} {r['sR']:>6.2f} {r['minR']:>6.1f} {r['Rstar']:>6.1f}  {regime(r)}")
