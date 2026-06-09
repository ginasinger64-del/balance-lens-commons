import React, { useState, useEffect, useMemo, useRef } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
  ReferenceLine, AreaChart, Area, Tooltip,
} from "recharts";

// ---- palette ---------------------------------------------------------------
const INK = "#11151B";
const PANEL = "#181E27";
const PANEL2 = "#1E2630";
const RULE = "#2B3440";
const TXT = "#E9EEF4";
const MUT = "#8B97A6";
const COOP = "#5BBF90";   // Cooperate — calm green
const DEF = "#E2564B";    // Defect — warning red
const ENF = "#D9A441";    // Enforce — gold, the protector
const RES = "#4F8FB0";    // Resource — cool slate-cyan

const MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace";
const SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

// ---- the model (ported verbatim from enforce.py / enforce2.py) -------------
function simulate(mode, cost, gens = 100) {
  const Rmax = 100, eps = 0.005, a = 2.0, g = 0.20, delta = 0.20, kappa = 2.0;
  const redist = mode === "selffund" ? 1.0 : 0.0;
  let fC = 1 / 3, fD = 1 / 3, fE = 1 / 3, R = Rmax;
  const win = [];
  const traj = [{ gen: 0, C: fC, D: fD, E: fE, R }];
  for (let t = 0; t < gens; t++) {
    const base = 12 * Math.pow(R / Rmax, a);
    const sup = Math.min(Math.max(kappa * fE, 0), 1);     // suppression of defect payoff
    const loot = fD * base * sup;                          // total confiscated
    const pC = 5;
    const pD = base * (1 - sup);
    let pE = 5 - cost;
    if (redist > 0 && fE > 1e-9) pE += redist * loot / fE; // self-funding: loot → enforcers
    win.push([pC, pD, pE]);
    if (win.length > 5) win.shift();
    let rC = 0, rD = 0, rE = 0;
    for (const w of win) { rC += w[0]; rD += w[1]; rE += w[2]; }
    const n = win.length; rC /= n; rD /= n; rE /= n;        // recent-payoff average
    R = R + g * R * (1 - R / Rmax) - delta * fD * Rmax;     // logistic regen − harvest
    if (R < 0) R = 0; if (R > Rmax) R = Rmax;
    const avg = fC * rC + fD * rD + fE * rE;                // replicator on recent payoff
    fC = fC * rC / avg; fD = fD * rD / avg; fE = fE * rE / avg;
    fC = (1 - eps) * fC + eps / 3; fD = (1 - eps) * fD + eps / 3; fE = (1 - eps) * fE + eps / 3;
    const s = fC + fD + fE; fC /= s; fD /= s; fE /= s;
    traj.push({ gen: t + 1, C: fC, D: fD, E: fE, R });
  }
  return traj;
}

const GENS = 100;
const fmtPct = (x) => (x * 100).toFixed(1) + "%";

const MODES = {
  unfunded: {
    label: "Unfunded",
    mechanism: "confiscated payoff → discarded",
    note: "Enforcers pay the cost. Everyone shares the benefit.",
  },
  selffund: {
    label: "Self-funded",
    mechanism: "confiscated payoff → enforcers",
    note: "The return to enforcing is captured privately by enforcers.",
  },
};

export default function CommonsDashboard() {
  const [mode, setMode] = useState("unfunded");
  const [cost, setCost] = useState(1.0);
  const [head, setHead] = useState(0);
  const [playing, setPlaying] = useState(true);
  const timer = useRef(null);

  const reduceMotion = useMemo(
    () => typeof window !== "undefined" &&
      window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    []
  );

  const traj = useMemo(() => simulate(mode, cost, GENS), [mode, cost]);

  // recompute → restart playback whenever the model changes
  useEffect(() => {
    if (reduceMotion) { setHead(GENS); setPlaying(false); return; }
    setHead(0); setPlaying(true);
  }, [mode, cost, reduceMotion]);

  useEffect(() => {
    if (!playing) return;
    if (head >= GENS) { setPlaying(false); return; }
    timer.current = setTimeout(() => setHead((h) => Math.min(h + 1, GENS)), 45);
    return () => clearTimeout(timer.current);
  }, [playing, head]);

  const shown = traj.slice(0, head + 1);
  const cur = traj[head] || traj[traj.length - 1];
  const done = head >= GENS;
  const finalE = traj[GENS].E;
  const protectedOutcome = finalE >= 0.05;

  const restart = () => { setHead(0); setPlaying(true); };
  const toggle = () => {
    if (done) { restart(); return; }
    setPlaying((p) => !p);
  };

  return (
    <div style={{ background: INK, color: TXT, fontFamily: SANS, minHeight: "100%" }}>
      <div style={{ maxWidth: 960, margin: "0 auto", padding: "28px 20px 40px" }}>

        {/* header */}
        <div style={{ fontFamily: MONO, fontSize: 11, letterSpacing: "0.22em",
          color: ENF, textTransform: "uppercase", marginBottom: 10 }}>
          Commons dynamics · live model
        </div>
        <h1 style={{ fontSize: 30, lineHeight: 1.1, fontWeight: 700, margin: "0 0 8px",
          letterSpacing: "-0.02em" }}>
          Does protection survive its own dynamics?
        </h1>
        <p style={{ color: MUT, margin: "0 0 22px", maxWidth: 620, fontSize: 15 }}>
          Three strategies compete on a regenerating commons. Enforcers suppress defectors
          but pay a cost. Flip how that cost is funded and watch the enforcer population
          live or die over {GENS} generations.
        </p>

        {/* controls */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 16, alignItems: "stretch",
          marginBottom: 20 }}>
          {/* mode switch */}
          <div style={{ background: PANEL, border: `1px solid ${RULE}`, borderRadius: 12,
            padding: 6, display: "flex", gap: 4, flex: "1 1 360px" }}>
            {Object.entries(MODES).map(([key, m]) => {
              const active = mode === key;
              return (
                <button key={key} onClick={() => setMode(key)}
                  style={{
                    flex: 1, textAlign: "left", cursor: "pointer",
                    background: active ? PANEL2 : "transparent",
                    border: active ? `1px solid ${ENF}55` : "1px solid transparent",
                    borderRadius: 9, padding: "10px 12px", color: active ? TXT : MUT,
                    transition: "all .15s",
                  }}>
                  <div style={{ fontSize: 14, fontWeight: 700 }}>{m.label}</div>
                  <div style={{ fontFamily: MONO, fontSize: 10.5,
                    color: active ? ENF : MUT, marginTop: 2 }}>{m.mechanism}</div>
                </button>
              );
            })}
          </div>

          {/* playback + cost */}
          <div style={{ background: PANEL, border: `1px solid ${RULE}`, borderRadius: 12,
            padding: "10px 14px", flex: "1 1 280px", display: "flex",
            flexDirection: "column", justifyContent: "center", gap: 10 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <button onClick={toggle}
                style={{ cursor: "pointer", background: ENF, color: INK, border: "none",
                  borderRadius: 8, padding: "7px 16px", fontWeight: 700, fontSize: 13,
                  minWidth: 84 }}>
                {done ? "Replay" : playing ? "Pause" : "Play"}
              </button>
              <button onClick={restart}
                style={{ cursor: "pointer", background: "transparent", color: MUT,
                  border: `1px solid ${RULE}`, borderRadius: 8, padding: "7px 14px",
                  fontSize: 13 }}>
                Reset
              </button>
              <div style={{ fontFamily: MONO, fontSize: 12, color: MUT, marginLeft: "auto" }}>
                gen <span style={{ color: TXT }}>{String(head).padStart(3, "0")}</span>/{GENS}
              </div>
            </div>
            <label style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 12,
              color: MUT }}>
              <span style={{ whiteSpace: "nowrap" }}>Enforcement cost</span>
              <input type="range" min={0} max={3} step={0.1} value={cost}
                onChange={(e) => setCost(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: ENF }} />
              <span style={{ fontFamily: MONO, color: TXT, minWidth: 28 }}>{cost.toFixed(1)}</span>
            </label>
          </div>
        </div>

        {/* main grid */}
        <div style={{ display: "grid", gap: 16,
          gridTemplateColumns: "minmax(0, 1.55fr) minmax(0, 1fr)" }}>

          {/* population chart */}
          <Panel title="Population" sub="share of agents by strategy">
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={shown} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}>
                <CartesianGrid stroke={RULE} strokeDasharray="2 4" vertical={false} />
                <XAxis dataKey="gen" type="number" domain={[0, GENS]}
                  tick={{ fill: MUT, fontSize: 11, fontFamily: MONO }} stroke={RULE} />
                <YAxis domain={[0, 1]} tickFormatter={(v) => Math.round(v * 100)}
                  tick={{ fill: MUT, fontSize: 11, fontFamily: MONO }} stroke={RULE} />
                <Tooltip
                  contentStyle={{ background: PANEL2, border: `1px solid ${RULE}`,
                    borderRadius: 8, fontFamily: MONO, fontSize: 12 }}
                  labelStyle={{ color: MUT }}
                  formatter={(v, n) => [fmtPct(v), n]} labelFormatter={(l) => "gen " + l} />
                <Line dataKey="C" name="Cooperate" stroke={COOP} strokeWidth={2}
                  dot={false} isAnimationActive={false} />
                <Line dataKey="D" name="Defect" stroke={DEF} strokeWidth={2}
                  dot={false} isAnimationActive={false} />
                <Line dataKey="E" name="Enforce" stroke={ENF} strokeWidth={2.6}
                  dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
            <Legend />
          </Panel>

          {/* live readout + verdict */}
          <Panel title="Readout" sub="current state">
            <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
              <Stat color={COOP} label="Cooperate" value={fmtPct(cur.C)} />
              <Stat color={DEF} label="Defect" value={fmtPct(cur.D)} />
              <Stat color={ENF} label="Enforce" value={fmtPct(cur.E)} big />
              <Stat color={RES} label="Resource" value={cur.R.toFixed(1)} />
            </div>
            <div style={{
              marginTop: 14, padding: "12px 14px", borderRadius: 10,
              background: done ? (protectedOutcome ? "#13251C" : "#2A1714") : PANEL2,
              border: `1px solid ${done ? (protectedOutcome ? COOP + "55" : DEF + "55") : RULE}`,
              minHeight: 84,
            }}>
              <div style={{ fontFamily: MONO, fontSize: 10.5, letterSpacing: "0.16em",
                textTransform: "uppercase", color: MUT, marginBottom: 6 }}>
                {done ? "Verdict" : "Running…"}
              </div>
              {done ? (
                <div style={{ fontSize: 13.5, lineHeight: 1.45 }}>
                  {protectedOutcome ? (
                    <span><b style={{ color: COOP }}>Enforcers persisted.</b> Defection held
                      to {fmtPct(traj[GENS].D)}, resource at {traj[GENS].R.toFixed(0)}. The
                      return to protection was captured privately.</span>
                  ) : (
                    <span><b style={{ color: DEF }}>Enforcers went extinct.</b> The benefit
                      was shared but the cost was not — cooperators free-rode, and protection
                      collapsed back to baseline.</span>
                  )}
                </div>
              ) : (
                <div style={{ fontSize: 13, color: MUT }}>{MODES[mode].note}</div>
              )}
            </div>
          </Panel>
        </div>

        {/* resource area */}
        <div style={{ marginTop: 16 }}>
          <Panel title="Resource level" sub="the shared stock, regenerating and harvested">
            <ResponsiveContainer width="100%" height={130}>
              <AreaChart data={shown} margin={{ top: 6, right: 8, left: -18, bottom: 0 }}>
                <defs>
                  <linearGradient id="resfill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={RES} stopOpacity={0.55} />
                    <stop offset="100%" stopColor={RES} stopOpacity={0.04} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke={RULE} strokeDasharray="2 4" vertical={false} />
                <XAxis dataKey="gen" type="number" domain={[0, GENS]}
                  tick={{ fill: MUT, fontSize: 11, fontFamily: MONO }} stroke={RULE} />
                <YAxis domain={[0, 100]}
                  tick={{ fill: MUT, fontSize: 11, fontFamily: MONO }} stroke={RULE} />
                <Area dataKey="R" stroke={RES} strokeWidth={2} fill="url(#resfill)"
                  isAnimationActive={false} />
              </AreaChart>
            </ResponsiveContainer>
          </Panel>
        </div>

        {/* footnote */}
        <p style={{ color: MUT, fontSize: 12, lineHeight: 1.5, marginTop: 22,
          borderTop: `1px solid ${RULE}`, paddingTop: 14 }}>
          Toy model — a minimal recent-payoff replicator on a logistically regenerating
          resource (α=2, g=δ=0.20, κ=2, 5-step memory). Live equations, not a recording.
          The ordering shown here survives finite-N stochastic and spatial versions; specific
          numbers are model-dependent and carry no claim about real systems. Tip: slide the
          enforcement cost up under <i>Unfunded</i> to watch the collapse threshold, then flip
          to <i>Self-funded</i> at the same cost.
        </p>
      </div>
    </div>
  );
}

// ---- small components ------------------------------------------------------
function Panel({ title, sub, children }) {
  return (
    <div style={{ background: PANEL, border: `1px solid ${RULE}`, borderRadius: 12,
      padding: 16 }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 10 }}>
        <span style={{ fontSize: 13, fontWeight: 700 }}>{title}</span>
        <span style={{ color: MUT, fontSize: 11.5 }}>{sub}</span>
      </div>
      {children}
    </div>
  );
}

function Stat({ color, label, value, big }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10,
      padding: "7px 0", borderBottom: `1px solid ${RULE}` }}>
      <span style={{ width: 9, height: 9, borderRadius: 2, background: color,
        flexShrink: 0 }} />
      <span style={{ color: MUT, fontSize: 13 }}>{label}</span>
      <span style={{ marginLeft: "auto", fontFamily: MONO, color: "#fff",
        fontSize: big ? 18 : 14, fontWeight: big ? 700 : 500 }}>{value}</span>
    </div>
  );
}

function Legend() {
  const items = [["Cooperate", COOP], ["Defect", DEF], ["Enforce", ENF]];
  return (
    <div style={{ display: "flex", gap: 16, marginTop: 8, flexWrap: "wrap" }}>
      {items.map(([l, c]) => (
        <span key={l} style={{ display: "flex", alignItems: "center", gap: 6,
          fontSize: 12, color: MUT }}>
          <span style={{ width: 14, height: 3, borderRadius: 2, background: c }} />{l}
        </span>
      ))}
    </div>
  );
}
