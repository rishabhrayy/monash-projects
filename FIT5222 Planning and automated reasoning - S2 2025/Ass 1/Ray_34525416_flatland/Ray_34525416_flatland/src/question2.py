# ------------------------------------------------------------
# Single-agent path planning with conflict avoidance (A* + LNS repair)
# Commented for clarity. Behavior unchanged.
# ------------------------------------------------------------

from lib_piglet.utils.tools import eprint
import glob, os, sys
import heapq, random, time

# Try Flatland imports; exit if environment not set up
try:
    from flatland.core.transition_map import GridTransitionMap
    from flatland.utils.controller import (
        get_action, Train_Actions, Directions, check_conflict,
        path_controller, evaluator, remote_evaluator
    )
except Exception as e:
    eprint("Cannot load flatland modules!", e)
    exit(1)

# -------- Debug/visual toggles --------
debug = False
visualizer = False

# -------- Single-instance testing toggles --------
test_single_instance = False
level = 0
test = 0

# ============================================================
# Path planner API
#   get_path(...) returns a list of (x, y) cells from start to goal.
#   The solver avoids vertex and edge conflicts with existing_paths.
# ============================================================

# Directions order used by Flatland's transitions
DIRS = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)

def _neighbors(rail: GridTransitionMap, x: int, y: int, dir_now: int):
    """
    Enumerate valid next states from (x,y,dir_now) using rail transitions.
    Returns: list of (nx, ny, ndir)
    """
    trans = rail.get_transitions(x, y, dir_now)  # iterable over [N,E,S,W]
    out = []
    for i, d in enumerate(DIRS):
        if trans[i]:
            nx, ny = x, y
            if d == Directions.NORTH: nx -= 1
            elif d == Directions.EAST: ny += 1
            elif d == Directions.SOUTH: nx += 1
            elif d == Directions.WEST: ny -= 1
            out.append((nx, ny, d))
    return out

def _in_bounds(rail: GridTransitionMap, x: int, y: int) -> bool:
    """Check map bounds."""
    return 0 <= x < rail.height and 0 <= y < rail.width

def _check_conflict(path, existing_paths):
    """
    Check path against existing_paths for:
      - vertex conflicts: same cell at same time
      - edge conflicts: swap positions between t and t+1
    Returns True if any conflict is found.
    """
    for t, cell in enumerate(path):
        for p in existing_paths:
            if t < len(p):
                # Vertex conflict
                if p[t] == cell:
                    return True
                # Edge conflict
                if t > 0 and p[t - 1] == cell and p[t] == path[t - 1]:
                    return True
    return False

def _astar(start, start_dir, goal, rail, existing_paths, max_timestep):
    """
    Time-extended A* with reservation checks.
    State = (x, y, dir, t). Cost = time (g = t). Heuristic = Manhattan.
    Allows 'wait' action by re-expanding same cell with t+1.
    """
    sx, sy = start
    gx, gy = goal

    # Priority queue of (f, state); parent and g_score tables for reconstruction
    openq, parent, g_score = [], {}, {}

    start_key = (sx, sy, start_dir, 0)
    g_score[start_key] = 0
    heapq.heappush(openq, (0, start_key))

    while openq:
        _, (x, y, dir_now, t) = heapq.heappop(openq)

        # Goal test on position only. Direction is irrelevant at goal.
        if (x, y) == goal:
            path = []
            k = (x, y, dir_now, t)
            while k in parent:
                path.append((k[0], k[1]))
                k = parent[k]
            path.append((sx, sy))
            path.reverse()
            return path

        # Stop expanding beyond horizon
        if t >= max_timestep:
            continue

        # Successors: all rail moves + wait
        succs = _neighbors(rail, x, y, dir_now) + [(x, y, dir_now)]
        for nx, ny, ndir in succs:
            t2 = t + 1

            # Reservation checks against existing plans
            ok = True
            for p in existing_paths:
                if t2 < len(p):
                    # Vertex conflict at next time
                    if p[t2] == (nx, ny):
                        ok = False
                    # Edge conflict: (x,y)->(nx,ny) vs (nx,ny)->(x,y)
                    if t < len(p) and p[t] == (nx, ny) and p[t2] == (x, y):
                        ok = False
            if not ok:
                continue

            nk = (nx, ny, ndir, t2)
            g2 = t2
            h2 = abs(nx - gx) + abs(ny - gy)  # Manhattan heuristic
            f2 = g2 + h2

            # Standard A* relaxation
            if g2 < g_score.get(nk, float("inf")):
                g_score[nk] = g2
                parent[nk] = (x, y, dir_now, t)
                heapq.heappush(openq, (f2, nk))

    # No feasible path found within horizon
    return []

def get_path(start, start_direction, goal, rail, agent_id, existing_paths, max_timestep):
    """
    Entry point used by the evaluator.
    Strategy:
      1) Plan with A* ignoring conflicts to get a baseline.
      2) If conflicts exist, run a short LNS-style repair: replan with reservations
         within a small time budget. Return first conflict-free plan found.
    """
    # 1) Baseline plan without reservations
    path = _astar(start, start_direction, goal, rail, [], max_timestep)
    if not path:
        return []

    best = path
    best_conflict = _check_conflict(best, existing_paths)

    # 2) LNS-style repair loop with small time budget
    start_time = time.time()
    TIME_LIMIT = 1.0  # seconds per agent

    while time.time() - start_time < TIME_LIMIT and best_conflict:
        # Replan with current reservations
        candidate = _astar(start, start_direction, goal, rail, existing_paths, max_timestep)

        # Return immediately if conflict-free
        if candidate and not _check_conflict(candidate, existing_paths):
            return candidate

        # Track best seen candidate if it removes conflicts
        c_conf = _check_conflict(candidate, existing_paths) if candidate else True
        if candidate and not c_conf:
            best, best_conflict = candidate, False

    return best  # May still contain conflicts if no repair found in time

# ============================================================
# Harness: local or remote evaluation
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Remote evaluator mode (used by auto-grader)
        remote_evaluator(get_path, sys.argv)
    else:
        # Local batch evaluation over multi-agent cases
        script_path = os.path.dirname(os.path.abspath(__file__))
        test_cases = glob.glob(os.path.join(script_path, "multi_test_case/level*_test_*.pkl"))
        if test_single_instance:
            test_cases = glob.glob(
                os.path.join(script_path, f"multi_test_case/level{level}_test_{test}.pkl")
            )
        test_cases.sort()
        # The '2' indicates multi-agent evaluation protocol
        evaluator(get_path, test_cases, debug, visualizer, 2)
