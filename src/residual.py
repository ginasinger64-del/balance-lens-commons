import numpy as np
Rmax=100.0; eps=0.005

def payoffs(R,a): return np.array([5.0,12.0*(R/Rmax)**a,2.0])

def minR(a,g,delta,window,rho=0.20,T=None,burn=None):
    # scale run length with the slow timescale (1/g ~ L) so high-L cells equilibrate
    if T is None: T=max(20000,int(300*window)); burn=T//2
    frac=np.array([1/3,1/3,1/3]); R=Rmax; win=[]; Rtr=[]
    for t in range(T):
        p=payoffs(R,a); win.append(p)
        if len(win)>window: win.pop(0)
        recent=np.mean(win,axis=0)
        R=min(Rmax,max(0.0,R+g*R*(1-R/Rmax)-delta*frac[1]*Rmax+rho*frac[2]*Rmax))
        avg=np.dot(frac,recent); frac=frac*(recent/avg)
        frac=(1-eps)*frac+eps*(1/3); frac/=frac.sum(); Rtr.append(R)
    return np.array(Rtr[burn:]).min()

def astar(g,delta,window,grid=np.arange(1.0,8.001,0.05),thr=1.0):
    for a in grid:
        if minR(a,g,delta,window)>thr: return round(float(a),3)
    return None

print("Fixed-P residual: extend L at fixed P (g=delta=P/L). Larger L = smaller g =")
print("smaller per-turn resource step. If alpha* CONVERGES -> residual is discretization")
print("(numerical, vanishes in continuum limit). If it keeps moving -> a real 2nd group.\n")
for P in [1.0, 0.5]:
    print(f"P = {P}")
    print(f"{'L':>5} {'g=d':>8} {'alpha*':>8} {'decrement':>10}")
    prev=None
    for L in [5,10,20,40,80,160]:
        g=P/L; a=astar(g,g,L)
        dec = "" if (prev is None or a is None) else f"{a-prev:+.3f}"
        astr = "None" if a is None else f"{a:.3f}"
        print(f"{L:>5} {g:>8.5f} {astr:>8} {dec:>10}")
        prev=a
    print()
