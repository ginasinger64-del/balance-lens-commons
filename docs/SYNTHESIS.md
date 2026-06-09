# Synthesis — Resource-Coupled Field

*Companion to FINDINGS.md (Results 1–10). This is the narrative; FINDINGS is the evidence.*

## The question

The toy started from one question: **what keeps local optimization coupled to collective
persistence?** A system of agents each maximizing local payoff can walk the whole collective
off a cliff (the original 20-agent run: utility-maximization → everyone copies the top
defector → collapse). The question is not "why does defection win" — under naive
imitation it wins by default — but what *architecture* keeps local incentives from
destroying the shared resource that makes optimization possible.

Two threads came out of pulling on that. They are independent and should be read as such.

---

## Thread I — what governs resilience (the coupling geometry)

We coupled the exploiter's payoff to the shared stock (`payoff_D = 12·(R/Rmax)^α`) so that
degrading the commons degrades the exploiter's own future return, and asked how steep that
coupling (α) must be to keep the commons alive.

- **Resilience is not the extraction/regeneration ratio.** The obvious candidate — δ/g
  (how fast exploitation drains vs how fast the resource regrows) — is *falsified*: cells
  with identical δ/g need wildly different α to survive (1.0 to "never"). (Result 1)

- **The leading-order control is (g·L, δ·L)** — the resource timescales measured against
  the *selection-update lag* L. In the weakly-driven regime these two dimensionless groups
  collapse a 4–8× spread of raw parameters onto a single transition. (Result 2)

- **The transition is a surface, not a point.** There is no universal protective α; the
  threshold lives in (g, δ, lag) space. (Result 3)

- **A third clock runs the show.** The strong-drive non-monotonic "hump" and the weak-drive
  "residual" turned out to be *one* phenomenon: the replicator updates once per turn
  regardless of how fast the resource moves, so the selection/resource clock ratio is a real
  third axis. Tying the clocks together removes the hump; sub-stepping the resource
  integration does nothing (so it is structural, not numerical). α* = f(P, clock-ratio);
  quote both coordinates. (Results 3c + 3d, merged)

The honest scope on Thread I: the *qualitative* structure is solid, but specific α* numbers
are resolution/architecture-dependent (the naive continuum limit is singular). The keeper is
the conceptual one: **resilience is governed by how fast the system can perceive and respond
to resource state relative to how fast it is being drained — not by the raw drain/regrow
ratio.** That is the original "coupling" intuition, made precise.

---

## Thread II — can an intervention keep the system viable? (the intervention hierarchy)

Given that local optimization decouples by default, what *added mechanism* re-couples it?
Three classes were tested. The result is a clean hierarchy.

**Restoration (repair) — fails. No protective regime at all.** A repairer that refills the
shared stock is either inert (too weak to be selected; exact activation threshold b>3) or,
once active, a *subsidy*: it refills exactly the stock the exploiters then harvest, so
protection gets *harder*, not easier (α* inflates, peaking at intermediate repair strength).
Gating restoration by exploitation ("repair only when defection is low") does not rescue it.
Restoration treats the symptom (depleted stock) and feeds the cause. (Results 4, A2)

**Enforcement (suppress the exploiter) — works, then collapses under its own cost.**
A strategy that directly reduces the exploiter's payoff lowers the protection threshold and,
in mean-field, even eliminates defection. But punishing is a public good: cooperators
free-ride on the enforcement, so the moment policing costs anything, enforcers are
out-competed and go extinct — the *second-order free-rider problem*. Protective only when
~free. (Result 5)

**Self-funded enforcement — solves the funding problem, partially, and introduces a new
constraint.** Redistribute confiscated exploiter payoff to the enforcers ("pay the police
from the loot") and a genuine *positive-cost* protective regime appears that unfunded
enforcement never had. But the funding is `revenue ∝ remaining exploitable behavior`, so as
enforcement succeeds and exploitation falls, the revenue that sustains enforcement falls with
it — a self-limiting ecology that oscillates near its funding ceiling. Within this
architecture, enforcement loses its revenue source as defection approaches zero. Oversight
and exploitation become **dynamically coupled populations**, not independent components.
(Result 6)

**Robustness (the kill-test).** Re-run under finite-N stochastic Fermi dynamics — dropping
both mean-field and replicator — the *ordinal* hierarchy survives: repair still subsidizes,
unfunded enforcement still collapses, self-funded enforcement still persists and raises the
resource. The *magnitudes* do not: defection elimination is a mean-field artifact, and clean
thresholds wash out. A new failure mode appears that the deterministic model is blind to —
noise-induced resource extinction (R=0 is an absorbing state). (Result 7)

**Spatial structure.** On a lattice with local resource patches, diffusion, and local
imitation, the hierarchy holds across all diffusion strengths, and self-funded enforcement is
*amplified* — clustering co-localizes suppression and loot-funding. A counterintuitive null:
spatial reciprocity *alone* does not rescue cooperation here (baseline stays defector-heavy
even at zero diffusion). The protective work is done by enforcement, not by assortment.
(Result 8)

---

## The spine — why the hierarchy survives every ecology

The hierarchy is not four facts; it is one principle. A mechanism-discrimination test held the
suppression mechanism and the total confiscated payoff fixed and varied *only the recipient*
of that payoff: vanish (unfunded), to enforcers privately (self-funded), to everyone equally
(pooled), or to the law-abiding only (pooled-CE). **Only private funding survived; every
pooled scheme collapsed identically to unfunded.** (Result 9)

The reason is an identity, not a curve-fit. Pooled redistribution adds the same share to
cooperators and enforcers, so it cancels from the comparison that decides whether enforcement
persists:

    pooled:      pE - pC = (5 - cost + share) - (5 + share) = -cost     (for ANY share)
    self-funded: pE - pC = -cost + private_reward                       (> 0 when reward>cost)

Cooperators free-ride on any shared benefit exactly as much as enforcers do, so a non-private
return leaves the protector permanently a cost behind, and it goes extinct. Because this is
algebra, not a feature of replicator dynamics, it is ecology-independent — which is why the
hierarchy reappeared under finite-N and spatial dynamics.

**The principle:**

> A protective mechanism survives if and only if its benefit is an *excludable private return*
> captured by the agents who bear its cost. Producing a non-excludable good — one that
> free-riders also enjoy — collapses the protector.

This subsumes the whole arc:

- **Repair fails** — a restored shared stock is non-excludable; defectors consume it freely.
  The return to repairing is a positive externality to the exploiter (subsidy), not a private
  gain to the repairer.
- **Unfunded enforcement fails** — suppression is a non-excludable public good (everyone
  enjoys fewer defectors) paid for privately. Textbook second-order free-riding.
- **Pooled enforcement fails** — redistributing the loot to all benefits cooperators too, so
  enforcers stay cost-disadvantaged (the −cost identity).
- **Self-funded enforcement works** — confiscated payoff is an excludable private reward to
  enforcers specifically, making protection privately sustainable.

The earlier framings were shadows of this. "Funding alignment" is excludability applied to the
cost side. "Cause vs symptom" was a red herring — both repair and enforcement can target the
right thing and still fail if the return is not excludable. The deep variable is *who can be
excluded from the benefit of the protective act.*

## The central result

> The system does not stabilize because bad actors vanish — under default imitation dynamics
> they do not. It stabilizes when the architecture makes *protection itself* evolutionarily
> viable: when the agents who pay to protect the commons capture an excludable return that
> free-riders cannot.

This is the answer to the original question. Local optimization stays coupled to collective
persistence not by eliminating exploitation, and not by patching the damage it does, but by
making the *act of protection* a locally winning strategy — which, mechanically, means making
its payoff excludable.

## Result 10 — excludability is a control parameter (added)

The recipient-swap (Result 9) generalizes: route a continuous fraction r of confiscated payoff
privately to enforcers. Across mean-field, finite-N stochastic, and spatial ecologies, raising r
monotonically increases enforcement persistence and resource health. Mean-field shows a sharp
phase transition (r*~0.8); noise and space soften it to a monotone ramp. The exact threshold is
parameter-dependent and dissolves under noise; the *direction* is ecology-invariant.

**The cleanest statement of the whole project:** protection does not scale with how much value
is recovered — it scales with how much of that value remains coupled (excludably) to the
protector. The operative variable is the *return pathway*: what fraction of the consequence of a
protective act stays bonded to its performer.

## What this is and is not

- It IS a coherent, mechanistic toy in which the keepers survived a genuine kill-test, with
  every failed hypothesis (resonance, discretization, the ratio law, cause-aware repair,
  cause-vs-symptom) documented and overturned by its own test. The central principle
  (excludability) is backed by an identity (the -cost cancellation), not just simulation,
  which is why it held across mean-field, finite-N, and spatial ecologies.
- It is NOT validated outside this model. The strongest *magnitude* claims are mean-field
  artifacts (Result 7). Everything is a single payoff form, one resource ODE. The excludability
  principle is general in its algebra but demonstrated only in this strategy/payoff family.
- The mapping to real oversight/alignment is an **analogy that generates hypotheses**, not a
  result about real systems. The legible correspondences (a bailout that keeps a failing
  actor solvent; oversight that collapses when no one funds it; enforcement funded by what it
  catches being unable to fully eliminate it) are suggestive, and that is all they are.

## Open

- **Spatial structure** — the one robustness axis left, and the one most likely to *change
  the ordering* rather than soften it (local assortment can let cooperator/enforcer clusters
  survive where well-mixed kills them). Run before any stronger claim.
- The continuum / clock-ratio law form (Thread I), and the Result-7 variance puzzle
  (self-funded raises R at ~equal mean defector load — likely variance damping).
