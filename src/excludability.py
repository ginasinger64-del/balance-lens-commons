# EXCLUDABILITY SWEEP: r = fraction of confiscated payoff routed PRIVATELY to enforcers.
# r=0 -> pooled/unfunded (public), r=1 -> fully self-funded (private). Same suppression,
# same total extraction; only the private fraction changes. Is there a critical r*?
import numpy as np
Rmax=100.0; eps=0.005

def run(a,g,delta,window,kappa,cost,r):
    T=200*window; burn=T//2
    fC=fD=fE=1/3; R=Rmax; win=[]; Rmin=1e9; sfE=sfD=sR=0.0; n=0
    for t in range(T):
        sup=min(max(kappa*fE,0.0),1.0); base=12.0*(R/Rmax)**a
        loot=fD*base*sup
        pC=5.0; pD=base*(1.0-sup)
        # private share r*loot to enforcers; public share (1-r)*loot split over everyone
        pub=(1.0-r)*loot
        pE=(5.0-cost) + (r*loot/fE if fE>1e-9 else 0.0) + pub
        pCc=pC+pub; pDd=pD+pub
        win.append((pCc,pDd,pE)); sC=sum(w[0] for w in win[-window:]) if False else None
        if len(win)>window: win.pop(0)
        m=len(win)
        rC=sum(w[0] for w in win)/m; rD=sum(w[1] for w in win)/m; rE=sum(w[2] for w in win)/m
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax; R=min(Rmax,max(0.0,R))
        avg=fC*rC+fD*rD+fE*rE
        fC=fC*rC/avg; fD=fD*rD/avg; fE=fE*rE/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fE=(1-eps)*fE+eps/3
        s=fC+fD+fE; fC/=s; fD/=s; fE/=s
        if t>=burn:
            if R<Rmin: Rmin=R
            sfE+=fE; sfD+=fD; sR+=R; n+=1
    return Rmin, sfE/n, sfD/n, sR/n

def astar(g,delta,window,kappa,cost,r,thr=1.0):
    a=0.5
    while a<=8.001:
        if run(a,g,delta,window,kappa,cost,r)[0]>thr: return round(a,2)
        a+=0.1
    return None

g=d=0.20; L=5; kappa=2.0; cost=1.0
print("EXCLUDABILITY SWEEP (mean-field). cell P=1.0 L=5, kappa=2, cost=1.")
print("r = private fraction of confiscated payoff. Same suppression & extraction throughout.\n")
print(f"{'r':>5} {'alpha*':>8} {'<fE>':>7} {'<fD>':>7} {'<R>':>7}   regime")
prev_state=None
for r in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
    a=astar(g,d,L,kappa,cost,r)
    _,fE,fD,R=run(2.0,g,d,L,kappa,cost,r)   # diagnostics at fixed a=2.0
    if fE<0.05:        reg="collapse (enforcers dead)"
    elif fD>0.12:      reg="coexistence"
    else:              reg="stable protection"
    astr="None" if a is None else f"{a:.2f}"
    print(f"{r:>5.1f} {astr:>8} {fE:>7.3f} {fD:>7.3f} {R:>7.1f}   {reg}")
print("\nLook for: collapse -> coexistence -> stable protection as r rises, and the r* where")
print("enforcers first persist (fE lifts off the floor). That r* is the excludability threshold.")
