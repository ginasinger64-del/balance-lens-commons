import numpy as np

Rmax=100.0; eps=0.005

def payoffs(R,a): return np.array([5.0,12.0*(R/Rmax)**a,2.0])

def minR(a,g,delta,window,rho=0.20,T=10000,burn=6000):
    frac=np.array([1/3,1/3,1/3]); R=Rmax; win=[]; Rtr=[]
    for t in range(T):
        p=payoffs(R,a); win.append(p)
        if len(win)>window: win.pop(0)
        recent=np.mean(win,axis=0)
        R=min(Rmax,max(0.0,R+g*R*(1-R/Rmax)-delta*frac[1]*Rmax+rho*frac[2]*Rmax))
        avg=np.dot(frac,recent); frac=frac*(recent/avg)
        frac=(1-eps)*frac+eps*(1/3); frac/=frac.sum(); Rtr.append(R)
    return np.array(Rtr[burn:]).min()

def astar(g,delta,window,grid=np.arange(1.0,8.001,0.1),thr=1.0):
    for a in grid:
        if minR(a,g,delta,window)>thr: return round(float(a),2)
    return None

# diagonal: delta=g, so delta*lag = g*lag = P. Test if alpha* depends only on P.
Ps=[0.25,0.5,0.75,1.0,1.5,2.0]
lags=[5,10,20,40]
print("alpha* on the diagonal (delta=g). Each row = fixed product P = g*lag = delta*lag.")
print("If (g*lag, delta*lag) is the control variable, alpha* should be ~constant across a row.\n")
print(f"{'P':>5} | " + "  ".join(f"L={L:<2d}(g={'':<0})" for L in lags))
print(f"{'':>5} | " + "  ".join(f"L={L:<3d}" for L in lags) + "   [spread]")
print("-"*60)
for P in Ps:
    vals=[]; show=[]
    for L in lags:
        g=P/L
        a=astar(g,g,L)
        vals.append(a)
        show.append("None " if a is None else f"{a:>4.1f}")
    nums=[v for v in vals if v is not None]
    spread = f"{max(nums)-min(nums):.1f}" if len(nums)>1 else "-"
    print(f"{P:>5.2f} | " + "  ".join(show) + f"    [{spread}]")

print("\nResidual-dependence check at P=1.0 (does raw g matter beyond the product?):")
for L in [5,10,20,40]:
    g=1.0/L; a=astar(g,g,L)
    print(f"  g=delta={g:.4f}, L={L:2d}  ->  alpha* = {'None' if a is None else f'{a:.1f}'}")
