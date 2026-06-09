# Excludability and the survival of protective behavior on a regenerating commons

A minimal evolutionary-game study of one question:

> **Can local optimization become self-limiting without external control — and if a
> protective behavior is added, when does it survive the system's own dynamics?**

Three strategies live on a logistically regenerating resource: **Cooperate**, **Defect**
(payoff coupled to the resource it depletes), and a third **Repair/Enforce** slot whose
design is varied. The headline result:

> **A protective mechanism survives if and only if its benefit is an *excludable private
> return* captured by the agents who bear its cost.** Restoration fails (it refills a shared
> stock exploiters consume); unfunded enforcement collapses (suppression is a public good
> others free-ride); pooled-funded enforcement collapses for the same reason; only
> *self-funded* enforcement — where confiscated payoff goes to enforcers specifically —
> survives, and it does so across mean-field, finite-N stochastic, and spatial ecologies.

The core is backed by an identity, not a fit: under any pooled redistribution the enforcer's
payoff minus the cooperator's is exactly **−cost**, for any pool size, so enforcers always lag
and go extinct. Only a private (excludable) return flips the sign.

## Try it

**▶ Live demo (runs in your browser, nothing to install):**
https://ginasinger64-del.github.io/balance-lens-commons/demo/commons-dashboard.html

Toggle Unfunded ↔ Self-funded and watch the enforcer population die or persist; slide
enforcement cost and funding-leakage to find the thresholds.

(Or download `demo/commons-dashboard.html` and double-click it locally — same thing, no dependencies.)

## Scope (read this first)

This is a **toy model** — a minimal replicator/imitation dynamic on a single regenerating
resource, one payoff family, deliberately stripped down. It is **not** validated outside this
model, and it makes **no** direct claim about real institutions or AI systems; any such mapping
is an analogy that generates hypotheses, nothing more. The *qualitative* hierarchy is robust
across the ecologies tested; specific transition numbers are model/architecture-dependent and
should not be quoted as physical (see `docs/FINDINGS.md`, Results 3d and 7).

The work is presented honestly including its **dead ends** — several hypotheses (period/lag
resonance, finite-step discretization, an extraction/regeneration ratio law, cause-aware
repair, "cause vs symptom") were proposed and then *falsified by their own tests*. Those are
documented in `docs/FINDINGS.md` on purpose; the self-correction is part of the evidence.

## Repository layout

```
demo/       commons-dashboard.html  — open in a browser, zero dependencies (also a .jsx version)
src/        simulation scripts (Python, NumPy; spatial/robustness also use scipy)
results/    captured stdout logs from each script (one .log per .py)
docs/
  FINDINGS.md    full result-by-result lab notebook (Results 1-9, incl. falsified hypotheses)
  SYNTHESIS.md   the narrative: how the pieces fit into one principle
```

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

## The model in one paragraph

Resource `R` regenerates logistically (`R += g·R·(1−R/Rmax)`), is depleted by defectors, and
(in repair variants) restored by repairers. Defect payoff is coupled to the stock,
`12·(R/Rmax)^α`; cooperate is flat (5); the third strategy is repair (`2 + b·(1−R/Rmax)`,
restores the stock) or enforce (suppresses defect payoff by `1−κ·f_E`, pays a cost, optionally
funded from confiscated defector payoff). Selection is a recent-payoff replicator (mean-field),
a finite-N Fermi imitation (stochastic), or local Fermi imitation on a lattice (spatial).

## License 
MIT — see LICENSE.

## Prior work

This re-derives and extends known results in the costly-punishment / second-order
free-riding / club-goods literature (e.g. pool-punishment institutions; the Ostrom/Buchanan
excludability line). The contribution here is the *bundle*: restoration-vs-enforcement
contrasted on a regenerating stock, excludability identified as the single unifying axis via
the recipient-swap, and the ordinal hierarchy shown to survive three ecologies. Verify nearest
prior work before claiming novelty in any writeup.
