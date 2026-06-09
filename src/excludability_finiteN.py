# Finite-N Fermi confirmation of the excludability threshold. Drops mean-field AND replicator.
# r = private fraction of confiscated payoff to enforcers; (1-r) pooled to everyone.
import numpy as np
Rmax=100.0
def simulate(r, N=500, T=4000, burn=2000, Tsel=0.5, mu=0.005,
             a=2.0, g=0.20, delta=0.20, kappa=2.0, cost=1.0, seed=0):
    rng=np.random.default_rng(seed)
    strat=rng.integers(0,3,size=N); R=Rmax   # 0=C,1=D,2=E
    fDs=[]; Rs=[]; fEs=[]
    for t in range(T):
        nC=np.sum(strat==0); nD=np.sum(strat==1); nE=np.sum(strat==2)
        fC=nC/N; fD=nD/N; fE=nE/N
        sup=min(max(kappa*fE,0.0),1.0); base=12.0*(R/Rmax)**a
        loot=fD*base*sup
        pub=(1.0-r)*loot
        pC=5.0+pub; pD=base*(1.0-sup)+pub
        pE=(5.0-cost)+(r*loot/fE if fE>1e-9 else 0.0)+pub
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax+1.0   # recruitment to avoid R=0 absorbing trap
        R=min(Rmax,max(0.0,R))
        pay=np.array([pC,pD,pE]); mine=pay[strat]
        models=rng.integers(0,N,size=N); modelpay=pay[strat[models]]
        prob=1.0/(1.0+np.exp(-(modelpay-mine)/Tsel))
        adopt=rng.random(N)<prob
        new=strat.copy(); new[adopt]=strat[models][adopt]
        mm=rng.random(N)<mu; new[mm]=rng.integers(0,3,size=np.sum(mm))
        strat=new
        if t>=burn: fDs.append(fD); Rs.append(R); fEs.append(fE)
    return np.mean(fEs), np.mean(fDs), np.mean(Rs)

print("FINITE-N FERMI excludability sweep (N=500, 3 seeds). a=2,g=d=0.20,kappa=2,cost=1.")
print("Does the r* snap survive noise + non-replicator selection?\n")
print(f"{'r':>5} {'<fE>':>7} {'<fD>':>7} {'<R>':>7}   regime")
for r in [0.0,0.2,0.4,0.6,0.7,0.8,0.9,1.0]:
    rs=[simulate(r,seed=s) for s in range(3)]
    fE=np.mean([x[0] for x in rs]); fD=np.mean([x[1] for x in rs]); R=np.mean([x[2] for x in rs])
    if fE<0.05:   reg="collapse (enforcers dead)"
    elif fD>0.15: reg="coexistence"
    else:         reg="stable protection"
    print(f"{r:>5.1f} {fE:>7.3f} {fD:>7.3f} {R:>7.1f}   {reg}")
