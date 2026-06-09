# Method B: refine ONLY the resource integration (n sub-steps/turn), holding selection
# cadence (1/turn) and memory window (L turns) FIXED. Isolates resource-discretization
# without sending selection speed to infinity. n=1 = original model.
Rmax=100.0; eps=0.005; rho=0.20

def minR(a,g,delta,window,nsub):
    T=200*window; burn=T//2
    fC=fD=fR=1.0/3.0; R=Rmax
    win=[]; sC=sD=sR=0.0; Rmin=1e9
    for t in range(T):
        pC=5.0; pD=12.0*(R/Rmax)**a; pR=2.0
        win.append((pC,pD,pR)); sC+=pC; sD+=pD; sR+=pR
        if len(win)>window:
            oC,oD,oO=win.pop(0); sC-=oC; sD-=oD; sR-=oO
        n=len(win); rC=sC/n; rD=sD/n; rRr=sR/n
        # resource: integrate one turn's worth of ODE with nsub substeps (fixed f within turn)
        dt=1.0/nsub
        for _ in range(nsub):
            R=R+dt*(g*R*(1.0-R/Rmax)-delta*fD*Rmax+rho*fR*Rmax)
            if R<0.0: R=0.0
            elif R>Rmax: R=Rmax
        avg=fC*rC+fD*rD+fR*rRr
        fC=fC*rC/avg; fD=fD*rD/avg; fR=fR*rRr/avg
        fC=(1-eps)*fC+eps/3; fD=(1-eps)*fD+eps/3; fR=(1-eps)*fR+eps/3
        s=fC+fD+fR; fC/=s; fD/=s; fR/=s
        if t>=burn and R<Rmin: Rmin=R
    return Rmin

def astar(g,delta,window,nsub,thr=1.0):
    a=0.20
    while a<=8.001:
        if minR(a,g,delta,window,nsub)>thr: return round(a,3)
        a+=0.05
    return None

print("Method B: sub-step resource integration at FIXED (g, delta, L). n=1 is the orig model.")
print("If alpha* converges as n grows, the residual IS resource-discretization and we can")
print("read off the discretization-free alpha* at each cell.\n")
for (P,L) in [(1.0,40),(1.0,80),(0.5,40)]:
    g=P/L
    print(f"P={P} L={L} (g=delta={g:.5f})")
    print(f"{'nsub':>5} {'alpha*':>8} {'decrement':>10}")
    prev=None
    for n in [1,2,4,8,16,32]:
        a=astar(g,g,L,n)
        dec="" if (prev is None or a is None) else f"{a-prev:+.3f}"
        print(f"{n:>5} {a:>8.3f} {dec:>10}")
        prev=a
    print()
