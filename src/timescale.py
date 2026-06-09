import numpy as np
Rmax=100.0; eps=0.005

def payoffs(R,a): return np.array([5.0,12.0*(R/Rmax)**a,2.0])

def metrics(a,g,delta,window,scale_eta=False,g_ref=0.15,rho=0.20,T=20000,burn=10000):
    # scale_eta=True: replicator step exponent eta = g/g_ref, so selection speed
    #   scales with resource speed (third clock tied to first). eta=1 at g=g_ref.
    # scale_eta=False: eta=1 always (original, unscaled per-turn replicator step).
    eta = (g/g_ref) if scale_eta else 1.0
    frac=np.array([1/3,1/3,1/3]); R=Rmax; win=[]; Rtr=[]
    for t in range(T):
        p=payoffs(R,a); win.append(p)
        if len(win)>window: win.pop(0)
        recent=np.mean(win,axis=0)
        R=min(Rmax,max(0.0,R+g*R*(1-R/Rmax)-delta*frac[1]*Rmax+rho*frac[2]*Rmax))
        avg=np.dot(frac,recent)
        frac=frac*(recent/avg)**eta          # <-- step size eta
        frac=(1-eps)*frac+eps*(1/3); frac/=frac.sum(); Rtr.append(R)
    Rt=np.array(Rtr[burn:])
    return Rt.min()

def astar(g,delta,window,scale_eta,grid=np.arange(1.0,8.001,0.1),thr=1.0):
    for a in grid:
        if metrics(a,g,delta,window,scale_eta=scale_eta)>thr: return round(float(a),2)
    return None

P=1.5; Ls=[5,10,20,40]
print(f"P={P}. Does tying the replicator step to g (eta=g/0.15) remove the hump?\n")
print(f"{'mode':<26} " + "  ".join(f"L={L:<3d}" for L in Ls))
print("-"*56)
for label,se in [("eta=1  (unscaled, orig)",False),("eta=g/g_ref (3 clocks tied)",True)]:
    row=[]
    for L in Ls:
        g=P/L; a=astar(g,g,L,se)
        row.append(" None" if a is None else f"{a:>4.1f}")
    nums=[float(x) for x in row if x.strip()!="None"]
    shape="monotone" if (nums==sorted(nums) or nums==sorted(nums,reverse=True)) else "HUMP"
    print(f"{label:<26} " + "  ".join(row) + f"   [{shape}]")

# also check the fixed-P residual at P=1.0 under both modes
print(f"\nFixed-P residual check at P=1.0 (orig drifted 2.7,2.8,2.6,2.0):")
print(f"{'mode':<26} " + "  ".join(f"L={L:<3d}" for L in Ls))
print("-"*56)
for label,se in [("eta=1  (unscaled, orig)",False),("eta=g/g_ref (3 clocks tied)",True)]:
    row=[]
    for L in Ls:
        g=1.0/L; a=astar(g,g,L,se)
        row.append(" None" if a is None else f"{a:>4.1f}")
    print(f"{label:<26} " + "  ".join(row))
