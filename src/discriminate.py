# Mechanism discrimination. Same suppression (E reduces D payoff x(1-kappa*fE)), same total
# confiscated loot L = fD*base_pD*sup. Vary ONLY where the loot goes:
#   unfunded   : vanishes                      (Result 5: collapses)
#   selffund   : to enforcers only, per-capita (Result 6: survives)  [private incentive]
#   pooled_all : to EVERYONE equally (incl. D) [Hyp A test: subsidy?]
#   pooled_CE  : to C and E equally (not D)     [isolates: private vs merely-not-to-D]
Rmax=100.0; eps=0.005

def run(a,g,delta,window,kappa,cost,scheme,redist=1.0):
    T=200*window; burn=T//2
    fC=fD=fE=1/3; R=Rmax
    win=[]; sC=sD=sE=0.0; Rmin=1e9; sfE=sfD=0.0; n=0
    for t in range(T):
        sup=min(max(kappa*fE,0.0),1.0); base=12.0*(R/Rmax)**a
        L=fD*base*sup                              # total confiscated (per-capita units)
        pC=5.0; pD=base*(1.0-sup); pE=5.0-cost
        if scheme=='selffund':
            pE += redist*L/fE if fE>1e-9 else 0.0
        elif scheme=='pooled_all':
            share=redist*L                         # total L*N split over N -> L each
            pC+=share; pD+=share; pE+=share
        elif scheme=='pooled_CE':
            denom=fC+fE
            share=redist*L/denom if denom>1e-9 else 0.0
            pC+=share; pE+=share
        # 'unfunded': nothing
        win.append((pC,pD,pE)); sC+=pC; sD+=pD; sE+=pE
        if len(win)>window:
            oC,oD,oE=win.pop(0); sC-=oC; sD-=oD; sE-=oE
        m=len(win); rC=sC/m; rD=sD/m; rE=sE/m
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax
        R=min(Rmax,max(0.0,R))
        avg=fC*rC+fD*rD+fE*rE
        fC=fC*rC/avg; fD=fD*rD/avg; fE=fE*rE/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fE=(1-eps)*fE+eps/3
        s=fC+fD+fE; fC/=s; fD/=s; fE/=s
        if t>=burn:
            if R<Rmin: Rmin=R
            sfE+=fE; sfD+=fD; n+=1
    return Rmin, sfE/n, sfD/n

g=d=0.20; L=5; kappa=2.0; cost=1.0
print("MECHANISM DISCRIMINATION. cell P=1.0 L=5, kappa=2, cost=1, redist=1.")
print("Same suppression + same total loot; only the RECIPIENT differs.\n")
print(f"{'scheme':<14}{'min_R':>7}{'<fE>':>7}{'<fD>':>7}   reading")
for scheme in ['unfunded','selffund','pooled_all','pooled_CE']:
    mnR,fE,fD=run(2.0,g,d,L,kappa,cost,scheme)
    tag=''
    if fE>0.15 and fD<0.12: tag='ENFORCERS LIVE, protected'
    elif fE<0.05: tag='enforcers DEAD, no protection'
    else: tag='partial'
    print(f"{scheme:<14}{mnR:>7.1f}{fE:>7.3f}{fD:>7.3f}   {tag}")
print()
print("Predictions:  C(funding-align): selffund LIVES, both pooled DIE.")
print("              B(cause/symptom): all that suppress should protect (needs E to persist).")
print("              A(resource-coupl): pooled_all worse fD than pooled_CE (loot subsidizes D).")
