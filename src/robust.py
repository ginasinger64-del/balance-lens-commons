# KILL-TEST: finite-N agent-based, Fermi (pairwise imitation) update. Both mean-field AND
# replicator are dropped. Same commons. Does the intervention hierarchy survive?
import numpy as np
Rmax=100.0

def simulate(mode, N=300, T=4000, burn=2000, Tsel=0.5, mu=0.005,
             a=2.0, g=0.20, delta=0.20, kappa=2.0, cost=1.0, b=8.0, rho=0.20,
             redist=1.0, seed=0):
    # strategies: 0=C, 1=D, 2=third (R for repair, E for enforce)
    rng=np.random.default_rng(seed)
    strat=rng.integers(0,3,size=N); R=Rmax
    fDs=[]; Rs=[]; f2s=[]
    for t in range(T):
        nC=np.sum(strat==0); nD=np.sum(strat==1); n2=np.sum(strat==2)
        fC=nC/N; fD=nD/N; f2=n2/N
        # payoffs (frozen for this generation)
        pC=5.0; pD=12.0*(R/Rmax)**a
        if mode=='repair':
            p2=2.0+b*(1.0-R/Rmax); restore=rho*f2*Rmax
        elif mode=='enforce':
            sup=min(max(kappa*f2,0.0),1.0); pD=pD*(1.0-sup); p2=5.0-cost; restore=0.0
        elif mode=='selffund':
            sup=min(max(kappa*f2,0.0),1.0); base=12.0*(R/Rmax)**a
            loot=fD*base*sup; pD=base*(1.0-sup)
            p2=(5.0-cost)+(redist*loot/f2 if f2>1e-9 else 0.0); restore=0.0
        else: # baseline C/D only (third strat treated as C)
            p2=5.0; restore=0.0
        # resource update
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax+restore
        R=min(Rmax,max(0.0,R))
        # Fermi synchronous update: each agent picks a random model, imitates w.p. Fermi
        pay=np.array([pC,pD,p2])
        mine=pay[strat]
        models=rng.integers(0,N,size=N)
        modelpay=pay[strat[models]]
        prob=1.0/(1.0+np.exp(-(modelpay-mine)/Tsel))
        adopt=rng.random(N)<prob
        new=strat.copy(); new[adopt]=strat[models][adopt]
        # mutation
        mmask=rng.random(N)<mu; new[mmask]=rng.integers(0,3,size=np.sum(mmask))
        strat=new
        if t>=burn: fDs.append(fD); Rs.append(R); f2s.append(f2)
    return np.mean(fDs), np.mean(Rs), np.min(Rs), np.mean(f2s)

conds=[("baseline C/D","baseline"),
       ("repair b=8","repair"),
       ("enforce unfunded cost=1","enforce"),
       ("self-funded cost=1","selffund")]
print("FINITE-N (N=300) + FERMI imitation. a=2.0, g=delta=0.20, kappa=2, cost=1, redist=1.")
print("Mean-field predicts: repair high fD (subsidy/no protect); unfunded enforce DEAD f2,")
print("high fD; self-funded LOW fD, high f2 (protected). 3 seeds averaged.\n")
print(f"{'condition':<26} {'mean_fD':>8} {'mean_R':>8} {'min_R':>7} {'mean_f2':>8}")
for label,mode in conds:
    rs=[simulate(mode,seed=s) for s in range(3)]
    fD=np.mean([r[0] for r in rs]); mR=np.mean([r[1] for r in rs])
    mnR=np.mean([r[2] for r in rs]); f2=np.mean([r[3] for r in rs])
    print(f"{label:<26} {fD:>8.3f} {mR:>8.1f} {mnR:>7.1f} {f2:>8.3f}")
