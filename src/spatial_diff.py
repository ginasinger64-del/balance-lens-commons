from spatial import simulate
import numpy as np
print("Diffusion sensitivity: is baseline defector-dominance a high-diffusion artifact?")
print("Lower Ddiff => more independent patches => classic spatial reciprocity should help C.\n")
print(f"{'Ddiff':>6} | {'baseline fD':>12} {'base R':>7} | {'selffund fD':>12} {'self R':>7} {'self f2':>8}")
for Dd in [0.0,0.02,0.05,0.15,0.40]:
    rb=np.mean([simulate('baseline',Ddiff=Dd,seed=s) for s in range(2)],axis=0)
    rs=np.mean([simulate('selffund',Ddiff=Dd,seed=s) for s in range(2)],axis=0)
    print(f"{Dd:>6.2f} | {rb[0]:>12.3f} {rb[1]:>7.1f} | {rs[0]:>12.3f} {rs[1]:>7.1f} {rs[2]:>8.3f}")
print("\nfD lower at low Ddiff => spatial reciprocity protects C when patches are independent.")
