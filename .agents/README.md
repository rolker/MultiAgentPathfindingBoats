# Agent Guide: MultiAgentPathfindingBoats

> Plans survey-line coverage for several boats: a Tkinter front end builds a
> problem, a Gurobi mixed-integer program solves it, and matplotlib plots the
> result.

## Fork

`origin` (`rolker/MultiAgentPathfindingBoats`) is a fork of `upstream`
(`sjh1036/MultiAgentPathfindingBoats`). Agent material lives only on the fork:
`.agents/`, `.agent/` and `docs/roadmap.md`. None of it may appear in a pull
request to upstream. Issues and pull requests for agent-driven work go to the
fork.

## Module Inventory

All modules are top-level Python files; there is no package, no dependency
file and no tests.

| Module | Description |
|--------|-------------|
| `ui.py` | Tkinter window ("Ducklings"). Validates the inputs, calls `formulator.formulate`, merges per-solution PDFs with `pypdf`. |
| `formulator.py` | Reads survey lines from CSV or generates them, places boat origin and rendezvous points, builds per-boat cost and path matrices, calls `solver.solve` once per weight. |
| `solver.py` | Builds and optimizes the Gurobi model ("MCPP"), with lazy cycle-elimination constraints, then calls `visualizer.printProblem`. |
| `dubins.py` | Dubins paths (LSL, RSR, LSR, RSL, LRL, RLR) between two poses for a minimum turning radius. |
| `visualizer.py` | Prints each boat's moves and plots the solution; shows the plot or saves it as PDF. |

## Architecture Overview

Call chain: `ui.formulateProblem` → `formulator.formulate` →
`formulator.createMatrices` (→ `dubins.findShortestPath` when a boat's minimum
radius is not 0) → `solver.solve` → `visualizer.printProblem`.

Point indexing, shared by formulator, solver and visualizer:

- Survey line `l` has endpoints `2*l` and `2*l + 1`.
- Boat `b`'s origin is point `numEndPoints + b`.
- Boat `b`'s rendezvous is point `numEndPoints + numBoats + b`.

The binary variable `x[boat, a, b]` means the boat leaves point `a`, transits
to the other end of `b`'s line, and surveys that line to arrive at `b`.
`costMatrices[boat][a][b]` is that move's time: transit distance over the
boat's transit speed plus line length over its survey speed. With a minimum
radius, the transit distance is the Dubins path length and
`pathMatrices[boat][a][b]` holds its segments for plotting.

The objective minimizes `t + Weight * (sum of all boats' costs)`, where `t` is
the makespan (every boat's total cost is constrained to be at most `t`).

`solver.solve` returns a list whose first element is the status:
`[0, 0]` optimal, `[0, 1]` time limit hit with a solution, `[1]` no solution,
`[2, message]` error. On success the list continues with the PDF title, the
unweighted objective value, and the chosen edges as `[boat, start, end]`.
`formulator.formulate` returns a list of these, one per weight.

## Key Files to Read First

1. `formulator.py` — `formulate` is the entry point a caller other than the UI
   would use; `createMatrices` defines the cost model.
2. `solver.py` — the model, its constraints and the return format.
3. `ui.py` — how the arguments to `formulate` are assembled, and their defaults.

## Build & Test

There is no build step and there are no tests; the workspace settings record
`build=none` and `test=none`. Run the application with `python ui.py`.

Requirements, from the imports:

- Python 3.12 or newer: `ui.py` nests double quotes inside double-quoted
  f-strings (for example line 113).
- `gurobipy` (Gurobi is a commercial solver and needs a license), `numpy`,
  `matplotlib`, `pypdf`, and `tkinter`.

## Dependencies

| Module | Imports | Third-party |
|--------|---------|-------------|
| `ui.py` | `formulator` | `tkinter`, `pypdf` |
| `formulator.py` | `solver`, `dubins` | `numpy` |
| `solver.py` | `visualizer` | `gurobipy` |
| `visualizer.py` | | `gurobipy`, `matplotlib` (also through `pylab`), `numpy` |
| `dubins.py` | | `numpy` |

## Common Pitfalls

- **`ui.py` cannot be imported.** It builds the window and enters
  `root.mainloop()` at module level.
- **Solving always plots.** `solver.solve` calls `visualizer.printProblem`
  unconditionally (`SHOWPATHS = True`); with `toPDF` false that ends in
  `plt.show()`, which blocks until the window is closed. Importing `solver`
  also imports matplotlib.
- **The solver time limit defaults to 10 seconds** (`timeLimit=10` in both
  `formulate` and `solve`); a result at the limit is returned as `[0, 1]`.
- **CSV input reads columns 1 to 4**, not 0 to 3 (`startingIndex = 1` in
  `formulator.py`), so each row needs a leading column. The README describes
  rows as `x1,y1,x2,y2`, and the "write to file" option writes exactly four
  columns, so a file the application wrote cannot be read back.
- **Step-through (`numSteps > 0`) fails.** `formulator.py` line 268 calls
  `stepThrough` with 13 arguments where 14 are required, and indexes
  `outputs[i-1]` with an `i` that is not defined when lines come from a file.
  `visualizer.py` line 149 calls `plotLine` without its `isPair` argument on
  the same path.
- **"Print to PDF" without an input file fails.** `ui.py` line 360 calls
  `len(fileName)` when `fileName` is `None`, after the per-solution PDFs were
  already removed.
- **Settings files never set boats or lines.** `ui.readTextFile` lowercases
  each line and then tests for `"numBoats"` and `"numLines"`.
- **Generation type 5** (rotated columns) exists in `formulator.py` and is
  accepted by the UI but is not in the README.
- **Solution PDFs are written to the current directory**, named from the
  problem size, weight and step number.
