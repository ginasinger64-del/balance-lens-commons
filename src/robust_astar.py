import numpy as np
Rmax=100.0; eps=0.005

def payoffs(R,a): return np.array([5.0,12.0*(R/Rmax)**a,2.0])

def metrics(a,g,delta,window,rho=0.20,T=20000,burn=10000):
    # longer run + bigger burn to de-noise tail statistics
    frac=np.array([1/3,1/3,1/3]); R=Rmax; win=[]; Rtr=[]
    for t in range(T):
        p=payoffs(R,a); win.append(p)
        if len(win)>window: win.pop(0)
        recent=np.mean(win,axis=0)
        R=min(Rmax,max(0.0,R+g*R*(1-R/Rmax)-delta*frac[1]*Rmax+rho*frac[2]*Rmax))
        avg=np.dot(frac,recent); frac=frac*(recent/avg)
        frac=(1-eps)*frac+eps*(1/3); frac/=frac.sum(); Rtr.append(R)
    Rt=np.array(Rtr[burn:])
    return dict(minR=Rt.min(), p5=np.percentile(Rt,5),
                frac_below2=np.mean(Rt<2.0), meanR=Rt.mean())

def astar(g,delta,window,crit,grid=np.arange(1.0,8.001,0.1)):
    for a in grid:
        if crit(metrics(a,g,delta,window)): return round(float(a),2)
    return None

# three criteria for "floor protected"
crits = {
    "min_R>1   (original)" : lambda m: m['minR']>1.0,
    "p5_R>5    (robust)"   : lambda m: m['p5']>5.0,
    "<2%% time below 2"     : lambda m: m['frac_below2']<0.02,
}
P=1.5
print(f"P={P}: does the alpha* hump at L=20 survive a more robust criterion?\n")
print(f"{'criterion':<22} " + "  ".join(f"L={L:<3d}" for L in [5,10,20,40]))
print("-"*52)
for name,crit in crits.items():
    row=[]
    for L in [5,10,20,40]:
        g=P/L; a=astar(g,g,L,crit)
        row.append(" None" if a is None else f"{a:>4.1f}")
    # flag monotone vs hump
    nums=[float(x) for x in row if x.strip()!="None"]
    shape = "monotone" if (nums==sorted(nums) or nums==sorted(nums,reverse=True)) else "HUMP"
    print(f"{name:<22} " + "  ".join(row) + f"   [{shape}]")
