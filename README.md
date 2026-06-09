## How to run the Python

```bash
pip install numpy scipy
cd src
python discriminate.py        # the headline result (excludability discriminator)
```

Notes on reproducibility:
- Deterministic scripts (mean-field replicator) reproduce **exactly** — no RNG in the update.
- Stochastic scripts (`robust*.py`, `spatial*.py`) average over seeds; expect numbers
  *close but not bit-identical* to the logs. The claim is the **ordering**, not the third decimal.
- A couple of scripts import another (`continuum2.py` imports `continuum.py`;
  `spatial_diff.py` imports `spatial.py`), so run them from inside `src/`.
- **`robust.py` is the *pre-fix* run**: it hit the R=0 absorbing-state artifact (the commons
  dies, so every condition flatlines). `robust2.py` is the corrected version with a small
  recruitment term that lets the resource recover, and it is the one the conclusions use. Both
  are kept on purpose — the pair shows the artifact being caught (see FINDINGS Result 7).

## Script → claim map

| Script | What it shows | Result |
|---|---|---|
| `sweep.py`, `sweep2.py` | baseline collapse; α-sweep; repair flat vs coupled | 1, 2b seed |
| `lagsweep.py` | (g·L, δ·L) collapses the transition; clock-ratio test | 2 |
| `densegroup.py` | dense sweep of the dimensionless product | 3 |
| `period.py` | oscillation period vs lag — **falsifies** resonance | 3c |
| `robust_astar.py` | α\* under 3 protection criteria — **falsifies** metric-artifact | 3c |
| `timescale.py` | tying selection clock to resource speed removes the "hump" | 3c |
| `gainsweep.py` | separates timescale-matching from control-gain | 3c |
| `residual.py`, `continuum.py`, `continuum2.py` | continuum limit is singular (not numerics) | 3d |
| `substep.py` | sub-stepping the resource — **falsifies** discretization | 3d |
| `repair.py` | repair has no protective regime (inert or subsidy) | 4 |
| `repair2.py` | rho-dependence (inconclusive) + cause-aware gating **fails** | 4 |
| `enforce.py` | enforcement protects but collapses under cost (free-riding) | 5 |
| `enforce2.py` | self-funded enforcement: positive-cost regime + conservation law | 6 |
| `robust.py`, `robust2.py` | finite-N Fermi: hierarchy survives ordinally | 7 |
| `spatial.py`, `spatial_diff.py` | spatial lattice + diffusion: hierarchy survives | 8 |
| `discriminate.py` | **the spine** — recipient-swap isolates excludability | 9 |
| `excludability.py`, `excludability_finiteN.py`, `excludability_spatial.py` | r-sweep: excludability as a control parameter; directional law survives all 3 ecologies | 10 |

## The model in one paragraph

Resource `R` regenerates logistically (`R += g·R·(1−R/Rmax)`), is depleted by defectors, and
(in repair variants) restored by repairers. Defect payoff is coupled to the stock,
`12·(R/Rmax)^α`; cooperate is flat (5); the third strategy is repair (`2 + b·(1−R/Rmax)`,
restores the stock) or enforce (suppresses defect payoff by `1−κ·f_E`, pays a cost, optionally
funded from confiscated defector payoff). Selection is a recent-payoff replicator (mean-field),
a finite-N Fermi imitation (stochastic), or local Fermi imitation on a lattice (spatial).

## License

MIT — see [LICENSE](LICENSE).

## Prior work

This re-derives and extends known results in the costly-punishment / second-order
free-riding / club-goods literature (e.g. pool-punishment institutions; the Ostrom/Buchanan
excludability line). The contribution here is the *bundle*: restoration-vs-enforcement
contrasted on a regenerating stock, excludability identified as the single unifying axis via
the recipient-swap, and the ordinal hierarchy shown to survive three ecologies. Verify nearest
prior work before claiming novelty in any writeup.
