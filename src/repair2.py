Rmax=100.0; eps=0.005

# design: how repair's restoration is gated.
#  'none'  : restore = rho*fR*Rmax                  (symptom-triggered, Result 4 baseline)
#  'soft'  : restore = rho*fR*Rmax*(1-fD)           (cause-aware, linear backoff)
#  'hard'  : restore = rho*fR*Rmax if fD<0.25 else 0 (cause-aware, shuts off on exploitation)
def run(a,g,delta,window,b,rho=0.20,design='none'):
    T=200*window; burn=T//2
    fC=fD=fR=1.0/3.0; R=Rmax
    win=[]; sC=sD=sR=0.0; Rmin=1e9; sfR=sfD=0.0; nstat=0
    for t in range(T):
        pC=5.0; pD=12.0*(R/Rmax)**a; pR=2.0+b*(1.0-R/Rmax)
        win.append((pC,pD,pR)); sC+=pC; sD+=pD; sR+=pR
        if len(win)>window:
            oC,oD,oO=win.pop(0); sC-=oC; sD-=oD; sR-=oO
        n=len(win); rC=sC/n; rD=sD/n; rRr=sR/n
        if   design=='none': restore=rho*fR*Rmax
        elif design=='soft': restore=rho*fR*Rmax*(1.0-fD)
        elif design=='hard': restore=rho*fR*Rmax if fD<0.25 else 0.0
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax+restore
        if R<0.0: R=0.0
        elif R>Rmax: R=Rmax
        avg=fC*rC+fD*rD+fR*rRr
        fC=fC*rC/avg; fD=fD*rD/avg; fR=fR*rRr/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fR=(1-eps)*fR+eps/3
        s=fC+fD+fR; fC/=s; fD/=s; fR/=s
        if t>=burn:
            if R<Rmin: Rmin=R
            sfR+=fR; sfD+=fD; nstat+=1
    return Rmin, sfR/nstat, sfD/nstat

def astar(g,delta,window,b,rho=0.20,design='none',thr=1.0):
    a=0.5
    while a<=8.001:
        if run(a,g,delta,window,b,rho,design)[0]>thr: return round(a,2)
        a+=0.1
    return None

# ---------- A1: rho-dependence of the subsidy (Design none, b=8, subsidy regime) ----------
g=d=0.20; L=5  # P=1.0 fast-clock cell (strongest subsidy: b=8 gave alpha*=5.40 at rho=.20)
print("A1  rho-dependence of subsidy  (cell P=1.0 L=5, design=none).  baseline b=0 alpha*=2.70")
print(f"{'rho':>6} {'b=0':>6} {'b=8 alpha*':>11}  inflation")
for rho in [0.05,0.10,0.20,0.40]:
    a0=astar(g,d,L,0.0,rho,'none'); a8=astar(g,d,L,8.0,rho,'none')
    a0s='None' if a0 is None else f'{a0:.2f}'; a8s='None' if a8 is None else f'{a8:.2f}'
    infl='' if (a0 is None or a8 is None) else f'+{a8-a0:.2f}'
    print(f"{rho:>6.2f} {a0s:>6} {a8s:>11}  {infl}")
print()

# ---------- A2: can a cause-aware repair design protect? alpha*(b) per design ----------
bs=[0.0,4.0,8.0,16.0]
print("A2  alpha*(b) by repair design  (cell P=1.0 L=5).  alpha* <= 2.70 = no subsidy / protective")
print(f"{'b':>6} {'none':>8} {'soft':>8} {'hard':>8}   (none=symptom, soft/hard=cause-aware)")
for b in bs:
    row=[]
    for des in ['none','soft','hard']:
        a=astar(g,d,L,b,0.20,des); row.append('None' if a is None else f'{a:.2f}')
    print(f"{b:>6.1f} {row[0]:>8} {row[1]:>8} {row[2]:>8}")
print()
print("diagnostics at b=8 (fR, fD by design):")
for des in ['none','soft','hard']:
    a=astar(g,d,L,8.0,0.20,des)
    if a: _,fR,fD=run(a,g,d,L,8.0,0.20,des); print(f"  {des:>5}: alpha*={a:.2f}  <fR>={fR:.3f}  <fD>={fD:.3f}")
    else: print(f"  {des:>5}: None")
