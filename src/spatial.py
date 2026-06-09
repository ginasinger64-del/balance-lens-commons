import numpy as np
Rmax=100.0

def neigh_sum(A):  # sum over 8 Moore neighbors, periodic
    s=np.zeros_like(A)
    for di in(-1,0,1):
        for dj in(-1,0,1):
            if di==0 and dj==0: continue
            s+=np.roll(np.roll(A,di,0),dj,1)
    return s

def lap(A):        # von Neumann laplacian, periodic
    return (np.roll(A,1,0)+np.roll(A,-1,0)+np.roll(A,1,1)+np.roll(A,-1,1)-4*A)

def simulate(mode,N=50,T=1500,burn=750,Tsel=0.5,mu=0.005,
             a=2.0,g=0.30,delta=0.10,rho=0.15,Ddiff=0.15,s0=0.3,
             kappa=2.0,cost=1.0,redist=1.0,b=8.0,seed=0):
    rng=np.random.default_rng(seed)
    s=rng.integers(0,3,size=(N,N)); R=np.full((N,N),Rmax)
    # 8 neighbor offsets for imitation pick
    offs=[(di,dj) for di in(-1,0,1) for dj in(-1,0,1) if not(di==0 and dj==0)]
    acc=dict(fD=[],fR=[],f2=[],R=[],RatD=[],RatC=[],assort=[])
    for t in range(T):
        D=(s==1).astype(float); C=(s==0).astype(float); E=(s==2).astype(float)
        locE=neigh_sum(E)/8.0; locD=neigh_sum(D)/8.0
        base_pD=12.0*(R/Rmax)**a
        pC=np.full((N,N),5.0)
        if mode=='repair':
            pD=base_pD; p2=2.0+b*(1.0-R/Rmax); restore=rho*Rmax*E
        elif mode=='enforce':
            sup=np.minimum(kappa*locE,1.0); pD=base_pD*(1.0-sup); p2=np.full((N,N),5.0-cost); restore=0.0
        elif mode=='selffund':
            sup=np.minimum(kappa*locE,1.0); pD=base_pD*(1.0-sup)
            loot=locD*base_pD*sup
            reward=np.where(locE>1e-6, redist*loot/np.maximum(locE,1e-6), 0.0)
            p2=(5.0-cost)+reward; restore=0.0
        else:  # baseline: third strat behaves like C
            pD=base_pD; p2=np.full((N,N),5.0); restore=0.0
        pay=np.where(s==0,pC,np.where(s==1,pD,p2))
        # resource: regen - local depletion(D) + restore(R) + diffusion + recruitment
        R=R+g*R*(1.0-R/Rmax)-delta*Rmax*D+restore+Ddiff*Rmax*lap(R)/Rmax*0+Ddiff*lap(R)+s0
        np.clip(R,0.0,Rmax,out=R)
        # local Fermi imitation vs a random Moore neighbor
        k=rng.integers(0,8,size=(N,N))
        ns=np.empty((N,N),dtype=s.dtype); npay=np.empty((N,N))
        for idx,(di,dj) in enumerate(offs):
            m=(k==idx)
            ns[m]=np.roll(np.roll(s,di,0),dj,1)[m]
            npay[m]=np.roll(np.roll(pay,di,0),dj,1)[m]
        prob=1.0/(1.0+np.exp(-(npay-pay)/Tsel))
        adopt=rng.random((N,N))<prob
        s=np.where(adopt,ns,s)
        mm=rng.random((N,N))<mu; s=np.where(mm,rng.integers(0,3,size=(N,N)),s)
        if t>=burn:
            D=(s==1); C=(s==0)
            acc['fD'].append(D.mean()); acc['f2'].append((s==2).mean()); acc['R'].append(R.mean())
            acc['RatD'].append(R[D].mean() if D.any() else np.nan)
            acc['RatC'].append(R[C].mean() if C.any() else np.nan)
            same=neigh_sum((s[:,:,None]==np.arange(3)).astype(float)[...,0]*0)  # placeholder
            # assortment: fraction of 8 neighbors sharing own strategy
            sm=np.zeros((N,N))
            for di,dj in offs: sm+=(np.roll(np.roll(s,di,0),dj,1)==s)
            acc['assort'].append((sm/8.0).mean())
    f=lambda k:np.nanmean(acc[k])
    return f('fD'),f('R'),f('f2'),f('RatD'),f('RatC'),f('assort')

conds=[("baseline C/D","baseline"),("repair b=8","repair"),
       ("unfunded enforce c=1","enforce"),("self-funded c=1","selffund")]
print("SPATIAL 50x50 lattice, local resource + diffusion, local Fermi imitation. 2 seeds.")
print("a=2, g=0.30, delta=0.10(local), rho=0.15, Ddiff=0.15, kappa=2, cost=1, redist=1.\n")
print(f"{'condition':<22}{'fD':>7}{'meanR':>8}{'f2':>7}{'R@D':>7}{'R@C':>7}{'assort':>8}")
for label,mode in conds:
    rs=[simulate(mode,seed=sd) for sd in range(2)]
    m=np.mean(rs,axis=0)
    print(f"{label:<22}{m[0]:>7.3f}{m[1]:>8.1f}{m[2]:>7.3f}{m[3]:>7.1f}{m[4]:>7.1f}{m[5]:>8.3f}")
print("\nrandom-mix assortment baseline ~0.33 (3 strategies). higher => clustering.")
print("R@D << R@C => defectors sit on depleted patches (spatial self-limiting).")
