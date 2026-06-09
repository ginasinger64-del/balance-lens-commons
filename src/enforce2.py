# Self-funding enforcement: confiscated defect payoff is redistributed to enforcers.
# payoff_E = (5 - cost) + redist * (total_loot / fE);  loot = fD * (suppressed defect payoff)
Rmax=100.0; eps=0.005

def run(a,g,delta,window,kappa,cost,redist):
    T=200*window; burn=T//2
    fC=fD=fE=1.0/3.0; R=Rmax
    win=[]; sC=sD=sE=0.0; Rmin=1e9; sfE=sfD=0.0; ss=0.0; nstat=0
    fDhist=[]
    for t in range(T):
        sup=min(max(kappa*fE,0.0),1.0)            # fraction of defect payoff confiscated
        base_pD=12.0*(R/Rmax)**a
        pD=base_pD*(1.0-sup)
        loot=fD*base_pD*sup                        # total confiscated this turn
        reward=redist*loot/fE if fE>1e-9 else 0.0
        pC=5.0; pE=(5.0-cost)+reward
        win.append((pC,pD,pE)); sC+=pC; sD+=pD; sE+=pE
        if len(win)>window:
            oC,oD,oE=win.pop(0); sC-=oC; sD-=oD; sE-=oE
        n=len(win); rC=sC/n; rD=sD/n; rE=sE/n
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax         # no restoration
        if R<0.0: R=0.0
        elif R>Rmax: R=Rmax
        avg=fC*rC+fD*rD+fE*rE
        fC=fC*rC/avg; fD=fD*rD/avg; fE=fE*rE/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fE=(1-eps)*fE+eps/3
        s=fC+fD+fE; fC/=s; fD/=s; fE/=s
        if t>=burn:
            if R<Rmin: Rmin=R
            sfE+=fE; sfD+=fD; nstat+=1; fDhist.append(fD)
    import statistics
    sdfD=statistics.pstdev(fDhist) if len(fDhist)>1 else 0.0
    return Rmin, sfE/nstat, sfD/nstat, sdfD

def astar(g,delta,window,kappa,cost,redist,thr=1.0):
    a=0.5
    while a<=8.001:
        if run(a,g,delta,window,kappa,cost,redist)[0]>thr: return round(a,2)
        a+=0.1
    return None

g=d=0.20; L=5; kappa=2.0
print("Self-funding enforcement, cell P=1.0 L=5, kappa=2. Unfunded (redist=0) died at cost>=0.5.")
print("Does funding hold protection at positive cost? alpha* low + fE up + fD low = yes.\n")
for redist in [0.0,0.5,1.0]:
    print(f"redist = {redist}")
    print(f"{'cost':>6} {'alpha*':>8} {'<fE>':>7} {'<fD>':>7} {'sd_fD':>7}")
    for c in [0.5,1.0,2.0,4.0]:
        a=astar(g,d,L,kappa,c,redist)
        if a is not None: _,fE,fD,sd=run(a,g,d,L,kappa,c,redist)
        else: fE=fD=sd=None
        astr='None' if a is None else f'{a:.2f}'
        fEs='' if fE is None else f'{fE:.3f}'; fDs='' if fD is None else f'{fD:.3f}'; sds='' if sd is None else f'{sd:.3f}'
        print(f"{c:>6.1f} {astr:>8} {fEs:>7} {fDs:>7} {sds:>7}")
    print()
