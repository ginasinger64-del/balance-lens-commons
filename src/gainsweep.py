import numpy as np
Rmax=100.0; eps=0.005

def payoffs(R,a): return np.array([5.0,12.0*(R/Rmax)**a,2.0])

def minR(a,g,delta,window,c,g_ref=0.15,rho=0.20,T=20000,burn=10000):
    eta = c*(g/g_ref)
    frac=np.array([1/3,1/3,1/3]); R=Rmax; win=[]; Rtr=[]
    for t in range(T):
        p=payoffs(R,a); win.append(p)
        if len(win)>window: win.pop(0)
        recent=np.mean(win,axis=0)
        R=min(Rmax,max(0.0,R+g*R*(1-R/Rmax)-delta*frac[1]*Rmax+rho*frac[2]*Rmax))
        avg=np.dot(frac,recent)
        frac=frac*(recent/avg)**eta
        frac=(1-eps)*frac+eps*(1/3); frac/=frac.sum(); Rtr.append(R)
    return np.array(Rtr[burn:]).min()

def astar(g,delta,window,c,grid=np.arange(1.0,8.001,0.1),thr=1.0):
    for a in grid:
        if minR(a,g,delta,window,c)>thr: return round(float(a),2)
    return None

P=1.5; Ls=[5,10,20,40]
print(f"P={P} gain sweep: eta = c*(g/g_ref), g_ref=0.15.  orig(c=inf-equiv eta=1): 3.9 5.3 6.5 5.9 (HUMP)\n")
print(f"{'c':>6}   eta@L5  | " + "  ".join(f"L={L:<3d}" for L in Ls) + "   shape")
print("-"*60)
for c in [0.25,0.5,0.75,1.0]:
    row=[]; etaL5 = c*(0.30/0.15)
    for L in Ls:
        g=P/L; a=astar(g,g,L,c)
        row.append(" None" if a is None else f"{a:>4.1f}")
    nums=[float(x) for x in row if x.strip()!="None"]
    n_none = row.count(" None")
    shape = "monotone" if (nums==sorted(nums) or nums==sorted(nums,reverse=True)) else "HUMP"
    if n_none: shape += f" ({n_none} None)"
    print(f"{c:>6.2f}   {etaL5:>5.2f}   | " + "  ".join(row) + f"   {shape}")
