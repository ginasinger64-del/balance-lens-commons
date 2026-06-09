import numpy as np
from scipy.signal import find_peaks

Rmax=100.0; eps=0.005

def payoffs(R,a): return np.array([5.0,12.0*(R/Rmax)**a,2.0])

def trace(a,g,delta,window,rho=0.20,T=12000,burn=6000):
    frac=np.array([1/3,1/3,1/3]); R=Rmax; win=[]; Rtr=[]
    for t in range(T):
        p=payoffs(R,a); win.append(p)
        if len(win)>window: win.pop(0)
        recent=np.mean(win,axis=0)
        R=min(Rmax,max(0.0,R+g*R*(1-R/Rmax)-delta*frac[1]*Rmax+rho*frac[2]*Rmax))
        avg=np.dot(frac,recent); frac=frac*(recent/avg)
        frac=(1-eps)*frac+eps*(1/3); frac/=frac.sum(); Rtr.append(R)
    return np.array(Rtr[burn:])

def period(R):
    x = R - R.mean()
    amp = R.std()
    if amp < 0.5:                      # essentially flat -> no oscillation
        return None, amp
    # peak-spacing
    pk,_ = find_peaks(x, distance=2, prominence=amp*0.3)
    tau_peak = np.median(np.diff(pk)) if len(pk)>2 else None
    # FFT cross-check
    f = np.fft.rfftfreq(len(x))
    P = np.abs(np.fft.rfft(x))**2
    P[0]=0
    fdom = f[np.argmax(P)]
    tau_fft = (1.0/fdom) if fdom>0 else None
    return (tau_peak, tau_fft, amp)

P=1.5
print(f"P = {P}  (g = delta = P/L).  alpha* from earlier: L5=3.9 L10=5.3 L20=6.5 L40=5.9 (hump at L20)\n")

# measure period at a fixed alpha where ALL lags oscillate (below every alpha*), and at alpha=3
for a_meas in [2.0, 3.0]:
    print(f"--- period measured at alpha = {a_meas} ---")
    print(f"{'L':>4} {'g=d':>7} {'amp_R':>7} {'tau_pk':>7} {'tau_fft':>8} {'tau/L':>7} {'tau*g':>7}")
    for L in [5,10,20,40]:
        g=P/L
        R=trace(a_meas,g,g,L)
        res=period(R)
        if res[0] is None and len(res)==2:
            print(f"{L:>4} {g:>7.4f} {res[1]:>7.2f}   flat (no oscillation)")
            continue
        tp,tf,amp=res
        tpL = (tp/L) if tp else float('nan')
        tpg = (tp*g) if tp else float('nan')
        ts = f"{tp:>7.1f}" if tp else "   None"
        fs = f"{tf:>8.1f}" if tf else "    None"
        print(f"{L:>4} {g:>7.4f} {amp:>7.2f} {ts} {fs} {tpL:>7.2f} {tpg:>7.3f}")
    print()
