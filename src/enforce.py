# Enforcement class: strategy E suppresses defector payoff (x by (1-kappa*fE)), costs itself
# (payoff_E = 5 - cost), and does NOT restore the stock. Strategies: C, D, E.
Rmax=100.0; eps=0.005

def run(a,g,delta,window,kappa,cost):
    T=200*window; burn=T//2
    fC=fD=fE=1.0/3.0; R=Rmax
    win=[]; sC=sD=sE=0.0; Rmin=1e9; sfE=sfD=0.0; nstat=0
    for t in range(T):
        supp=max(0.0,1.0-kappa*fE)              # enforcement suppresses defect payoff
        pC=5.0; pD=12.0*(R/Rmax)**a*supp; pE=5.0-cost
        win.append((pC,pD,pE)); sC+=pC; sD+=pD; sE+=pE
        if len(win)>window:
            oC,oD,oE=win.pop(0); sC-=oC; sD-=oD; sE-=oE
        n=len(win); rC=sC/n; rD=sD/n; rE=sE/n
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax       # NO restoration term
        if R<0.0: R=0.0
        elif R>Rmax: R=Rmax
        avg=fC*rC+fD*rD+fE*rE
        fC=fC*rC/avg; fD=fD*rD/avg; fE=fE*rE/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fE=(1-eps)*fE+eps/3
        s=fC+fD+fE; fC/=s; fD/=s; fE/=s
        if t>=burn:
            if R<Rmin: Rmin=R
            sfE+=fE; sfD+=fD; nstat+=1
    return Rmin, sfE/nstat, sfD/nstat

def astar(g,delta,window,kappa,cost,thr=1.0):
    a=0.5
    while a<=8.001:
        if run(a,g,delta,window,kappa,cost)[0]>thr: return round(a,2)
        a+=0.1
    return None

g=d=0.20; L=5  # same cell as repair tests. baseline (no intervention) alpha* ~ 2.70.
print("Cell P=1.0 L=5. Repair baseline: NO protective regime (inert or subsidy).")
print("Enforcement reduces defect payoff x(1-kappa*fE), no restoration.\n")

print("E1  FREE enforcement (cost=0): does enforcement-class protect? alpha* DOWN = yes.")
print(f"{'kappa':>6} {'alpha*':>8} {'<fE>':>7} {'<fD>':>7}")
for k in [0.0,0.5,1.0,2.0,4.0]:
    a=astar(g,d,L,k,0.0); 
    if a is not None: _,fE,fD=run(a,g,d,L,k,0.0)
    else: fE=fD=None
    astr='None' if a is None else f'{a:.2f}'
    print(f"{k:>6.1f} {astr:>8} {('' if fE is None else f'{fE:.3f}'):>7} {('' if fD is None else f'{fD:.3f}'):>7}")
print()

print("E2  COSTLY enforcement (kappa=2 fixed): sweep policing cost. When do enforcers die?")
print(f"{'cost':>6} {'alpha*':>8} {'<fE>':>7} {'<fD>':>7}")
for c in [0.0,0.5,1.0,2.0,3.0]:
    a=astar(g,d,L,2.0,c)
    if a is not None: _,fE,fD=run(a,g,d,L,2.0,c)
    else: fE=fD=None
    astr='None' if a is None else f'{a:.2f}'
    print(f"{c:>6.1f} {astr:>8} {('' if fE is None else f'{fE:.3f}'):>7} {('' if fD is None else f'{fD:.3f}'):>7}")
