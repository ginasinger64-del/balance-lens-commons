import numpy as np

Rmax = 100.0
eps  = 0.005
T    = 6000
burn = 3000

def payoffs(R, alpha):
    return np.array([5.0, 12.0*(R/Rmax)**alpha, 2.0])  # C, D, R(flat)

def run(alpha, g, delta, window, rho=0.20):
    frac = np.array([1/3,1/3,1/3]); R = Rmax; win=[]
    R_tr=[]
    for t in range(T):
        p = payoffs(R, alpha)
        win.append(p)
        if len(win) > window: win.pop(0)
        recent = np.mean(win, axis=0)
        regen   = g*R*(1-R/Rmax)
        harvest = delta*frac[1]*Rmax
        restore = rho*frac[2]*Rmax
        R = min(Rmax, max(0.0, R + regen - harvest + restore))
        avg = np.dot(frac, recent)
        frac = frac*(recent/avg)
        frac = (1-eps)*frac + eps*(1/3); frac /= frac.sum()
        R_tr.append(R)
    Rt = np.array(R_tr[burn:])
    return Rt.min()

def alpha_star(g, delta, window, grid=np.arange(1.0, 8.01, 0.25), thr=1.0):
    # fully deterministic model -> exact given grid
    for a in grid:
        if run(a, g, delta, window) > thr:
            return float(a)
    return None

cells = [(0.05,0.05),(0.10,0.10),(0.20,0.20),(0.30,0.30)]
windows = [1,3,5,10,20]

print("alpha*(lag)  — flat repair, floor-liftoff threshold min_R>1.0")
print(f"{'g':>5} {'delta':>6} | " + " ".join(f"L={w:<2d}" for w in windows))
print("-"*52)
for (g,d) in cells:
    row=[]
    for w in windows:
        a=alpha_star(g,d,w)
        row.append(" None" if a is None else f"{a:>4.2f}")
    print(f"{g:>5.2f} {d:>6.2f} | " + "  ".join(row))

print()
print("COLLAPSE TEST: does (delta*lag, g*lag) control alpha*?")
print("If yes, these pairs should give the SAME alpha*:")
tests = [
    ("g=.10 d=.10 L=10", 0.10,0.10,10),
    ("g=.20 d=.20 L=5 ", 0.20,0.20,5),
    ("--",None,None,None),
    ("g=.05 d=.05 L=20", 0.05,0.05,20),
    ("g=.10 d=.10 L=10", 0.10,0.10,10),
    ("g=.20 d=.20 L=5 ", 0.20,0.20,5),
    ("--",None,None,None),
    ("g=.05 d=.05 L=10", 0.05,0.05,10),
    ("g=.10 d=.10 L=5 ", 0.10,0.10,5),
]
for label,g,d,w in tests:
    if g is None: print("  "+"-"*20); continue
    a=alpha_star(g,d,w)
    print(f"  {label} (d*L={d*w:.2f}, g*L={g*w:.2f}) -> alpha* = {'None' if a is None else f'{a:.2f}'}")
