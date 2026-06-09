Why do some protective systems survive their own incentives while others collapse?
A series of falsification experiments exploring which mechanisms let protective behavior
persist under local optimization pressure on a regenerating commons.
It started as a toy commons model and a narrow question — can local optimization become
self-limiting without external control? — and became, after ten rounds of killing its own
hypotheses, a falsification trail that keeps pointing at one variable: return-path
coupling.
The claim that survived:
> Protective behavior persists in proportion to how strongly the *consequences* of protection
> remain coupled to the protector. Protection does not scale with how much value is recovered;
> it scales with how much of that value stays coupled (excludably) to the protector.
This is not asserted — it's what was left standing after the more obvious candidates were
falsified by their own tests.
The arc, in five steps:
Ratio control failed. The obvious knob — extraction/regeneration ratio (δ/g) — does
not govern resilience. Falsified. (Result 1)
Timescale coupling emerged. The leading-order controls are the dimensionless groups
g·L and δ·L — resource speed measured against the selection-update lag. (Results 2–3)
A third clock explained the anomalies. Strong-drive non-monotonicity and a weak-drive
residual were one effect: the selection/resource clock ratio. (Results 3c–3d)
Restoration consistently failed as a protective mechanism. Refilling a shared stock
subsidizes the exploiters who consume it; there is no protective regime. (Results 4–6)
Excludability emerged as the most robust control parameter across mean-field, finite-N
stochastic, and spatial ecologies. The strongest single result in the repo. (Results 9–10)
The strongest figure is the three-ecology excludability sweep (Result 10): mean-field
shows a sharp transition, finite-N and spatial soften it to a ramp, but the direction is
identical everywhere — more privately-coupled return → more persistent protection. That
directional law survived every kill-test.
---
The model
Three strategies live on a logistically regenerating resource: Cooperate, Defect
(payoff coupled to the resource it depletes), and a third Repair/Enforce slot whose
design is varied. The mechanistic core is backed by an identity, not a fit: under any pooled
redistribution the enforcer's payoff minus the cooperator's is exactly −cost, for any pool
size, so enforcers always lag
and go extinct. Only a private (excludable) return flips the sign.
Try it
▶ Live demo (runs in your browser, nothing to install):
https://ginasinger64-del.github.io/balance-lens-commons/demo/commons-dashboard.html
Toggle Unfunded ↔ Self-funded and watch the enforcer population die or persist; slide
enforcement cost and funding-leakage to find the thresholds.
(Or download `demo/commons-dashboard.html` and double-click it locally — same thing, no dependencies.)

Scope (read this first)
This is a toy model — a minimal replicator/imitation dynamic on a single regenerating
resource, one payoff family, deliberately stripped down. It is not validated outside this
model, and it makes no direct claim about real institutions or AI systems; any such mapping
is an analogy that generates hypotheses, nothing more. The qualitative hierarchy is robust
across the ecologies tested; specific transition numbers are model/architecture-dependent and
should not be quoted as physical (see `docs/FINDINGS.md`, Results 3d and 7).
The work is presented honestly including its dead ends — several hypotheses (period/lag
resonance, finite-step discretization, an extraction/regeneration ratio law, cause-aware
repair, "cause vs symptom") were proposed and then falsified by their own tests. Those are
documented in `docs/FINDINGS.md` on purpose; the self-correction is part of the evidence.
Repository layout
```
demo/       commons-dashboard.html  — open in a browser, zero dependencies (also a .jsx version)
src/        simulation scripts (Python, NumPy; spatial/robustness also use scipy)
results/    captured stdout logs from each script (one .log per .py)
docs/
  FINDINGS.md    full result-by-result lab notebook (Results 1-10, incl. falsified hypotheses)
  SYNTHESIS.md   the narrative: how the pieces fit into one principle
```
How to run the Python
```bash
pip install numpy scipy
cd src
python discriminate.py        # the headline result (excludability discriminator)
```
Notes on reproducibility:
Deterministic scripts (mean-field replicator) reproduce exactly — no RNG in the update.
Stochastic scripts (`robust*.py`, `spatial*.py`) average over seeds; expect numbers
close but not bit-identical to the logs. The claim is the ordering, not the third decimal.
A couple of scripts import another (`continuum2.py` imports `continuum.py`;
`spatial_diff.py` imports `spatial.py`), so run them from inside `src/`.
`robust.py` is the pre-fix run: it hit the R=0 absorbing-state artifact (the commons
dies, so every condition flatlines). `robust2.py` is the corrected version with a small
recruitment term that lets the resource recover, and it is the one the conclusions use. Both
are kept on purpose — the pair shows the artifact being caught (see FINDINGS Result 7).
Script → claim map
Script	What it shows	Result
`sweep.py`, `sweep2.py`	baseline collapse; α-sweep; repair flat vs coupled	1, 2b seed
`lagsweep.py`	(g·L, δ·L) collapses the transition; clock-ratio test	2
`densegroup.py`	dense sweep of the dimensionless product	3
`period.py`	oscillation period vs lag — falsifies resonance	3c
`robust_astar.py`	α* under 3 protection criteria — falsifies metric-artifact	3c
`timescale.py`	tying selection clock to resource speed removes the "hump"	3c
`gainsweep.py`	separates timescale-matching from control-gain	3c
`residual.py`, `continuum.py`, `continuum2.py`	continuum limit is singular (not numerics)	3d
`substep.py`	sub-stepping the resource — falsifies discretization	3d
`repair.py`	repair has no protective regime (inert or subsidy)	4
`repair2.py`	rho-dependence (inconclusive) + cause-aware gating fails	4
`enforce.py`	enforcement protects but collapses under cost (free-riding)	5
`enforce2.py`	self-funded enforcement: positive-cost regime + conservation law	6
`robust.py`, `robust2.py`	finite-N Fermi: hierarchy survives ordinally	7
`spatial.py`, `spatial_diff.py`	spatial lattice + diffusion: hierarchy survives	8
`discriminate.py`	the spine — recipient-swap isolates excludability	9
`excludability.py`, `excludability_finiteN.py`, `excludability_spatial.py`	r-sweep: excludability as a control parameter; directional law survives all 3 ecologies	10
The model in one paragraph
Resource `R` regenerates logistically (`R += g·R·(1−R/Rmax)`), is depleted by defectors, and
(in repair variants) restored by repairers. Defect payoff is coupled to the stock,
`12·(R/Rmax)^α`; cooperate is flat (5); the third strategy is repair (`2 + b·(1−R/Rmax)`,
restores the stock) or enforce (suppresses defect payoff by `1−κ·f_E`, pays a cost, optionally
funded from confiscated defector payoff). Selection is a recent-payoff replicator (mean-field),
a finite-N Fermi imitation (stochastic), or local Fermi imitation on a lattice (spatial).
License
MIT — see LICENSE.

Prior work
This re-derives and extends known results in the costly-punishment / second-order
free-riding / club-goods literature (e.g. pool-punishment institutions; the Ostrom/Buchanan
excludability line). The contribution here is the bundle: restoration-vs-enforcement
contrasted on a regenerating stock, excludability identified as the single unifying axis via
the recipient-swap, and the ordinal hierarchy shown to survive three ecologies. Verify nearest
prior work before claiming novelty in any writeup.
