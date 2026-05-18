import { useState, useEffect, useRef, useCallback } from "react";

// ─── UTILS ───────────────────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// ─── N-QUEENS ────────────────────────────────────────────────────────────────

function isSafeQueen(board, row, col, n) {
  for (let i = 0; i < row; i++) {
    if (board[i] === col) return false;
    if (Math.abs(board[i] - col) === Math.abs(i - row)) return false;
  }
  return true;
}

function solveNQueens(n) {
  const solutions = [];
  const board = Array(n).fill(-1);
  function solve(row) {
    if (row === n) { solutions.push([...board]); return; }
    for (let col = 0; col < n; col++) {
      if (isSafeQueen(board, row, col, n)) {
        board[row] = col;
        solve(row + 1);
        board[row] = -1;
      }
    }
  }
  solve(0);
  return solutions;
}

// ─── KNIGHT'S TOUR ───────────────────────────────────────────────────────────

const KNIGHT_MOVES = [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]];

function solveKnightTour(n, startR, startC) {
  const board = Array.from({ length: n }, () => Array(n).fill(-1));
  const path = [];
  board[startR][startC] = 0;
  path.push([startR, startC]);

  function warnsdorff(r, c) {
    return KNIGHT_MOVES
      .map(([dr, dc]) => [r + dr, c + dc])
      .filter(([nr, nc]) => nr >= 0 && nr < n && nc >= 0 && nc < n && board[nr][nc] === -1)
      .map(([nr, nc]) => ({
        r: nr, c: nc,
        deg: KNIGHT_MOVES.filter(([dr, dc]) => {
          const rr = nr + dr, cc = nc + dc;
          return rr >= 0 && rr < n && cc >= 0 && cc < n && board[rr][cc] === -1;
        }).length
      }))
      .sort((a, b) => a.deg - b.deg);
  }

  let r = startR, c = startC;
  for (let move = 1; move < n * n; move++) {
    const nexts = warnsdorff(r, c);
    if (nexts.length === 0) return null;
    const { r: nr, c: nc } = nexts[0];
    board[nr][nc] = move;
    path.push([nr, nc]);
    r = nr; c = nc;
  }
  return path;
}

// ─── KNAPSACK ────────────────────────────────────────────────────────────────

function solveKnapsack(weights, target) {
  const steps = [];
  let bestCombo = null;
  let bestTotal = 0;

  function recurse(idx, current, chosen) {
    const total = current.reduce((s, w) => s + w, 0);
    steps.push({ chosen: [...chosen], total, idx, phase: "try" });

    if (total === target) {
      steps.push({ chosen: [...chosen], total, idx, phase: "exact" });
      if (bestCombo === null) bestCombo = [...chosen];
      return true;
    }
    if (total > target || idx >= weights.length) {
      steps.push({ chosen: [...chosen], total, idx, phase: "backtrack" });
      return false;
    }

    // include
    chosen.push(weights[idx]);
    current.push(weights[idx]);
    if (recurse(idx + 1, current, chosen)) return true;
    current.pop(); chosen.pop();

    // exclude
    if (recurse(idx + 1, current, chosen)) return true;

    steps.push({ chosen: [...chosen], total, idx, phase: "backtrack" });
    return false;
  }

  recurse(0, [], []);
  return { steps, bestCombo };
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────

export default function App() {
  const [tab, setTab] = useState("queens");

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0f",
      fontFamily: "'Courier New', monospace",
      color: "#e2e8f0",
      padding: "0",
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        borderBottom: "2px solid #e94560",
        padding: "24px 32px",
        display: "flex",
        alignItems: "center",
        gap: "16px",
      }}>
        <div style={{ fontSize: "28px" }}>⚙️</div>
        <div>
          <div style={{ fontSize: "22px", fontWeight: "bold", color: "#e94560", letterSpacing: "3px", textTransform: "uppercase" }}>
            REKURSIF & BACKTRACKING
          </div>
          <div style={{ fontSize: "11px", color: "#94a3b8", letterSpacing: "2px" }}>
            VISUALISASI ALGORITMA INTERAKTIF
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: "1px solid #1e293b", background: "#0d1117" }}>
        {[
          { id: "queens", label: "♛ N-Queens", color: "#f59e0b" },
          { id: "knight", label: "♞ Knight's Tour", color: "#10b981" },
          { id: "knapsack", label: "🎒 Knapsack", color: "#8b5cf6" },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              flex: 1,
              padding: "14px",
              border: "none",
              background: tab === t.id ? "#1e293b" : "transparent",
              color: tab === t.id ? t.color : "#64748b",
              fontFamily: "inherit",
              fontSize: "13px",
              fontWeight: "bold",
              letterSpacing: "1px",
              cursor: "pointer",
              borderBottom: tab === t.id ? `2px solid ${t.color}` : "2px solid transparent",
              transition: "all 0.2s",
            }}
          >{t.label}</button>
        ))}
      </div>

      <div style={{ padding: "24px" }}>
        {tab === "queens" && <NQueensTab />}
        {tab === "knight" && <KnightTab />}
        {tab === "knapsack" && <KnapsackTab />}
      </div>
    </div>
  );
}

// ─── N-QUEENS TAB ─────────────────────────────────────────────────────────────

function NQueensTab() {
  const [n, setN] = useState(6);
  const [solutions, setSolutions] = useState([]);
  const [solutionIdx, setSolutionIdx] = useState(0);
  const [animBoard, setAnimBoard] = useState([]);
  const [animStep, setAnimStep] = useState(-1);
  const [running, setRunning] = useState(false);
  const stopRef = useRef(false);

  const solve = () => {
    const sols = solveNQueens(n);
    setSolutions(sols);
    setSolutionIdx(0);
    setAnimBoard(sols[0] || []);
    setAnimStep(-1);
  };

  const animateSolve = async () => {
    setRunning(true);
    stopRef.current = false;
    const board = Array(n).fill(-1);
    setAnimBoard([...board]);
    
    const steps = [];
    function collect(row, b) {
      if (row === n) { steps.push([...b]); return; }
      for (let col = 0; col < n; col++) {
        if (isSafeQueen(b, row, col, n)) {
          b[row] = col;
          steps.push([...b]);
          collect(row + 1, b);
          b[row] = -1;
          steps.push([...b]);
        }
      }
    }
    collect(0, board);

    for (let i = 0; i < steps.length; i++) {
      if (stopRef.current) break;
      setAnimBoard(steps[i]);
      setAnimStep(i);
      await sleep(120);
    }
    const sols = solveNQueens(n);
    setSolutions(sols);
    setSolutionIdx(0);
    setAnimBoard(sols[0] || []);
    setRunning(false);
  };

  const currentBoard = solutions.length > 0 ? solutions[solutionIdx] : animBoard;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
      {/* Controls */}
      <div>
        <Panel color="#f59e0b" title="♛ N-Queens Problem">
          <p style={{ color: "#94a3b8", fontSize: "13px", lineHeight: "1.6", marginBottom: "16px" }}>
            Tempatkan N ratu pada papan N×N sehingga tidak ada dua ratu yang saling menyerang 
            (tidak sebaris, sekolom, atau diagonal).
          </p>
          <Label>Ukuran Papan (N)</Label>
          <div style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
            {[4,5,6,7,8].map(v => (
              <button key={v} onClick={() => { setN(v); setSolutions([]); setAnimBoard([]); }}
                style={chipStyle(n === v, "#f59e0b")}>{v}</button>
            ))}
          </div>
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            <Btn color="#f59e0b" onClick={animateSolve} disabled={running}>
              ▶ Animasi Solve
            </Btn>
            <Btn color="#f59e0b" onClick={solve} disabled={running} outline>
              ⚡ Langsung
            </Btn>
            {running && <Btn color="#e94560" onClick={() => stopRef.current = true}>■ Stop</Btn>}
          </div>

          {solutions.length > 0 && (
            <div style={{ marginTop: "16px" }}>
              <div style={{ color: "#f59e0b", fontSize: "13px", marginBottom: "8px" }}>
                ✅ {solutions.length} solusi ditemukan
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <button onClick={() => setSolutionIdx(i => Math.max(0, i-1))}
                  style={navBtn} disabled={solutionIdx === 0}>◀</button>
                <span style={{ color: "#94a3b8", fontSize: "13px" }}>
                  Solusi {solutionIdx + 1} / {solutions.length}
                </span>
                <button onClick={() => setSolutionIdx(i => Math.min(solutions.length-1, i+1))}
                  style={navBtn} disabled={solutionIdx === solutions.length-1}>▶</button>
              </div>
            </div>
          )}
        </Panel>

        {/* Code */}
        <CodeBox code={`def solve_nqueens(n):
    board = [-1] * n
    solutions = []
    
    def is_safe(row, col):
        for i in range(row):
            if board[i] == col: return False
            if abs(board[i]-col) == abs(i-row):
                return False
        return True
    
    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # backtrack
    
    backtrack(0)
    return solutions`} />
      </div>

      {/* Board */}
      <div>
        <Panel color="#f59e0b" title="Visualisasi Papan">
          <ChessBoard n={n} board={currentBoard} color="#f59e0b" piece="♛" />
          {animStep >= 0 && running && (
            <div style={{ marginTop: "8px", color: "#64748b", fontSize: "11px", textAlign: "center" }}>
              Step: {animStep}
            </div>
          )}
        </Panel>
      </div>
    </div>
  );
}

// ─── KNIGHT'S TOUR TAB ────────────────────────────────────────────────────────

function KnightTab() {
  const [n, setN] = useState(6);
  const [startR, setStartR] = useState(0);
  const [startC, setStartC] = useState(0);
  const [path, setPath] = useState([]);
  const [visiblePath, setVisiblePath] = useState([]);
  const [running, setRunning] = useState(false);
  const [selecting, setSelecting] = useState(false);
  const stopRef = useRef(false);

  const solve = async (animate = true) => {
    const result = solveKnightTour(n, startR, startC);
    if (!result) { alert("Solusi tidak ditemukan!"); return; }
    setPath(result);
    if (!animate) { setVisiblePath(result); return; }
    setRunning(true);
    stopRef.current = false;
    setVisiblePath([]);
    for (let i = 0; i <= result.length; i++) {
      if (stopRef.current) break;
      setVisiblePath(result.slice(0, i));
      await sleep(80);
    }
    setRunning(false);
  };

  const board = Array.from({ length: n }, () => Array(n).fill(-1));
  visiblePath.forEach(([r, c], i) => { board[r][c] = i; });

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
      <div>
        <Panel color="#10b981" title="♞ Knight's Tour">
          <p style={{ color: "#94a3b8", fontSize: "13px", lineHeight: "1.6", marginBottom: "16px" }}>
            Temukan urutan langkah kuda catur sehingga mengunjungi setiap petak tepat satu kali.
            Gunakan algoritma Warnsdorff untuk efisiensi.
          </p>
          <Label>Ukuran Papan</Label>
          <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
            {[5,6,7,8].map(v => (
              <button key={v} onClick={() => { setN(v); setPath([]); setVisiblePath([]); setStartR(0); setStartC(0); }}
                style={chipStyle(n === v, "#10b981")}>{v}×{v}</button>
            ))}
          </div>
          <Label>Posisi Awal (klik papan)</Label>
          <div style={{ color: "#10b981", fontSize: "13px", marginBottom: "12px" }}>
            ({startR}, {startC}) — baris {startR+1}, kolom {startC+1}
          </div>
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            <Btn color="#10b981" onClick={() => solve(true)} disabled={running}>▶ Animasi</Btn>
            <Btn color="#10b981" onClick={() => solve(false)} disabled={running} outline>⚡ Langsung</Btn>
            {running && <Btn color="#e94560" onClick={() => stopRef.current = true}>■ Stop</Btn>}
          </div>
          {path.length > 0 && (
            <div style={{ marginTop: "12px", color: "#10b981", fontSize: "13px" }}>
              ✅ Tur selesai: {path.length} langkah ({n*n} petak)
            </div>
          )}
        </Panel>
        <CodeBox code={`def knight_tour(n, start_r, start_c):
    board = [[-1]*n for _ in range(n)]
    path = [(start_r, start_c)]
    board[start_r][start_c] = 0
    
    moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),
             (1,-2),(1,2),(2,-1),(2,1)]
    
    def warnsdorff(r, c):
        # Pilih langkah dgn paling sedikit
        # opsi berikutnya (heuristik)
        nexts = []
        for dr,dc in moves:
            nr,nc = r+dr, c+dc
            if 0<=nr<n and 0<=nc<n and board[nr][nc]==-1:
                deg = sum(1 for ddr,ddc in moves
                    if 0<=nr+ddr<n and 0<=nc+ddc<n
                    and board[nr+ddr][nc+ddc]==-1)
                nexts.append((deg,nr,nc))
        return sorted(nexts)
    
    r, c = start_r, start_c
    for step in range(1, n*n):
        nexts = warnsdorff(r, c)
        if not nexts: return None
        _, nr, nc = nexts[0]
        board[nr][nc] = step
        path.append((nr, nc))
        r, c = nr, nc
    return path`} />
      </div>

      <div>
        <Panel color="#10b981" title="Visualisasi Papan — klik untuk pilih start">
          <KnightBoard n={n} board={board} path={visiblePath}
            onCellClick={(r, c) => { setStartR(r); setStartC(c); setPath([]); setVisiblePath([]); }}
            startR={startR} startC={startC} />
          <div style={{ marginTop: "8px", display: "flex", gap: "12px", flexWrap: "wrap", fontSize: "11px", color: "#64748b" }}>
            <span>🟩 Start</span>
            <span style={{ color: "#10b981" }}>♞ Posisi terakhir</span>
            <span style={{ color: "#475569" }}>angka = urutan langkah</span>
          </div>
        </Panel>
      </div>
    </div>
  );
}

// ─── KNAPSACK TAB ─────────────────────────────────────────────────────────────

function KnapsackTab() {
  const [target, setTarget] = useState(30);
  const [weightsStr, setWeightsStr] = useState("2, 5, 6, 9, 12, 14, 20");
  const [steps, setSteps] = useState([]);
  const [visibleSteps, setVisibleSteps] = useState([]);
  const [bestCombo, setBestCombo] = useState(null);
  const [running, setRunning] = useState(false);
  const stopRef = useRef(false);
  const [speed, setSpeed] = useState(80);

  const weights = weightsStr.split(",").map(s => parseInt(s.trim())).filter(n => !isNaN(n));

  const solve = async (animate = true) => {
    const result = solveKnapsack(weights, target);
    setSteps(result.steps);
    setBestCombo(result.bestCombo);
    if (!animate) { setVisibleSteps(result.steps); return; }
    setRunning(true);
    stopRef.current = false;
    setVisibleSteps([]);
    for (let i = 0; i <= result.steps.length; i++) {
      if (stopRef.current) break;
      setVisibleSteps(result.steps.slice(0, i));
      await sleep(speed);
    }
    setVisibleSteps(result.steps);
    setRunning(false);
  };

  const currentStep = visibleSteps[visibleSteps.length - 1];

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
      <div>
        <Panel color="#8b5cf6" title="🎒 Knapsack Problem">
          <p style={{ color: "#94a3b8", fontSize: "13px", lineHeight: "1.6", marginBottom: "16px" }}>
            Temukan kombinasi barang yang totalnya tepat mencapai berat target menggunakan 
            rekursi dan backtracking.
          </p>
          <Label>Berat Target</Label>
          <input
            type="number" value={target}
            onChange={e => setTarget(Number(e.target.value))}
            style={inputStyle("#8b5cf6")}
          />
          <Label>Daftar Berat Barang (pisah koma)</Label>
          <input
            value={weightsStr}
            onChange={e => setWeightsStr(e.target.value)}
            style={inputStyle("#8b5cf6")}
          />
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "8px" }}>
            <span style={{ color: "#64748b", fontSize: "12px" }}>Kecepatan:</span>
            {[[200,"Lambat"],[80,"Sedang"],[20,"Cepat"]].map(([v,l]) => (
              <button key={v} onClick={() => setSpeed(v)} style={chipStyle(speed===v,"#8b5cf6")}>{l}</button>
            ))}
          </div>
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            <Btn color="#8b5cf6" onClick={() => solve(true)} disabled={running}>▶ Animasi</Btn>
            <Btn color="#8b5cf6" onClick={() => solve(false)} disabled={running} outline>⚡ Langsung</Btn>
            {running && <Btn color="#e94560" onClick={() => stopRef.current = true}>■ Stop</Btn>}
          </div>

          {bestCombo && (
            <div style={{
              marginTop: "16px", padding: "12px",
              background: "rgba(139,92,246,0.1)", border: "1px solid #8b5cf6",
              borderRadius: "8px"
            }}>
              <div style={{ color: "#8b5cf6", fontWeight: "bold", marginBottom: "6px" }}>
                ✅ Solusi Ditemukan!
              </div>
              <div style={{ color: "#94a3b8", fontSize: "13px" }}>
                Barang: [{bestCombo.join(", ")}]
              </div>
              <div style={{ color: "#c4b5fd", fontSize: "13px" }}>
                Total: {bestCombo.reduce((s,w)=>s+w,0)} / {target}
              </div>
            </div>
          )}
        </Panel>
        <CodeBox code={`def knapsack(weights, target, idx=0, chosen=[]):
    total = sum(chosen)
    
    # Base cases
    if total == target:
        return chosen  # Solusi ditemukan!
    if total > target or idx >= len(weights):
        return None   # Backtrack
    
    # Coba masukkan barang ke-idx
    chosen.append(weights[idx])
    result = knapsack(weights, target, idx+1, chosen)
    if result: return result
    chosen.pop()  # Backtrack: keluarkan
    
    # Coba tanpa barang ke-idx
    return knapsack(weights, target, idx+1, chosen)

# Contoh
weights = [2, 5, 6, 9, 12, 14, 20]
print(knapsack(weights, 30))  # [2, 5, 9, 14]`} />
      </div>

      <div>
        <Panel color="#8b5cf6" title="Visualisasi Backtracking">
          {/* Progress bar */}
          {steps.length > 0 && (
            <div style={{ marginBottom: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#64748b", marginBottom: "4px" }}>
                <span>Progress</span>
                <span>{visibleSteps.length} / {steps.length} steps</span>
              </div>
              <div style={{ height: "4px", background: "#1e293b", borderRadius: "2px" }}>
                <div style={{
                  height: "100%", borderRadius: "2px", background: "#8b5cf6",
                  width: `${steps.length ? (visibleSteps.length / steps.length) * 100 : 0}%`,
                  transition: "width 0.1s"
                }} />
              </div>
            </div>
          )}

          {/* Items grid */}
          <div style={{ marginBottom: "12px" }}>
            <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "6px" }}>BARANG TERSEDIA</div>
            <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
              {weights.map((w, i) => {
                const inChosen = currentStep?.chosen?.includes(w);
                const isCurrent = currentStep?.idx === i;
                return (
                  <div key={i} style={{
                    padding: "6px 10px",
                    border: `1px solid ${isCurrent ? "#f59e0b" : inChosen ? "#8b5cf6" : "#334155"}`,
                    borderRadius: "6px",
                    background: isCurrent ? "rgba(245,158,11,0.15)" : inChosen ? "rgba(139,92,246,0.2)" : "transparent",
                    fontSize: "13px",
                    color: isCurrent ? "#f59e0b" : inChosen ? "#c4b5fd" : "#64748b",
                    transition: "all 0.2s",
                    fontWeight: isCurrent ? "bold" : "normal",
                  }}>
                    {w}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Knapsack visual */}
          <div style={{
            border: "2px solid #8b5cf6", borderRadius: "12px",
            padding: "16px", marginBottom: "12px",
            background: "rgba(139,92,246,0.05)", minHeight: "100px",
          }}>
            <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "8px", display: "flex", justifyContent: "space-between" }}>
              <span>🎒 ISI KNAPSACK</span>
              <span style={{ color: currentStep?.total > target ? "#e94560" : currentStep?.total === target ? "#10b981" : "#8b5cf6" }}>
                {currentStep?.total ?? 0} / {target}
              </span>
            </div>
            {/* Fill bar */}
            <div style={{ height: "12px", background: "#1e293b", borderRadius: "6px", marginBottom: "8px", overflow: "hidden" }}>
              <div style={{
                height: "100%",
                background: currentStep?.total > target ? "#e94560" : currentStep?.total === target ? "#10b981" : "#8b5cf6",
                width: `${Math.min(100, ((currentStep?.total ?? 0) / target) * 100)}%`,
                borderRadius: "6px", transition: "all 0.2s"
              }} />
            </div>
            <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
              {(currentStep?.chosen ?? []).map((w, i) => (
                <span key={i} style={{
                  padding: "4px 8px", background: "rgba(139,92,246,0.3)",
                  border: "1px solid #8b5cf6", borderRadius: "4px",
                  fontSize: "12px", color: "#c4b5fd"
                }}>{w}</span>
              ))}
            </div>
          </div>

          {/* Phase indicator */}
          {currentStep && (
            <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
              <div style={{
                width: "8px", height: "8px", borderRadius: "50%",
                background: currentStep.phase === "exact" ? "#10b981" :
                  currentStep.phase === "backtrack" ? "#e94560" : "#8b5cf6",
                boxShadow: `0 0 6px ${currentStep.phase === "exact" ? "#10b981" : currentStep.phase === "backtrack" ? "#e94560" : "#8b5cf6"}`,
              }} />
              <span style={{ fontSize: "12px", color: "#94a3b8" }}>
                {currentStep.phase === "exact" ? "✅ SOLUSI DITEMUKAN" :
                  currentStep.phase === "backtrack" ? "↩ Backtrack" :
                  `Mencoba barang ke-${currentStep.idx + 1}`}
              </span>
            </div>
          )}

          {/* Recent steps log */}
          <div style={{ marginTop: "12px", maxHeight: "120px", overflowY: "auto" }}>
            <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "4px" }}>LOG TERBARU</div>
            {visibleSteps.slice(-8).reverse().map((s, i) => (
              <div key={i} style={{
                fontSize: "11px", color: i === 0 ? "#c4b5fd" : "#475569",
                padding: "2px 0",
                borderLeft: `2px solid ${s.phase === "exact" ? "#10b981" : s.phase === "backtrack" ? "#e94560" : "#8b5cf6"}`,
                paddingLeft: "6px", marginBottom: "2px"
              }}>
                [{s.chosen.join(",")}] = {s.total} — {s.phase}
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}

// ─── SHARED COMPONENTS ────────────────────────────────────────────────────────

function ChessBoard({ n, board, color, piece }) {
  const size = Math.min(320, Math.floor(480 / n));
  return (
    <div style={{ display: "inline-block" }}>
      {Array.from({ length: n }).map((_, r) => (
        <div key={r} style={{ display: "flex" }}>
          {Array.from({ length: n }).map((_, c) => {
            const isLight = (r + c) % 2 === 0;
            const hasQueen = board[r] === c;
            return (
              <div key={c} style={{
                width: size, height: size,
                background: isLight ? "#1e293b" : "#0f172a",
                border: `1px solid #334155`,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: size * 0.55,
                transition: "all 0.3s",
                boxShadow: hasQueen ? `inset 0 0 12px ${color}44` : "none",
                background: hasQueen ? `rgba(${color === "#f59e0b" ? "245,158,11" : "16,185,129"},0.15)` : isLight ? "#1e293b" : "#0f172a",
              }}>
                {hasQueen && <span style={{ filter: `drop-shadow(0 0 6px ${color})` }}>{piece}</span>}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}

function KnightBoard({ n, board, path, onCellClick, startR, startC }) {
  const size = Math.min(320, Math.floor(480 / n));
  const lastPos = path[path.length - 1];
  return (
    <div style={{ display: "inline-block", cursor: "pointer" }}>
      {Array.from({ length: n }).map((_, r) => (
        <div key={r} style={{ display: "flex" }}>
          {Array.from({ length: n }).map((_, c) => {
            const isLight = (r + c) % 2 === 0;
            const step = board[r][c];
            const isStart = r === startR && c === startC;
            const isLast = lastPos && lastPos[0] === r && lastPos[1] === c && path.length > 1;
            const visited = step >= 0;
            return (
              <div key={c} onClick={() => onCellClick(r, c)}
                style={{
                  width: size, height: size,
                  background: isStart && !visited ? "rgba(16,185,129,0.3)" :
                    isLast ? "rgba(16,185,129,0.4)" :
                    visited ? "rgba(16,185,129,0.12)" :
                    isLight ? "#1e293b" : "#0f172a",
                  border: `1px solid ${isStart ? "#10b981" : "#334155"}`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: step >= 0 ? Math.max(8, size * 0.28) : size * 0.55,
                  color: isLast ? "#10b981" : "#64748b",
                  fontWeight: isLast ? "bold" : "normal",
                  transition: "all 0.15s",
                  userSelect: "none",
                }}>
                {isLast ? "♞" : step >= 0 ? step + 1 : isStart ? "◎" : ""}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}

function Panel({ color, title, children }) {
  return (
    <div style={{
      border: `1px solid ${color}33`,
      borderTop: `2px solid ${color}`,
      borderRadius: "8px",
      padding: "16px",
      background: "#0d1117",
      marginBottom: "16px",
    }}>
      <div style={{ color, fontWeight: "bold", fontSize: "14px", letterSpacing: "1px", marginBottom: "12px" }}>
        {title}
      </div>
      {children}
    </div>
  );
}

function CodeBox({ code }) {
  return (
    <div style={{
      background: "#050810", border: "1px solid #1e293b",
      borderRadius: "8px", padding: "14px",
      fontFamily: "'Courier New', monospace",
      fontSize: "11px", color: "#7dd3fc",
      lineHeight: "1.7", whiteSpace: "pre",
      overflowX: "auto",
    }}>
      <div style={{ color: "#475569", marginBottom: "6px", fontSize: "10px", letterSpacing: "1px" }}>
        ── PYTHON CODE ──
      </div>
      {code}
    </div>
  );
}

function Label({ children }) {
  return <div style={{ color: "#64748b", fontSize: "11px", letterSpacing: "1px", marginBottom: "6px", textTransform: "uppercase" }}>{children}</div>;
}

function Btn({ color, onClick, disabled, outline, children }) {
  return (
    <button onClick={onClick} disabled={disabled} style={{
      padding: "8px 16px",
      background: outline ? "transparent" : color,
      border: `1px solid ${color}`,
      borderRadius: "6px",
      color: outline ? color : "#0a0a0f",
      fontFamily: "'Courier New', monospace",
      fontSize: "12px", fontWeight: "bold",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.4 : 1,
      transition: "all 0.2s",
    }}>{children}</button>
  );
}

function chipStyle(active, color) {
  return {
    padding: "4px 12px",
    border: `1px solid ${active ? color : "#334155"}`,
    borderRadius: "4px",
    background: active ? `${color}22` : "transparent",
    color: active ? color : "#64748b",
    fontFamily: "'Courier New', monospace",
    fontSize: "12px", cursor: "pointer",
    transition: "all 0.2s",
  };
}

function inputStyle(color) {
  return {
    width: "100%", padding: "8px 12px",
    background: "#050810", border: `1px solid ${color}44`,
    borderRadius: "6px", color: "#e2e8f0",
    fontFamily: "'Courier New', monospace",
    fontSize: "13px", marginBottom: "12px",
    outline: "none", boxSizing: "border-box",
  };
}

const navBtn = {
  padding: "4px 12px", border: "1px solid #334155",
  borderRadius: "4px", background: "transparent",
  color: "#94a3b8", cursor: "pointer", fontFamily: "inherit",
};
