# Repair-coupling sweep. payoff_R = 2 + b*(1-R/Rmax); repair restores rho*fR*Rmax.
# b=0 -> flat repair (dominated, dies) = C/D baseline. Sweep b, track protection threshold alpha*.
Rmax=100.0; eps=0.005

def run(a,g,delta,window,b,rho=0.20):
    T=200*window; burn=T//2
    fC=fD=fR=1.0/3.0; R=Rmax
    win=[]; sC=sD=sR=0.0; Rmin=1e9; sfR=0.0; sfD=0.0; nstat=0
    for t in range(T):
        pC=5.0; pD=12.0*(R/Rmax)**a; pR=2.0+b*(1.0-R/Rmax)
        win.append((pC,pD,pR)); sC+=pC; sD+=pD; sR+=pR
        if len(win)>window:
            oC,oD,oO=win.pop(0); sC-=oC; sD-=oD; sR-=oO
        n=len(win); rC=sC/n; rD=sD/n; rRr=sR/n
        R=R+g*R*(1.0-R/Rmax)-delta*fD*Rmax+rho*fR*Rmax
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

def astar(g,delta,window,b,thr=1.0):
    a=0.5
    while a<=8.001:
        if run(a,g,delta,window,b)[0]>thr: return round(a,2)
        a+=0.1
    return None

cells=[("P=0.75 L=5 (fast clock)",0.15,0.15,5),
       ("P=1.0  L=5 (fast clock)",0.20,0.20,5),
       ("P=1.0  L=10(slow clock)",0.10,0.10,10)]
bs=[0.0,0.5,1.0,2.0,4.0,8.0,16.0]

print("alpha*(b): protection threshold vs repair-coupling strength b.  b=0 = dead repair (C/D only).")
print("alpha* UP with b => repair SUBSIDIZES (protection harder). DOWN => repair helps.\n")
for label,g,d,L in cells:
    print(label)
    print(f"{'b':>6} {'alpha*':>8} {'<fR>':>7} {'<fD>':>7}")
    base=None
    for b in bs:
        a=astar(g,d,L,b)
        # diagnostics at a fixed reference alpha just above baseline threshold
        fR=fD=None
        if a is not None:
            _,fR,fD=run(a,g,d,L,b)
        astr="None" if a is None else f"{a:.2f}"
        fRs="" if fR is None else f"{fR:.3f}"
        fDs="" if fD is None else f"{fD:.3f}"
        tag=""
        if b==0: base=a
        elif a is not None and base is not None:
            tag = " (subsidy)" if a>base+1e-9 else (" (helps)" if a<base-1e-9 else " (neutral)")
        print(f"{b:>6.1f} {astr:>8} {fRs:>7} {fDs:>7}{tag}")
    print()
