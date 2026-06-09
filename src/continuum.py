# Continuum-limit study. Fast pure-float inner loop.
# Conditions: alpha grid below 1.0; L beyond 160; run length ~ 1/g.
Rmax=100.0; eps=0.005; rho=0.20

def minR(a,g,delta,window):
    # run length scaled with slow timescale 1/g (~ L/P): T = 200*window
    T=200*window; burn=T//2
    fC=fD=fR=1.0/3.0; R=Rmax
    win=[]  # list of (pC,pD,pR)
    sC=sD=sR=0.0
    Rmin=1e9
    for t in range(T):
        pC=5.0; pD=12.0*(R/Rmax)**a; pR=2.0
        win.append((pC,pD,pR)); sC+=pC; sD+=pD; sR+=pR
        if len(win)>window:
            oC,oD,oO=win.pop(0); sC-=oC; sD-=oD; sR-=oO
        n=len(win); rC=sC/n; rD=sD/n; rRr=sR/n
        # resource update
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax+rho*fR*Rmax
        if R<0.0: R=0.0
        elif R>Rmax: R=Rmax
        # replicator on recent avg
        avg=fC*rC+fD*rD+fR*rRr
        fC=fC*rC/avg; fD=fD*rD/avg; fR=fR*rRr/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fR=(1-eps)*fR+eps/3
        s=fC+fD+fR; fC/=s; fD/=s; fR/=s
        if t>=burn and R<Rmin: Rmin=R
    return Rmin

def astar(g,delta,window,thr=1.0):
    a=0.20
    while a<=8.001:
        if minR(a,g,delta,window)>thr: return round(a,3)
        a+=0.05
    return None

# sanity: P=1.0 L=40 should be ~1.95 (numpy residual.py)
print("sanity P=1.0 L=40 (expect ~1.95):", astar(1.0/40,1.0/40,40))
print()

for P in [1.0,0.5]:
    print(f"P = {P}   (alpha grid from 0.20, step 0.05)")
    print(f"{'L':>5} {'g=d':>9} {'alpha*':>8} {'decrement':>10}")
    prev=None
    for L in [40,80,160,320,640]:
        g=P/L; a=astar(g,g,L)
        dec="" if (prev is None or a is None) else f"{a-prev:+.3f}"
        astr="None" if a is None else f"{a:.3f}"
        print(f"{L:>5} {g:>9.5f} {astr:>8} {dec:>10}")
        prev=a
    print()
