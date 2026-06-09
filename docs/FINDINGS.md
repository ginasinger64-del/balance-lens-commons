# Resource-Coupled Field: Experimental Sequence

Minimal well-mixed replicator model. Three strategies (Cooperate / Defect / Repair)
on a logistically self-regenerating resource stock R. Defect payoff is coupled to the
stock via an exponent alpha: `payoff_D = 12*(R/Rmax)^alpha`; Cooperate flat (5),
Repair flat (2) unless coupled. Selection = discrete replicator on the last-`window`-turn
average payoff. Resource: `R += g*R*(1-R/Rmax) - delta*fD*Rmax + rho*fR*Rmax`.

Model is deterministic given parameters (no RNG in the update), so every alpha* below
is exact to the alpha-grid resolution, not a seed average.

---

## Working claim (strongest defensible version)

> Resilience is not controlled by the extraction/regeneration ratio. It is primarily
> controlled by the resource dynamics measured against the selection-update lag. In
> weak/moderate regimes, delta*lag and g*lag collapse the transition. At stronger drive,
> residual lag dependence appears, suggesting resonance between the resource-oscillation
> period and the selection delay.

---

## Result 1 — delta/g is FALSIFIED as the control variable

In the 2D (g, delta) sweep at fixed lag=5, cells sharing the same delta/g ratio give
wildly different transition points alpha*:

    g     delta   delta/g   alpha*
    0.05  0.05    1.00      1.0
    0.10  0.10    1.00      1.5
    0.20  0.20    1.00      3.0
    0.30  0.30    1.00      4.0
    0.40  0.40    1.00      None (no protection at any alpha in range)

Same ratio, five answers spanning the full range. The ratio scatters the data rather
than collapsing it. Absolute scale matters; the ratio carries no information at the
extremes (delta=0.05 -> always protectable; delta=0.40 -> never).

## Result 2 — (delta*lag, g*lag) collapses the data in the weak/moderate regime

Lag sweep + collapse test (lagsweep.py): cells sharing the dimensionless product
delta*lag = g*lag = 1.00, despite 4x spread in raw parameters, land within one
alpha-grid cell:

    g=.05 delta=.05 L=20  -> alpha* = 2.75
    g=.10 delta=.10 L=10  -> alpha* = 3.00
    g=.20 delta=.20 L=5   -> alpha* = 2.75   (raw table gave 1.0 / 1.5 / 2.75)

Half the product (=0.50) gives a distinct, lower, internally-consistent band
(alpha* = 1.25, 1.50). The dimensionless group is the leading-order control.

## Result 3 — collapse breaks at strong drive via non-monotonic lag dependence

Dense product sweep (densegroup.py), delta=g diagonal, product P = g*lag:

    P     L=5   L=10  L=20  L=40   spread
    0.25  1.0   1.0   1.0   1.0    0.0    perfect
    0.50  1.5   1.3   1.1   1.0    0.5
    0.75  2.1   1.9   1.7   1.3    0.8
    1.00  2.7   2.8   2.6   2.0    0.8    tight except largest lag
    1.50  3.9   5.3   6.5   5.9    2.6    FAILS, non-monotonic in lag
    2.00  6.6   None  None  None    -     falls apart

Two departures from a clean single-group law:
  (a) Residual: at fixed P, alpha* drifts DOWN as lag grows (P=1.0: 2.7,2.8,2.6,2.0).
      A trend, not grid noise -> the product is leading-order, not exact.
  (b) At P>=1.5 alpha* is NON-MONOTONIC in lag (hump at L=20: 3.9, 5.3, 6.5, 5.9).
      The strong-drive breakdown is REAL but its mechanism is NOT YET KNOWN. Two
      hypotheses tested and rejected (see Result 3c).

## Result 3c — strong-drive hump EXPLAINED (third clock, established); residual is SEPARATE

SUMMARY: period/lag resonance falsified; threshold artifact falsified; third-clock
hypothesis ESTABLISHED (within this model) as the explanation for the strong-drive hump.
Tying selection speed to resource speed removes the hump across the full gain range
tested; the fast-end (L=5) instability is a distinct CONTROL-GAIN effect that appears only
at high gain, not a timescale effect. The weak-regime fixed-P residual SURVIVES clock
rescaling and is a separate higher-order effect (see Result 3d).

The non-monotonic alpha*(L) at P=1.5 was probed directly.

FALSIFIED #1 -- period/lag resonance (period.py). Measured the resource oscillation
period tau at P=1.5 across L=5,10,20,40 (peak-spacing + FFT, agree to <1%):

    alpha=2.0:  L=5  tau=54   tau/L=10.8  tau*g=16.2
                L=10 tau=79   tau/L= 7.9  tau*g=11.9
                L=20 tau=129  tau/L= 6.5  tau*g= 9.7   <- alpha* peaks here
                L=40 tau=214  tau/L= 5.4  tau*g= 8.0

    Both tau/L and tau*g are MONOTONE in L and pass through L=20 with no feature.
    No small-integer commensurability at the hump. Resonance reading is dead.

FALSIFIED #2 -- threshold/sampling artifact (robust_astar.py). Re-measured alpha*(L)
under three protection criteria with doubled run length (T=20000, burn=10000):

    criterion           L=5  L=10  L=20  L=40
    min_R>1 (original)  3.9  5.3   6.5   5.9   HUMP
    p5_R>5  (robust)    4.0  5.5   6.9   6.5   HUMP
    <2% time below 2    3.9  5.4   6.6   6.1   HUMP

    Hump survives every criterion and the longer runs. Not a metric artifact. REAL.

STANDING HYPOTHESIS (now SUPPORTED) -- an unscaled third clock. Three timescales:
  (1) resource dynamics ~1/g   (2) selection memory = lag window L
  (3) the replicator step: `frac *= recent/avg` fires ONCE PER TURN at a fixed per-turn
      rate that does not scale with g or L.
The (g*L, delta*L) grouping holds (1) and (2) in fixed ratio (why P collapses the weak
regime) but does nothing to (3). At fixed P the window spans constant resource time
(L*g = P), yet the replicator's per-turn responsiveness is invariant while g varies 8x.

TEST RUN (timescale.py). Tied selection speed to resource speed via step exponent
eta = g/g_ref (g_ref=0.15; eta=1 at L=10). At P=1.5:

    mode                         L=5    L=10  L=20  L=40
    eta=1   (unscaled, orig)     3.9    5.3   6.5   5.9   HUMP
    eta=g/g_ref (3 clocks tied)  None   5.3   4.4   4.2   monotone

  -> Hump REMOVED for L=10,20,40 (goes monotone). Third clock supported: the hump was
     generated by the mismatch between resource speed, selection memory, and replicator
     responsiveness. The intervention predicted the right direction.
  -> CAVEAT: L=5 -> None. At L=5, eta = 0.30/0.15 = 2.0, i.e. doubled replicator gain.
     This conflates two things -- timescale MATCHING and control GAIN. eta=2 overshoots
     (classic too-much-gain instability), destroying protection independent of the hump.
     So the L=5 anomaly is evidence against the *specific scaling* eta=g/g_ref, NOT
     against the third-clock hypothesis.

RESIDUAL IS SEPARATE. Same rescaling at P=1.0:

    mode                         L=5   L=10  L=20  L=40
    eta=1   (unscaled, orig)     2.7   2.8   2.6   2.0
    eta=g/g_ref (3 clocks tied)  3.0   2.5   2.2   2.0

  Shape changes (flat-then-drop -> clean monotone) but spread (~1.0) does NOT vanish.
  The fixed-P residual survives clock-tying => it is a DIFFERENT phenomenon from the hump.
  Most likely the leading-order (g*L, delta*L) law is simply not exact -- a genuine
  higher-order correction, independent of the replicator rate. Mechanism still open, but
  it is a refinement, not a breakdown.

  Discriminating test (queued): gain sweep eta = c*(g/g_ref) for c in {0.25,0.5,0.75,1.0}
  on the P=1.5 row. Question: does the hump stay gone BEFORE the fast-end (L=5) instability
  appears? If yes -> "third clock ESTABLISHED". If no -> "third clock SUPPORTED" stands.

GAIN SWEEP RESULT (gainsweep.py) -- ESTABLISHED. P=1.5, eta = c*(g/g_ref):

    c      eta@L5   L=5   L=10  L=20  L=40   shape
    0.25   0.50     2.3   2.2   2.1   2.1    flat/monotone, all protected
    0.50   1.00     3.9   3.2   2.9   3.0    0.1 wobble (grid noise, not the hump)
    0.75   1.50     5.7   4.3   3.7   3.7    monotone, all protected
    1.00   2.00     None  5.3   4.4   4.2    monotone + L=5 instability

  The original L=20-peaked hump (amp ~2.6) does not reappear at ANY gain. Clean window
  c<=0.75 where hump is gone AND all four lags protected. The two effects separate exactly
  as the control framing predicted: timescale MATCHING (eta ~ g) kills the hump at every
  gain; control GAIN (coefficient c) causes the fast-end instability and only at high gain
  (L=5 dies only at c=1.0, eta=2.0). Side note: gain raises alpha* monotonically
  (c=0.25 ~2.2 vs c=1.0 ~5 at L=10) -- expected gain/stability-cost tradeoff, orthogonal
  to the hump.

---

WORKING SENTENCE (current honest state):
> In the weak regime, resilience approximately collapses under g*L and delta*L, with a
> small higher-order residual that survives clock rescaling and remains unexplained. In
> the strong regime the collapse fails via a non-monotonic hump in alpha*(L); this is NOT
> period/lag resonance or a threshold artifact, but an unscaled selection-update clock --
> the replicator step fires once per turn regardless of resource speed -- since tying
> selection speed to resource speed removes the hump.

---

Also archived (Result 2b, repair-as-subsidy): in the coupled-repair variant a
scarcity-triggered repairer INVERTS from protective to subsidizing. Cells protected at
the weakest coupling under flat repair become collapse-capable at every alpha once repair
is coupled (fR ~0.44-0.49 while min_R pins at 0.0). The fixer feeds the thing it restrains.

---

## Result 3d — the fixed-P residual is STRUCTURAL (the third clock / surface), NOT numerical
##              [REVISED -- earlier "discretization" reading was WRONG; see history below]

Tested two ways.

NAIVE L-EXTENSION (residual.py + continuum.py). Push L at fixed P (g=delta=P/L), alpha
grid extended below 1.0, run length ~1/g:

    P=1.0  L:  40   80   160  320  640  1280 2560
           a*: 1.95 1.45 1.20 0.95 0.75 0.45 0.20   decrements ~constant -0.25 (NOT shrinking)
    P=0.5  L:  40   80   160  320  640  1280 2560
           a*: 0.85 0.75 0.60 0.50 0.35 0.20 0.20   (both then pinned at 0.20 grid floor)

alpha* does NOT converge -- it slides ~linearly in log L, decrements stay ~0.25, and both
curves run into the grid floor. The earlier "converges to alpha~1" reading was a GRID-FLOOR
ARTIFACT (the old grid bottomed at 1.0). Pushing L at fixed P with selection fixed per-turn
sends the selection/resource clock ratio to INFINITY -- a singular adiabatic-selection
limit, not a continuum limit. So L-extension cannot probe discretization.

PROPER TEST -- sub-step the resource integration (substep.py). Refine ONLY the resource
ODE timestep (n sub-steps/turn) at FIXED (g, delta, L); selection cadence and memory window
held fixed. n=1 is the original model.

    P=1.0 L=40 : alpha* = 1.95 for n=1,2,4,8,16,32   (flat)
    P=1.0 L=80 : alpha* = 1.45 -> 1.50               (one grid cell)
    P=0.5 L=40 : alpha* = 0.85 for all n             (flat)

alpha* is INVARIANT to the resource timestep. Euler at n=1 already agrees with n=32 (g is
small, per-turn resource step tiny). => resource-discretization error is ~zero. The residual
is NOT numerical.

SYNTHESIS (this MERGES 3c and 3d): refining the resource timestep does nothing (B); varying
L moves alpha* a lot (A). Therefore the L-dependence at fixed P is REAL and STRUCTURAL.
L is the selection-memory window = the selection/resource CLOCK RATIO -- the SAME third clock
as 3c. At strong drive that clock produced the non-monotonic hump; at weak drive it produces
this monotone residual. They are ONE phenomenon, and it is exactly the third axis that
Result 3 already named ("surface in (g, delta, lag)"). The "residual" was never separate --
it is the curvature of that surface along a fixed-P slice. The (g*L, delta*L) collapse is
approximate precisely because it projects out the clock-ratio axis.

CANONICAL STATEMENT (quotable, REVISED):
  The fixed-P residual is structural, not numerical. Sub-stepping the resource integration
  leaves alpha* unchanged (resource-discretization error ~0), so the residual is not a
  finite-step artifact. Extending the memory window L at fixed P instead moves alpha*
  substantially and without convergence -- because that limit sends the selection/resource
  clock ratio to infinity (a singular adiabatic limit), not because of numerics. The residual
  is therefore a genuine dependence on the selection-update clock relative to resource speed:
  the same third clock that produces the strong-drive hump, here appearing at weak drive as a
  smooth monotone shift. Consequently alpha* is a function of (P, clock-ratio), not P alone;
  any quoted transition must specify the clock ratio, which is a real model parameter rather
  than a numerical knob. 3c and 3d are one mechanism.

  [HISTORY: 3d first concluded "discretization, closed" from residual.py, which looked like
  downward convergence toward alpha~1. Extending the alpha grid below 1.0 exposed that as a
  floor artifact (no convergence), and sub-stepping (method B) falsified discretization
  outright. Corrected to structural / third-clock. Two reversals; both caught by the tests.]

---

## Result 4 — repair has NO protective regime (activation threshold + subsidy, no Goldilocks)

Repair coupling strength b swept: payoff_R = 2 + b*(1-R/Rmax); repair restores rho*fR*Rmax
(rho=0.20). b=0 => flat repair (dominated, dies) = C/D baseline. alpha* = protection
threshold (min_R>1). (repair.py)

                     b:   0     0.5   1     2     4     8     16
  P=0.75 L=5   alpha*:   2.10  2.10  2.10  2.00  2.20  3.20  2.60
               <fR>:     .003  .003  .004  .006  .036  .427  .526
  P=1.0  L=5   alpha*:   2.70  2.70  2.70  2.70  2.80  5.40  None
  P=1.0  L=10  alpha*:   2.80  2.80  2.80  2.80  4.00  4.50  2.80

THREE REGIMES:
  b < 3   INERT. payoff_R at full scarcity = 2+b; cooperate = 5. Repair can only beat
          cooperate if 2+b > 5 => b > 3 (EXACT activation threshold). Below it, repair is
          dominated at all R, never selected (fR at ~0.003 mutation floor); system = C/D,
          alpha* = baseline. (The "help" at b=2 is one grid cell with fR still dead = noise.)
  3<b<~12 SUBSIDY. Repair activates, fR climbs (.036 -> .43), restores the stock, defectors
          harvest the refill (fD climbs too), alpha* inflates sharply (P1.0/L5: 2.7 -> 5.4).
          Non-monotonic, peaks ~b=8 (strong enough to refill, not to crowd D out).
  b large CELL-DEPENDENT, never good. Fast clock (P1.0/L5) -> None (unprotectable). Slower
          cells partially reverse (repair floods stock) but in a degenerate fR~.5, fD~.48,
          cooperators-extinct world.

HEADLINE: across the whole b range repair NEVER net-protects. Best case is inert; everything
above the activation threshold is subsidy or collapse. No Goldilocks strength. A scarcity-
triggered repairer is ignored until strong enough to be adopted, then feeds the exploiter it
was meant to restrain -- an oversight/bailout layer with no benign operating range, worst at
intermediate strength.

  Scope: this repairer restores the SHARED HARVESTABLE stock -> defectors eat the refill,
  which IS the subsidy mechanism. "No protective regime" is solid for THIS design; whether
  any repair design can protect is the open test (Result 4 follow-ups: rho-dependence; a
  cause-aware repair whose restoration is gated by defector density rather than scarcity).
  Caveats: single rho, mean-field, coarse b grid near activation and the high-b reversal.

## Result 4 follow-ups (repair2.py)

A1 -- rho-dependence: INCONCLUSIVE / not trustworthy. At cell P=1.0 L=5 the b=0 baseline
alpha* came out non-monotonic in rho (5.20, 5.60, 2.70, 2.70 for rho=.05,.10,.20,.40) -- yet
repair is DEAD at b=0, so rho should barely matter. That swing is the min_R metric being
fragile in this fast-clock large-amplitude oscillatory cell (deepest-trough = noisy tail
statistic). Subsidy inflation (b=8 minus b=0) trends up with rho (+0.9 at rho=.05 -> +2.7 at
rho=.20), weakly consistent with "more restoration = more subsidy", but numbers untrusted.
Needs a calmer cell or a robust protection metric before any rho law is claimed.

A2 -- cause-aware repair FAILS (the key follow-up). Gated restoration by defector density:
  none = rho*fR*Rmax ; soft = rho*fR*Rmax*(1-fD) ; hard = rho*fR*Rmax if fD<0.25 else 0.

    b      none   soft   hard       (cell P=1.0 L=5)
    0      2.70   2.70   2.70
    4      2.80   2.90   2.90
    8      5.40   5.30   5.00        subsidy essentially UNCHANGED by gating
    16     None   None   None
    diagnostics b=8: fR 0.244/0.308/0.362 (gating RAISES fR), fD 0.255/0.267/0.283

  Gating restoration by exploitation does NOT create a protective regime. It converts
  repairers from stock-refillers into non-restoring population-occupiers (fR rises because
  suppressed restoration keeps R low, keeping repair attractive). Either repair restores and
  feeds defectors, or it does not restore and is dead weight while defectors drain unchecked.
  => RESTORATION-CLASS repair has NO protective regime, gating included. The harvestable-
  refill flaw is not the whole mechanism; removing it does not help.

  SHARPENED QUESTION: every "repair" here ADDS TO THE STOCK (treats the symptom). The missing
  class is ENFORCEMENT -- suppress the defector's payoff/fitness directly (treat the cause),
  at a cost, without refilling the commons. Does enforcement-class have the protective regime
  restoration lacks? (-> Result 5)

---

## Result 5 — ENFORCEMENT protects (and eliminates defection) but collapses under its own cost

New class: strategy E suppresses defect payoff x(1-kappa*fE), pays a policing cost
(payoff_E = 5 - cost), does NOT restore the stock. Strategies C, D, E. Cell P=1.0 L=5.
(enforce.py)

E1  FREE enforcement (cost=0), sweep strength kappa:
    kappa:  0     0.5   1.0   2.0   4.0
    alpha*: 3.80  2.90  2.00  0.50  0.50      alpha* DOWN (mirror image of repair's subsidy)
    <fD>:   .170  .161  .112  .002  .002      defectors driven to the mutation floor

  Enforcement LOWERS the protection threshold and, at kappa>=2, ELIMINATES defection
  (fD -> 0.002). FIRST mechanism in the whole study to drive fD to zero in a WELL-MIXED
  population -- breaks Result 2's "defection never eliminated, only bounded" caveat.
  Suppressing the exploiter (cause) works where restoration (symptom) had no protective
  regime. Refill-vs-suppress distinction CONFIRMED.

E2  COSTLY enforcement (kappa=2), sweep policing cost:
    cost:   0.0   0.5   1.0   2.0   3.0
    alpha*: 0.50  2.50  2.60  2.60  2.60      protection LOST at cost>=0.5
    <fE>:   .499  .020  .009  .004  .003      enforcers go extinct
    <fD>:   .002  .133  .145  .135  .142      defectors return

  SECOND-ORDER FREE-RIDER PROBLEM (textbook): punishing is a public good; not-paying-for-
  police (cooperate=5) beats paying (enforce=5-cost). Any cost >= ~0.5 wipes out enforcers,
  enforcement evaporates, defection returns. Protective regime is REAL but knife-edge --
  exists only when enforcement is ~free.

  ROBUST CLAIM: only enforcement has a protective regime; restoration is inert or subsidizing.
  Enforcement uniquely eliminates defection (well-mixed) but is destroyed by its own cost via
  second-order free-riding. Lesson is not "enforce" -- it is "enforcement protects IFF the
  funding problem is solved." (-> Result 6: self-funding.) Caveats: single cell, mean-field,
  cost threshold (~0.5) parameter-specific, multiplicative suppression is one form, free
  enforcement slightly artificial (E neutral with C at kappa=0).

## Result 6 — SELF-FUNDED enforcement: a positive-cost protective regime + a new conservation law

A fraction `redist` of suppressed defector payoff is redistributed to enforcers
(payoff_E = (5-cost) + redist*loot/fE; loot = fD * confiscated defect payoff). Cell P=1.0
L=5, kappa=2. (enforce2.py)

                redist=0          redist=0.5        redist=1.0
  cost   a*  fE   fD         a*  fE   fD        a*  fE   fD   sd_fD
  0.5   2.5 .02  .13        0.5 .58  .07       0.5 .53  .03   .05
  1.0   2.6 .01  .15        2.4 .04  .15       0.5 .57  .09   .19
  2.0   2.6 .00  .14        3.1 .01  .17       2.5 .05  .16   .27
  4.0   2.6 .00  .13        2.6 .00  .15       3.1 .01  .17

Self-funding PARTIALLY solves the second-order free-rider problem. It raises the sustainable
policing-cost ceiling monotonically with redist (unfunded dies at cost>=0.5; half-funded
survives 0.5 not 1.0; fully-funded survives 1.0 not 2.0 -- funding ~doubles bearable cost)
and creates a POSITIVE-COST protective regime that unfunded enforcement never had:
  redist=1.0, cost=1.0 -> alpha*=0.50, fE=0.57, fD=0.09 (protected despite substantial cost).

NEW CONSTRAINT (the interesting part). Enforcement revenue is proportional to REMAINING
EXPLOITABLE BEHAVIOR (loot = fD * ...). As defectors are suppressed:
  fD down -> revenue down -> fE down -> defectors recover.
A self-limiting enforcement ecology: successful enforcement reduces the resource that
sustains enforcement. Near the funding ceiling this shows as oscillatory enforcer/defector
dynamics (sd_fD: 0.05 stable at cost 0.5 -> 0.19 oscillatory at cost 1.0 -> 0.27 collapsed).

NARROW CLAIM (mechanism-tied, do NOT overstate): "Within this funding architecture,
enforcement loses its revenue source as defection approaches zero." (NOT the broader
"structurally unable to drive misbehavior to zero" -- the narrow version is what the model
shows.) The funding mechanism introduces effectively a CONSERVATION LAW: oversight is no
longer an external/independent component but is dynamically coupled to the amount of
exploitable behavior left. Oversight and exploitation become linked populations.

ARC INTERPRETATION (Results 4-6):
  Restoration fails -- it replenishes what exploiters consume.
  Unfunded enforcement fails -- oversight is a public good (2nd-order free-riding).
  Self-funded enforcement succeeds by coupling oversight TO exploitation -- but that coupling
  makes enforcement depend on the persistence of the behavior it suppresses. The stable state
  is permanent low-level policing of permanent low-level defection; perfect success defunds
  itself.

  Caveats: single cell, mean-field, per-capita loot routing (low fE -> high per-enforcer
  reward is what rescues enforcers; worth a sensitivity check), ceiling values parameter-
  specific, oscillation reading suggestive not fully mapped.

---

## Result 7 — FINITE-N FERMI ROBUSTNESS: hierarchy survives ordinally, magnitudes do not

Kill-test: finite-population stochastic Fermi (pairwise imitation) update -- drops BOTH
mean-field AND replicator. Same commons. (robust.py / robust2.py)

INITIAL ARTIFACT: without recruitment, demographic noise drove R to exactly 0; logistic
regen has an ABSORBING boundary at R=0 (regen = g*R*(...) = 0 there), so the resource could
not recover, and this dominated/masked the test (all conditions uniform except repair, whose
R-independent restoration escaped the trap). A small constant recruitment (s0=1.0/turn) was
added to prevent the zero-resource absorbing state from swamping the comparison.

WITH RECRUITMENT (N=500, a=2.0, g=delta=0.20, kappa=2, cost=1, redist=1; 3 seeds):
  baseline C/D              mean_fD=0.206  mean_R=40.6
  repair b=8                mean_fD=0.420  mean_R=55.9              (fD UP)
  unfunded enforce cost=1   mean_fD=0.206  mean_R=40.6  fE=0.007    (enforcers extinct)
  self-funded   cost=1      mean_fD=0.210  mean_R=70.2  fE=0.216    (enforcers persist, R up)

SURVIVES (ordinal hierarchy is NOT a mean-field artifact):
  - Repair still SUBSIDIZES: raises R but raises fD (0.21->0.42); restoration feeds exploiters.
  - Unfunded enforcement still COLLAPSES: enforcers ~extinct under cost, system = baseline.
  - Self-funded enforcement still PERSISTS: redistribution sustains fE at positive cost and
    raises mean R substantially, even under stochastic finite-N + non-replicator selection.

DOES NOT SURVIVE (mean-field magnitudes are artifacts):
  - Defection ELIMINATION: mean-field drove fD->0.002; finite-N Fermi holds fD~0.21 (barely
    below baseline). Enforcers improve R but do NOT crush defection. Result 5's "first
    mechanism to eliminate fD in well-mixed" is replicator-specific. Direction right, magnitude gone.
  - Clean deterministic thresholds: softened/washed out by stochasticity.

NEW FINITE-N COLLAPSE MODE: noise-induced resource extinction. R=0 is absorbing; demographic
noise reaches it; without recruitment the commons dies permanently regardless of intervention.
Absent from mean-field. min_R=0.0 in every condition even here -- protective regimes graze the floor.

OPEN PUZZLE: self-funded has ~baseline mean_fD (0.21) yet much higher R (70 vs 41). Same mean
defector load should give same harvest. Tentative: enforcement damps fD VARIANCE (slows
defector booms), so R isn't drawn down as hard at peaks. Needs the fD time series to confirm.

VERDICT: the intervention hierarchy is not merely a mean-field replicator artifact, but its
dramatic magnitudes are. Survives: repair subsidizes, unfunded enforcement collapses,
self-funded enforcement persists & improves resource outcomes. Does not: defection
elimination, clean thresholds. Remaining robustness axis = spatial structure (most likely to
change the ORDERING, not just soften it).

---

## Result 8 — SPATIAL ROBUSTNESS: hierarchy survives; spatial reciprocity alone does NOT protect

Lattice (50x50), each cell a local resource patch + occupant strategy; local depletion by
defectors, optional resource diffusion, LOCAL Fermi imitation (neighbors only). Enforcement
suppression and self-funding are LOCAL (neighborhood). (spatial.py, spatial_diff.py)

a=2, g=0.30, delta=0.10(local), rho=0.15, kappa=2, cost=1, redist=1; 2 seeds. Ddiff=0.15:
  condition              fD     meanR   f2     R@D    R@C    assort
  baseline C/D          0.633   67.4   0.175   63.6   73.9   0.737
  repair b=8            0.666   66.6   0.018   63.1   73.5   0.773
  unfunded enforce c=1  0.594   70.0   0.058   64.9   78.7   0.774
  self-funded c=1       0.260   88.9   0.274   75.0   97.8   0.764

Diffusion sweep (baseline vs self-funded):
  Ddiff:        0.00   0.02   0.05   0.15   0.40
  baseline fD:  0.600  0.619  0.623  0.633  0.007(degenerate ~all-C, R smoothed flat)
  selffund fD:  0.260  0.260  0.265  0.260  0.007
  selffund f2:  0.260  0.263  0.269  0.274  0.002

FINDINGS:
  - Strong clustering everywhere (assort ~0.76 vs 0.33 random); defectors sit on poorer
    patches (R@D < R@C). Spatial self-limiting PRESENT but partial.
  - Intervention hierarchy SURVIVES ordinally and robustly across diffusion: repair
    subsidizes (fD up, repairers ~die), unfunded enforcement collapses (enforcers ~extinct),
    self-funded enforcement protects -- MORE strongly than well-mixed (fD 0.63->0.26,
    R 67->89), because clustering co-localizes suppression AND loot-funding.
  - NEW / counterintuitive: spatial structure ALONE does NOT rescue cooperation here. Even at
    Ddiff=0 (independent patches, max spatial reciprocity) baseline fD ~0.60. Nowak-May
    reciprocity is too weak in this resource-coupled model -- the protective work is done by
    ENFORCEMENT, not spatial assortment. Space helps the mechanism that already worked; it
    does not substitute for it.

COMBINED ROBUSTNESS VERDICT (7+8): ordinal hierarchy (repair fails / unfunded collapses /
self-funded protects) holds across mean-field, finite-N stochastic Fermi, AND spatial
local-interaction + diffusion. Mean-field MAGNITUDES (elimination, sharp thresholds) do not
survive. Most robust single result: self-funded enforcement protects in EVERY ecology.

---

## Result 9 — THE SPINE: protection survives iff its return is EXCLUDABLE (mechanism discrimination)

Held suppression mechanism AND total confiscated loot FIXED; varied ONLY the recipient of the
loot. Cell P=1.0 L=5, kappa=2, cost=1, redist=1. (discriminate.py)

  scheme        min_R   <fE>   <fD>
  unfunded       0.0    0.008  0.002    enforcers dead, R collapsed
  selffund      47.8    0.479  0.107    LIVES, protected
  pooled_all     0.0    0.008  0.002    enforcers dead
  pooled_CE      0.0    0.008  0.002    enforcers dead   (loot to C+E only, not D)

ONLY private (per-enforcer) funding survives. Both pooled schemes collapse identically to
unfunded. This discriminates the three candidate principles:

  C  FUNDING ALIGNMENT -- CONFIRMED, and the reason is an IDENTITY, not a fit:
       pooled adds the same share to C and E, so it CANCELS in the comparison that decides
       enforcer persistence:  pE - pC = (5 - cost + share) - (5 + share) = -cost  (any share).
       Cooperators free-ride on redistribution exactly as much as enforcers -> enforcers stay
       a cost behind -> extinct. Self-funding: pE - pC = -cost + private_reward > 0. The sim
       confirms the algebra. Ecology-independent (holds in finite-N / spatial for same reason).
  B  CAUSE vs SYMPTOM -- REFUTED as sufficient: every scheme has IDENTICAL suppression; only
       enforcer persistence differs. Acting on the exploiter does nothing if the actor can't
       survive.
  A  RESOURCE COUPLING -- no signal here: pooled_all == pooled_CE (funding collapse precedes
       any defector-subsidy difference).

THE PRINCIPLE (unifies Results 4-8 in one line):
  A protective mechanism survives IFF its benefit is an EXCLUDABLE PRIVATE RETURN captured by
  the agents performing it. Producing a NON-EXCLUDABLE good (one free-riders also enjoy)
  collapses the protector.
    - Repair fails: restored shared stock is non-excludable; defectors consume it (subsidy).
    - Unfunded enforcement fails: suppression is a public good paid for privately.
    - Pooled enforcement fails: redistribution benefits cooperators too -> enforcers stay
      cost-disadvantaged (the -cost identity).
    - Self-funded enforcement works: confiscated payoff goes specifically to enforcers ->
      protection is privately sustainable.
  "Funding alignment" = excludability on the cost side. "Cause vs symptom" was a red herring:
  both repair and enforcement can target the right thing and still fail if the return is not
  excludable. The deep variable is WHO CAN BE EXCLUDED FROM THE BENEFIT of the protective act.

TAKEAWAY: The system does not stabilize because bad actors vanish. It stabilizes when the
architecture makes PROTECTION ITSELF evolutionarily viable.

---

## Sequence status: CLOSED (3c & 3d unified)

  1   delta/g falsified as control variable.                              [solid]
  2   (g*L, delta*L) collapses resilience in weak regime (leading order). [solid, approx]
  2b  scarcity-triggered repair inverts protective -> subsidizing.        [solid, qualitative]
  3   transition is a SURFACE; the third axis is the clock ratio.         [solid]
  3c+3d  ONE mechanism -- the unscaled selection/resource clock ratio.    [established, in-model]
      Strong drive: non-monotonic hump (removed by clock-tying; a separate
      control-gain instability appears only at high gain). Weak drive:
      monotone fixed-P "residual". NOT discretization (sub-stepping is null).
      => alpha* = f(P, clock-ratio); quote both coordinates, never P alone.
  4   repair has NO protective regime: inert (b<3) or subsidy/collapse (b>3); [solid, in-model]
      exact activation threshold b>3; subsidy peaks ~b=8; no Goldilocks. Holds
      for shared-harvestable-stock repair; cause-aware gating also fails (A2).
  5   ENFORCEMENT (suppress the exploiter) is the only protective class:      [solid, in-model]
      lowers alpha*, uniquely eliminates fD in well-mixed -- BUT collapses under
      its own cost via 2nd-order free-riding (dies at cost>=~0.5). Protects iff
      the funding problem is solved (-> Result 6 self-funding).
  6   SELF-FUNDED enforcement: positive-cost protective regime exists;          [solid, in-model]
      funding ~doubles bearable cost. New conservation law -- revenue ~ remaining
      exploitable behavior, so suppressing defection starves enforcement
      (self-limiting; oscillatory near ceiling). Oversight & exploitation = coupled
      populations. Narrow claim: loses revenue as fD->0 within THIS architecture.
  7   ROBUSTNESS (finite-N + Fermi): intervention hierarchy survives ORDINALLY  [tested]
      (repair subsidizes / unfunded collapses / self-funded persists & raises R),
      but mean-field MAGNITUDES do NOT (no defection elimination; thresholds wash
      out). New finite-N mode: noise-induced resource extinction (R=0 absorbing).
  8   ROBUSTNESS (spatial lattice + diffusion): hierarchy survives ordinally       [tested]
      across all diffusion; self-funded protects MORE strongly (clustering co-locates
      suppression+funding). NEW: spatial reciprocity ALONE does not rescue cooperation
      (baseline fD~0.60 even at Ddiff=0) -- enforcement does the work, not assortment.
  9   THE SPINE -- protection survives IFF its return is EXCLUDABLE (private to the      [solid;
      protector). Mechanism discrimination: only self-funding survives; both pooled        identity-
      schemes collapse to unfunded via the identity pE-pC=-cost. Refutes cause-vs-          backed]
      symptom as sufficient; unifies repair-fails / unfunded-fails / self-funded-works.
      => "the system stabilizes when the architecture makes PROTECTION itself viable."

---

## Caveats (do not oversell)

- Deterministic mean-field, single configuration; no spatial structure / assortment.
  In well-mixed form defection is never *eliminated* at any alpha, only damage-bounded.
- Regime labels use arbitrary classifier thresholds; any individual alpha* is +/-1 grid
  cell. The ratio-falsification spread (1.0..None) is far larger than one cell, so
  Result 1 is robust; exact alpha* numbers and the (a)/(b) residual structure are softer.
- The resonance reading (3b) is a hypothesis, NOT yet shown. Discriminating test:
  measure oscillation period tau at the P=1.5 cells (peak-spacing / FFT on the R trace)
  and check whether the alpha* hump tracks tau/lag hitting a small-integer ratio.

## Result 10 — EXCLUDABILITY IS A CONTROL PARAMETER (ecology-invariant directional law)

The recipient-swap of Result 9 was all-or-nothing (private vs pooled). Result 10 makes the
private fraction continuous: r = fraction of confiscated payoff routed PRIVATELY to enforcers;
(1-r) pooled to everyone. Same suppression, same total extraction; only r changes.
(excludability.py, excludability_finiteN.py, excludability_spatial.py)

                MEAN-FIELD          FINITE-N FERMI       SPATIAL LATTICE
  r       fE     regime         fE     R              fE     fD     R
  0.0    .008    collapse      .007   40.6           .029   .615   68
  0.2    .008    collapse      .018   42.4           .124   .517   75
  0.4    .008    collapse      .062   51.0           .247   .326   86
  0.6    .008    collapse      .100   56.8           .250   .299   87
  0.8    .389    IGNITE        .159   63.5           .267   .268   89
  1.0    .479    protected     .216   70.2           .274   .260   89

FINDING: across all three ecologies, raising the private fraction r monotonically increases
enforcer persistence and resource health and decreases defection. The DIRECTION is invariant.

SHARP vs SOFT (the honest correction): mean-field shows a clean PHASE TRANSITION -- nothing
until r*~0.8, then ignition. Finite-N and spatial SOFTEN it into a monotone RAMP (enforcers
lift off by r~0.4, no snap). This is the same mean-field-sharpens / noise-rounds pattern as
Result 7. So the robust claim is NOT "there is a critical threshold r*=0.8" -- that exact
value dissolves under noise. The robust claim is DIRECTIONAL and ecology-invariant.

ROBUST CLAIM (the strongest single statement in the repo):
  Coupling consequences back to the actor that generated them systematically increases the
  persistence of protective behavior -- across mean-field, finite-N stochastic, and spatial
  ecologies. Protection does not scale with how much value is recovered; it scales with how
  much of that value remains coupled (excludably) to the protector.

  This reframes the whole intervention arc: the operative variable is the RETURN PATHWAY --
  what fraction of the consequence of a protective act stays bonded to its performer. Result 9
  (excludability) is the r=0 vs r=1 endpoints; Result 10 is the full axis between them.
  Caveat: r* is parameter-dependent (moves with cost/kappa); the threshold STRUCTURE and the
  directional dependence are the results, not the number 0.8.

---

## Open leads (the hunt)

  ROBUSTNESS PROGRAM COMPLETE (Results 7 + 8): hierarchy survives mean-field, finite-N Fermi,
  spatial + diffusion. No longer a single-model curiosity. Stop adding ecologies.

  ACTIVE -- MECHANISM DISCRIMINATION (Result 9). Three candidate principles for WHY the
  hierarchy survives:
    A. Resource Coupling: adding to a shared/accessible pool creates exploitable surplus.
    B. Cause vs Symptom: act on the exploiter (works) vs on the state variable (fails).
    C. Funding Alignment: protection survives only if its maintenance cost is privately
       coupled to the regulated thing (enforcers funded directly).
  Discriminator: TAX-AND-REDISTRIBUTE enforcement -- tax defector payoff, pool it, redistribute
    EQUALLY to everyone (vs self-funded = to enforcers only). Predictions:
      C true -> self-funded survives, pooled COLLAPSES (enforcers lose private incentive;
                redistribution cancels out of the C-vs-E comparison -> still -cost).
      B true -> both work (both suppress D) -- requires enforcers to persist under pooling.
      A true -> pooling to all (incl. defectors) acts as a subsidy, resembling repair.
  SYNTHESIS drafted (SYNTHESIS.md); update after Result 9 with the operative principle.
  B(law). The 2D law alpha* = f(P, clock-ratio): characterize the surface (Thread I).

## Files

- sweep2.py / sweep2.log         — alpha sweep, flat vs coupled repair (Results 2b seed)
- lagsweep.py / lagsweep.log     — lag sweep + (delta*lag, g*lag) collapse test (Result 2)
- densegroup.py / densegroup.log — dense product sweep (Result 3)
- period.py / period.log         — oscillation-period measurement at P=1.5 (Result 3c, falsified #1)
- robust_astar.py / robust_astar.log — alpha* under 3 criteria + long runs (Result 3c, falsified #2)
- timescale.py / timescale.log    — clock-tying test (Result 3c, third-clock supported + residual split)
- gainsweep.py / gainsweep.log    — gain sweep (Result 3c, third-clock established; gain effect isolated)
- residual.py / residual.log      — fixed-P L-extension, first pass (Result 3d history)
- continuum.py / continuum.log, continuum2.py / continuum2.log — L-extension below alpha=1 (singular limit)
- substep.py / substep.log        — resource sub-stepping (Result 3d, falsifies discretization; residual = structural)
- repair.py / repair.log          — repair-coupling sweep (Result 4, repair phase diagram)
- repair2.py / repair2.log        — rho-dependence (A1, inconclusive) + cause-aware gating (A2, fails)
- enforce.py / enforce.log        — enforcement class (Result 5: protective but cost-fragile)
- enforce2.py / enforce2.log      — self-funded enforcement (Result 6: positive-cost regime + conservation law)
- robust.py / robust.log, robust2.py / robust2.log — finite-N Fermi kill-test (Result 7)
- spatial.py / spatial.log, spatial_diff.py / spatial_diff.log — spatial lattice + diffusion (Result 8)
- discriminate.py / discriminate.log — mechanism discrimination (Result 9: excludability principle)
- excludability.py / .log — excludability sweep, mean-field (Result 10: sharp transition r*~0.8)
- excludability_finiteN.py / .log — finite-N Fermi r-sweep (Result 10: softened ramp)
- excludability_spatial.py / .log — spatial lattice r-sweep (Result 10: directional law survives)
- SYNTHESIS.md                   — narrative tying Results 1-9 to the original question
- FINDINGS.md                    — this file

The 2D (g, delta) sweep that produced Result 1's table was run separately (script on
local machine); its CSVs are flat_repair_sweep_results.csv / coupled_repair_sweep_results.csv.
