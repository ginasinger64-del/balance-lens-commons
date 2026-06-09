from continuum import astar
print("Extending L to test for a plateau / merge. alpha grid from 0.20.\n")
for P in [1.0,0.5]:
    print(f"P = {P}")
    print(f"{'L':>6} {'g=d':>10} {'alpha*':>8} {'decrement':>10}")
    prev=None
    for L in [160,320,640,1280,2560]:
        g=P/L; a=astar(g,g,L)
        dec="" if (prev is None or a is None) else f"{a-prev:+.3f}"
        astr="None" if a is None else f"{a:.3f}"
        print(f"{L:>6} {g:>10.6f} {astr:>8} {dec:>10}")
        prev=a
    print()

# gap between the two P curves at each L
print("Gap (alpha*_P1.0 - alpha*_P0.5) vs L:")
for L in [160,320,640,1280,2560]:
    a1=astar(1.0/L,1.0/L,L); a5=astar(0.5/L,0.5/L,L)
    if a1 and a5: print(f"  L={L:>5}: {a1:.3f} - {a5:.3f} = {a1-a5:+.3f}")
