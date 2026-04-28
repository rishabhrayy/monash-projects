# ============================================================
# Multi-agent planner for Flatland (LaCAM* style) with:
# - Direction-aware reverse lower bounds (admissible heuristic)
# - Reservation table for vertex and edge conflicts
# - Constraint table for lazy conflict resolution
# - Junction metering to reduce local congestion
# - Restart-based outer loop and local repair (replan)
# Commented for clarity. Logic preserved.
# ============================================================

from lib_piglet.utils.tools import eprint
from typing import List, Tuple, Dict, Set
import glob, os, sys, heapq, time, random, math, collections

# Flatland interfaces
try:
    from flatland.core.transition_map import GridTransitionMap
    from flatland.envs.agent_utils import EnvAgent
    from flatland.utils.controller import (
        get_action, Train_Actions, Directions, check_conflict,
        path_controller, evaluator, remote_evaluator
    )
except Exception as e:
    eprint("Cannot load flatland modules!")
    eprint(e)
    exit(1)

# -------------------------
# Debugger and visualizer
# -------------------------
debug = False
visualizer = False

# For targeting a single test file during local debug
test_single_instance = False
level = 0
test = 0

# -------------------------
# Direction constants order
# -------------------------
DIRS = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)

# ============================================================
# Rail helpers
# ============================================================

def _in_bounds(rail: GridTransitionMap, x: int, y: int) -> bool:
    """Check map bounds for safety."""
    return 0 <= x < rail.height and 0 <= y < rail.width

def _neighbors(rail: GridTransitionMap, x: int, y: int, d: int):
    """
    Enumerate valid next (x,y,dir) states from current (x,y,dir) using
    Flatland's transition map. Includes only track-following moves.
    """
    trans = rail.get_transitions(x, y, d)  # iterable truthy flags [N,E,S,W]
    out = []
    for i, nd in enumerate(DIRS):
        if trans[i]:
            nx, ny = x, y
            if nd == Directions.NORTH: nx -= 1
            elif nd == Directions.EAST:  ny += 1
            elif nd == Directions.SOUTH: nx += 1
            elif nd == Directions.WEST:  ny -= 1
            out.append((nx, ny, nd))
    return out

def _is_junction(rail: GridTransitionMap, x: int, y: int) -> bool:
    """
    A light notion of 'junction': sum of outgoing permissions over all
    incoming directions exceeds 2.
    """
    deg = 0
    for ed in DIRS:
        deg += sum(rail.get_transitions(x, y, ed))
    return deg > 2

# ------------------------------------------------------------
# Directional reverse lower bound h(x,y,dir)->steps to goal
#   Build by a reverse Dijkstra from the goal over (cell,dir)
#   Admissible and tighter than Manhattan on rails.
# ------------------------------------------------------------
def _dir_lb(rail: GridTransitionMap, goal: Tuple[int,int]) -> Dict[Tuple[int,int,int], int]:
    gx, gy = goal
    INF = 10**9
    dist: Dict[Tuple[int,int,int], int] = {}
    pq, seen = [], set()
    # Seed: all directions at the goal have 0
    for d in DIRS:
        dist[(gx, gy, d)] = 0
        heapq.heappush(pq, (0, gx, gy, d))

    while pq:
        g, x, y, d_here = heapq.heappop(pq)
        key = (x, y, d_here)
        if key in seen:
            continue
        seen.add(key)

        # Reverse predecessor cell along d_here
        px, py = x, y
        if d_here == Directions.NORTH: px += 1
        elif d_here == Directions.EAST:  py -= 1
        elif d_here == Directions.SOUTH: px -= 1
        elif d_here == Directions.WEST:  py += 1
        if not _in_bounds(rail, px, py):
            continue

        # Any predecessor direction pd that can move from (px,py,pd) to (x,y,d_here)
        for pd in DIRS:
            trans = rail.get_transitions(px, py, pd)
            allow = (
                (d_here == Directions.NORTH and trans[Directions.NORTH]) or
                (d_here == Directions.EAST  and trans[Directions.EAST ]) or
                (d_here == Directions.SOUTH and trans[Directions.SOUTH]) or
                (d_here == Directions.WEST  and trans[Directions.WEST ])
            )
            if not allow:
                continue
            k2 = (px, py, pd); ng = g + 1
            if dist.get(k2, INF) > ng:
                dist[k2] = ng
                heapq.heappush(pq, (ng, px, py, pd))
    return dist

# Cache to avoid recomputing per goal
_DIR_LB_CACHE: Dict[Tuple[int,int], Dict[Tuple[int,int,int], int]] = {}

def dir_lb_cached(rail: GridTransitionMap, goal: Tuple[int,int]):
    """Memoized access to directional LB map for a goal."""
    m = _DIR_LB_CACHE.get(goal)
    if m is None:
        m = _dir_lb(rail, goal)
        _DIR_LB_CACHE[goal] = m
    return m

# ============================================================
# Reservations and constraints
# ============================================================

class ConstraintTable:
    """
    Agent-specific hard constraints for lazy conflict resolution.
    - vtx[t] contains cells forbidden at time t.
    - edg[t] contains directed edges (u->v) forbidden at time t.
    """
    def __init__(self):
        self.vtx: Dict[int, Set[Tuple[int,int]]] = {}
        self.edg: Dict[int, Set[Tuple[Tuple[int,int],Tuple[int,int]]]] = {}

    def forbid_vertex(self, t: int, cell: Tuple[int,int]):
        self.vtx.setdefault(t, set()).add(cell)

    def forbid_edge(self, t: int, u: Tuple[int,int], v: Tuple[int,int]):
        self.edg.setdefault(t, set()).add((u, v))

    def violates(self, t: int, u: Tuple[int,int], v: Tuple[int,int]) -> bool:
        """Return True if (u->v) at time t violates any constraint."""
        if t in self.vtx and v in self.vtx[t]:
            return True
        if t in self.edg and (u, v) in self.edg[t]:
            return True
        return False

def build_reservations(paths: List[List[Tuple[int,int]]]) -> Dict[int, Dict[int, Tuple[Tuple[int,int],Tuple[int,int]]]]:
    """
    Create a time-indexed reservation table from already planned paths.
    reservations[t][aid] = (pos_t, pos_t+1); if path ends, agent stays put.
    """
    reservations: Dict[int, Dict[int, Tuple[Tuple[int,int],Tuple[int,int]]]] = {}
    if not paths:
        return reservations
    T = max((len(p) for p in paths if p), default=0)
    for t in range(max(T, 1)):
        reservations[t] = {}
        for aid, p in enumerate(paths):
            if not p:
                continue
            u = p[t] if t < len(p) else p[-1]
            v = p[t+1] if t+1 < len(p) else p[-1]
            reservations[t][aid] = (u, v)
    return reservations

def conflict_with_reservations(
    t: int,
    u: Tuple[int,int],
    v: Tuple[int,int],
    res_t: Dict[int, Tuple[Tuple[int,int],Tuple[int,int]]]
) -> Tuple[bool, int]:
    """
    Check if move u->v at time t conflicts with reserved moves.
    Returns (True, other_agent_id) if vertex or edge-swap conflict exists.
    """
    for jid, (ou, ov) in res_t.items():
        if v == ov:                   # vertex conflict at t+1
            return True, jid
        if u == ov and v == ou:       # opposing edge swap
            return True, jid
    return False, -1

def _busy_soon(
    cell: Tuple[int,int],
    t_now: int,
    reservations: Dict[int, Dict[int, Tuple[Tuple[int,int],Tuple[int,int]]]],
    k: int = 2
) -> bool:
    """
    Heuristic for local metering:
    If any reserved move will enter 'cell' in next k steps, mark as busy.
    """
    for tau in range(t_now + 1, t_now + 1 + k + 1):
        rt = reservations.get(tau - 1, {})
        for _aid, (_u, ov) in rt.items():
            if ov == cell:
                return True
    return False

# ============================================================
# Single-agent planner with constraints (inner A*)
# ============================================================

def plan_single(
    rail: GridTransitionMap,
    start: Tuple[int,int],
    start_dir: int,
    goal: Tuple[int,int],
    max_timestep: int,
    reservations: Dict[int, Dict[int, Tuple[Tuple[int,int],Tuple[int,int]]]],
    ctab: ConstraintTable,
    dir_lb: Dict[Tuple[int,int,int], int]
) -> List[Tuple[int,int]]:
    """
    Time-extended A*:
      State = (x,y,dir,t), g = t, h from reverse directional LB (admissible).
      - Checks hard constraints and reservation conflicts.
      - Adds junction metering to avoid immediate congestion.
      - Adds small bias for heuristic progress and straight motion.
    """
    sx, sy = start
    gx, gy = goal
    INF = 10**9

    # f-queue: (f, g=t, x, y, dir)
    openq: List[Tuple[float,int,int,int,int]] = []
    parent: Dict[Tuple[int,int,int,int], Tuple[int,int,int,int]] = {}
    gbest: Dict[Tuple[int,int,int,int], int] = {}

    def h(x, y, d):
        v = dir_lb.get((x, y, d), INF)
        return v if v != INF else abs(x - gx) + abs(y - gy)

    s = (sx, sy, start_dir, 0)
    gbest[s] = 0
    heapq.heappush(openq, (h(sx, sy, start_dir), 0, sx, sy, start_dir))

    while openq:
        f, t, x, y, d = heapq.heappop(openq)

        # Goal on position only (dir irrelevant at goal)
        if (x, y) == goal:
            path = []
            node = (x, y, d, t)
            while node in parent:
                path.append((node[0], node[1]))
                node = parent[node]
            path.append((sx, sy))
            path.reverse()
            return path

        if t >= max_timestep:
            continue

        # Generate successors: all rail moves + wait
        succs = _neighbors(rail, x, y, d) + [(x, y, d)]
        # Optional ordering by heuristic for better queue locality
        succs.sort(key=lambda nd: h(nd[0], nd[1], nd[2]))

        for nx, ny, nd in succs:
            t2 = t + 1
            u, v = (x, y), (nx, ny)

            # Metering: avoid entering a busy junction unless necessary
            if _is_junction(rail, nx, ny) and _busy_soon((nx, ny), t, reservations, k=2):
                continue

            # Hard agent-specific constraints
            if ctab.violates(t2, u, v):
                continue

            # Check reservations from already planned agents
            res_t = reservations.get(t, {})
            bad, _ = conflict_with_reservations(t, u, v, res_t)
            if bad:
                continue

            nk = (nx, ny, nd, t2)
            g2 = t2
            if g2 < gbest.get(nk, INF):
                gbest[nk] = g2
                parent[nk] = (x, y, d, t)

                # Heuristic terms
                h_here = h(x, y, d)
                h_next = h(nx, ny, nd)

                # Small bonuses to break ties and reduce dithering
                bonus = 0.0
                if h_next < h_here:                  # progressing toward goal
                    bonus -= 0.03
                if (nx, ny) != (x, y) and nd == d:   # straight motion preference
                    bonus -= 0.01
                noise = (random.random() - 0.5) * 1e-4

                f2 = g2 + h_next + bonus + noise
                if f2 <= max_timestep + 1000:        # guard against numeric drift
                    heapq.heappush(openq, (f2, g2, nx, ny, nd))

    # Failed to find a plan within horizon
    return []

# ============================================================
# LaCAM* outer loop: grow plans, detect conflicts, add constraints, replan
# ============================================================

def earliest_conflict(paths: List[List[Tuple[int,int]]]) -> Tuple[int,int,int,Tuple[int,int],Tuple[int,int]]:
    """
    Scan paths for earliest conflict:
      - Vertex conflict at t+1
      - Edge swap between t and t+1
    Returns (t, i, j, pos_i, pos_j) or t=-1 if none.
    """
    if not paths:
        return -1, -1, -1, (0, 0), (0, 0)
    T = max(len(p) for p in paths)
    n = len(paths)
    for t in range(T):
        pos_t  = [ (p[t]   if t   < len(p) else p[-1]) for p in paths ]
        pos_t1 = [ (p[t+1] if t+1 < len(p) else p[-1]) for p in paths ]

        # Vertex conflicts at t+1
        seen: Dict[Tuple[int,int], int] = {}
        for i, v in enumerate(pos_t1):
            if v in seen:
                j = seen[v]
                return t, i, j, v, v
            seen[v] = i

        # Edge swaps between t and t+1
        for i in range(n):
            for j in range(i + 1, n):
                if pos_t[i] == pos_t1[j] and pos_t1[i] == pos_t[j]:
                    return t, i, j, pos_t1[i], pos_t1[j]

    return -1, -1, -1, (0, 0), (0, 0)

def _choose_loser(i: int, j: int, t: int,
                  paths: List[List[Tuple[int,int]]],
                  goals: List[Tuple[int,int]]) -> int:
    """
    Break ties when two agents conflict:
      Prefer to replan the agent with longer current path and further remaining distance.
    """
    def score(k: int):
        p = paths[k]
        rem = abs(p[-1][0] - goals[k][0]) + abs(p[-1][1] - goals[k][1]) if p else 1e9
        return (len(p), rem)
    return i if score(i) >= score(j) else j

def _plan_order(rail: GridTransitionMap, agents: List[EnvAgent]) -> List[int]:
    """
    Compute a planning order:
      - Agents starting in crowded cells go earlier.
      - Longer trips go earlier.
      - Local shuffle per block to avoid brittle ties.
    """
    groups: Dict[Tuple[int,int], List[int]] = collections.defaultdict(list)
    for i, a in enumerate(agents):
        groups[a.initial_position].append(i)

    def key(i: int):
        a = agents[i]
        crowd = len(groups[a.initial_position])
        dx = abs(a.initial_position[0] - a.target[0]) + abs(a.initial_position[1] - a.target[1])
        return (-crowd, -dx, i)

    order = sorted(range(len(agents)), key=key)
    for k in range(0, len(order), 4):
        random.shuffle(order[k:k+4])
    return order

def lacam_star_plan(
    agents: List[EnvAgent],
    rail: GridTransitionMap,
    max_timestep: int,
    start_pos: List[Tuple[int,int]],
    start_dir: List[int],
    goals: List[Tuple[int,int]],
    time_budget_sec: float = 3.0,
    restarts: int = 6
) -> List[List[Tuple[int,int]]]:
    """
    Outer loop:
      1) Choose a planning order.
      2) Plan each agent once with reservations from prior agents.
      3) Repeatedly detect earliest conflict, add constraints to one 'loser', and replan that agent.
      4) Keep the best-total-cost solution across several randomized restarts under a time budget.
    """
    n = len(agents)
    dir_lbs = [dir_lb_cached(rail, goals[i]) for i in range(n)]

    best_paths: List[List[Tuple[int,int]]] = [[] for _ in range(n)]
    best_score = math.inf
    start_time = time.time()

    for r in range(restarts):
        if time.time() - start_time > time_budget_sec:
            break

        order = _plan_order(rail, agents)                 # guided plan order
        constraints: List[ConstraintTable] = [ConstraintTable() for _ in range(n)]
        paths: List[List[Tuple[int,int]]] = [[] for _ in range(n)]

        # Seed phase: plan each agent once with current reservations
        fail = False
        for aid in order:
            res = build_reservations(paths)
            p = plan_single(
                rail, start_pos[aid], start_dir[aid], goals[aid],
                max_timestep, res, constraints[aid], dir_lbs[aid]
            )
            if not p:
                fail = True
                break
            paths[aid] = p
        if fail:
            continue

        # Lazy conflict fixing
        while True:
            t, i, j, vi, vj = earliest_conflict(paths)
            if t < 0:  # no conflicts
                break

            loser = _choose_loser(i, j, t, paths, goals)
            # Forbid the problematic vertex at t+1 and the edge used at t
            constraints[loser].forbid_vertex(t + 1, vi)
            ui = paths[loser][t] if t < len(paths[loser]) else paths[loser][-1]
            constraints[loser].forbid_edge(t, ui, vi)

            # Replan only the loser against reservations from others
            res = build_reservations([paths[k] if k != loser else [] for k in range(n)])
            p = plan_single(
                rail, start_pos[loser], start_dir[loser], goals[loser],
                max_timestep, res, constraints[loser], dir_lbs[loser]
            )
            if not p:
                fail = True
                break
            paths[loser] = p

            if time.time() - start_time > time_budget_sec:
                break

        if fail:
            continue

        # Score by sum of individual costs (SIC)
        sic = sum(len(p) - 1 for p in paths if p)
        if sic < best_score:
            best_score, best_paths = sic, paths

        if time.time() - start_time > time_budget_sec:
            break

    # Fallback: if any path missing, return waits at start
    if any(len(p) == 0 for p in best_paths):
        best_paths = [[start_pos[i]] for i in range(n)]

    # Pad all paths to the same length so the simulator can step lock-step
    T = max(len(p) for p in best_paths)
    for p in best_paths:
        if not p:
            continue
        while len(p) < T:
            p.append(p[-1])

    return best_paths

# ============================================================
# Public API used by the evaluator
# ============================================================

def get_path(agents: List[EnvAgent], rail: GridTransitionMap, max_timestep: int):
    """
    Batch planner entry:
      - Builds start states from agents
      - Chooses adaptive time budget and restarts based on n
      - Calls LaCAM* outer loop
    """
    n = len(agents)
    start_pos = [a.initial_position for a in agents]
    start_dir = [a.initial_direction for a in agents]
    goals     = [a.target for a in agents]

    time_budget_sec = min(3.0, 0.08 * max(1, n))               # small per-batch budget
    restarts = 6 if n <= 25 else 8 if n <= 50 else 12           # more agents → more restarts

    return lacam_star_plan(
        agents, rail, max_timestep, start_pos, start_dir, goals,
        time_budget_sec=time_budget_sec, restarts=restarts
    )

def replan(
    agents: List[EnvAgent],
    rail: GridTransitionMap,
    current_timestep: int,
    existing_paths: List[List[Tuple[int, int]]],
    max_timestep: int,
    new_malfunction_agents: List[int],
    failed_agents: List[int]
):
    """
    Local repair:
      - Freeze prefix up to current_timestep.
      - Derive new start states from current positions and implied directions.
      - Plan suffix over remaining horizon with a tight budget.
      - Stitch prefix + suffix.
    """
    n = len(agents)

    # Fixed prefix for each agent up to current_timestep
    prefix = [
        (p[:current_timestep + 1] if p else [agents[i].position])
        for i, p in enumerate(existing_paths)
    ]

    # Build new starts at time current_timestep for suffix planning
    start_pos, start_dir, goals = [], [], [a.target for a in agents]
    for i in range(n):
        if current_timestep < len(existing_paths[i]):
            pos = existing_paths[i][current_timestep]
        else:
            pos = prefix[i][-1]
        start_pos.append(pos)

        # Derive heading from last move if available; else keep agent's current dir
        if current_timestep > 0 and current_timestep < len(existing_paths[i]):
            prev = existing_paths[i][current_timestep - 1]
            cur  = existing_paths[i][current_timestep]
            dx, dy = cur[0] - prev[0], cur[1] - prev[1]
            if   dx == -1 and dy == 0: d = Directions.NORTH
            elif dx ==  1 and dy == 0: d = Directions.SOUTH
            elif dx ==  0 and dy == 1: d = Directions.EAST
            elif dx ==  0 and dy == -1: d = Directions.WEST
            else: d = agents[i].direction
        else:
            d = agents[i].direction
        start_dir.append(d)

    # Remaining horizon and tight time budget for quick local fix
    rem = max(0, max_timestep - current_timestep)
    suffix = lacam_star_plan(
        agents, rail, rem, start_pos, start_dir, goals,
        time_budget_sec=min(2.0, 0.05 * max(1, n)), restarts=4
    )

    # Stitch prefix with suffix (drop duplicate first cell of suffix)
    new_paths: List[List[Tuple[int,int]]] = []
    for i in range(n):
        post = suffix[i][1:] if suffix[i] else []
        new_paths.append(prefix[i] + post)
    return new_paths

# ============================================================
# CLI harness: remote or local evaluation
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Remote evaluator mode with replan hook
        remote_evaluator(get_path, sys.argv, replan=replan)
    else:
        # Local multi-agent evaluation over all test cases
        script_path = os.path.dirname(os.path.abspath(__file__))
        test_cases = glob.glob(os.path.join(script_path, "multi_test_case/level*_test_*.pkl"))
        if test_single_instance:
            test_cases = glob.glob(
                os.path.join(script_path, f"multi_test_case/level{level}_test_{test}.pkl")
            )
        test_cases.sort()
        deadline_files = [test.replace(".pkl", ".ddl") for test in test_cases]
        # mode=3 indicates multi-agent with deadlines; pass replan callback
        evaluator(get_path, test_cases, debug, visualizer, 3, deadline_files, replan=replan)
