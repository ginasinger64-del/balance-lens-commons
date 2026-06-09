# Spatial-lattice confirmation of the excludability control parameter.
# Local resource patches + diffusion + LOCAL Fermi imitation. r = private fraction of
# locally-confiscated payoff to neighborhood enforcers; (1-r) pooled to the neighborhood.
import numpy as np
Rmax=100.0
def neigh_sum(A):
    s=np.zeros_like(A)
    for di in(-1,0,1):
        for dj in(-1,0,1):
            if di==0 and dj==0: continue
            s+=np.roll(np.roll(A,di,0),dj,1)
    return s
def lap(A):
    return np.roll(A,1,0)+np.roll(A,-1,0)+np.roll(A,1,1)+np.roll(A,-1,1)-4*A

def simulate(r,N=50,T=1500,burn=750,Tsel=0.5,mu=0.005,
             a=2.0,g=0.30,delta=0.10,Ddiff=0.15,s0=0.3,kappa=2.0,cost=1.0,seed=0):
    rng=np.random.default_rng(seed)
    s=rng.integers(0,3,size=(N,N)); R=np.full((N,N),Rmax)
    offs=[(di,dj) for di in(-1,0,1) for dj in(-1,0,1) if not(di==0 and dj==0)]
    fE_acc=[]; fD_acc=[]; R_acc=[]
    for t in range(T):
        D=(s==1).astype(float); E=(s==2).astype(float)
        locE=neigh_sum(E)/8.0; locD=neigh_sum(D)/8.0
        base=12.0*(R/Rmax)**a
        sup=np.minimum(kappa*locE,1.0)
        loot=locD*base*sup
        pub=(1.0-r)*loot
        reward=np.where(locE>1e-6, r*loot/np.maximum(locE,1e-6), 0.0)
        pC=5.0+pub; pD=base*(1.0-sup)+pub; pE=(5.0-cost)+reward+pub
        R=R+g*R*(1.0-R/Rmax)-delta*Rmax*D+Ddiff*lap(R)+s0
        np.clip(R,0.0,Rmax,out=R)
        pay=np.where(s==0,pC,np.where(s==1,pD,pE))
        k=rng.integers(0,8,size=(N,N)); ns=np.empty_like(s); npay=np.empty((N,N))
        for idx,(di,dj) in enumerate(offs):
            m=(k==idx)
            ns[m]=np.roll(np.roll(s,di,0),dj,1)[m]
            npay[m]=np.roll(np.roll(pay,di,0),dj,1)[m]
        prob=1.0/(1.0+np.exp(-(npay-pay)/Tsel))
        adopt=rng.random((N,N))<prob
        s=np.where(adopt,ns,s)
        mm=rng.random((N,N))<mu; s=np.where(mm,rng.integers(0,3,size=(N,N)),s)
        if t>=burn:
            fE_acc.append((s==2).mean()); fD_acc.append((s==1).mean()); R_acc.append(R.mean())
    return np.mean(fE_acc), np.mean(fD_acc), np.mean(R_acc)

print("SPATIAL LATTICE excludability sweep (50x50, 2 seeds). Local resource+diffusion, local Fermi.")
print("Does the directional dependence (more private r -> more enforcement) survive a third ecology?\n")
print(f"{'r':>5} {'<fE>':>7} {'<fD>':>7} {'<R>':>7}")
for r in [0.0,0.2,0.4,0.6,0.8,1.0]:
    rs=[simulate(r,seed=sd) for sd in range(2)]
    fE=np.mean([x[0] for x in rs]); fD=np.mean([x[1] for x in rs]); R=np.mean([x[2] for x in rs])
    print(f"{r:>5.1f} {fE:>7.3f} {fD:>7.3f} {R:>7.1f}")
