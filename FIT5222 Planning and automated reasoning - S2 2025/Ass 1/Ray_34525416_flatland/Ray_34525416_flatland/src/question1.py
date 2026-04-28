"""
This is the python script for question 1. 
In this script, you are required to implement a single agent path-finding algorithm.
"""

# Utility import: eprint is a custom error-printing function from piglet utilities.
from lib_piglet.utils.tools import eprint

# Standard Python libraries
import glob, os, sys
from heapq import heappush, heappop  # heap functions used for priority queue in A* search

# Try importing Flatland modules. If fail, exit gracefully.
try:
    from flatland.core.transition_map import GridTransitionMap
    from flatland.utils.controller import (
        get_action, Train_Actions, Directions, check_conflict, 
        path_controller, evaluator, remote_evaluator
    )
except Exception as e:
    eprint("Cannot load flatland modules!")
    eprint(e)
    exit(1)

#########################
# Debugger and visualizer options
#########################

# Set these debug options to True if you want extra information printed
debug = False
visualizer = False

# Run only one instance if set to True (helps debugging)
test_single_instance = False
level = 0   # choose level for single test
test = 0    # choose test case index

#########################
# Pathfinding implementation
#########################

# Function: get_path
# This function computes a path from start to goal using A* search.
#
# Args:
#   start: (x, y) start location
#   start_direction: integer for initial facing direction
#   goal: (x, y) target location
#   rail: Flatland GridTransitionMap (describes tracks and moves allowed)
#   max_timestep: maximum timesteps allowed for simulation (not strictly used here)
#
# Returns:
#   path: list of (x, y) coordinates from start to goal
def get_path(start: tuple, start_direction: int, goal: tuple, rail: GridTransitionMap, max_timestep: int):

    # Heuristic function: Manhattan distance between a point and the goal
    def h(p):
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])

    # State includes position + direction
    start_state = (start[0], start[1], start_direction)
    goal_cells = {(goal[0], goal[1])}  # set for faster lookup

    # Priority queue (min-heap) storing nodes as (f, g, state)
    open_heap = []
    heappush(open_heap, (h(start), 0, start_state))

    # Dictionaries to reconstruct path
    came_from = {}   # state -> parent state
    g_cost = {start_state: 0}  # actual cost from start
    closed = set()   # visited states

    # Main A* loop
    while open_heap:
        f, g, (x, y, d) = heappop(open_heap)

        # Check if reached goal
        if (x, y) in goal_cells:
            path = []
            s = (x, y, d)
            # Backtrack through parents to build path
            while s in came_from:
                path.append((s[0], s[1]))
                s = came_from[s]
            path.append((start_state[0], start_state[1]))
            path.reverse()
            return path

        # Skip if already processed
        if (x, y, d) in closed:
            continue
        closed.add((x, y, d))

        # Expand successors: check valid rail transitions from current (x, y, dir)
        transitions = rail.get_transitions(x, y, d)
        # transitions is iterable over [N, E, S, W], truthy if move is possible
        for new_dir, allowed in enumerate(transitions):
            if not allowed:
                continue

            # Compute new coordinates based on direction
            nx, ny = x, y
            if new_dir == Directions.NORTH:
                nx -= 1
            elif new_dir == Directions.EAST:
                ny += 1
            elif new_dir == Directions.SOUTH:
                nx += 1
            elif new_dir == Directions.WEST:
                ny -= 1

            ns = (nx, ny, new_dir)
            tentative_g = g + 1  # assume uniform step cost

            # Skip if we already have a better path to this state
            if ns in g_cost and tentative_g >= g_cost[ns]:
                continue

            # Record best path so far
            g_cost[ns] = tentative_g
            came_from[ns] = (x, y, d)
            heappush(open_heap, (tentative_g + h((nx, ny)), tentative_g, ns))

    # If no path found, return just the start point (prevents crash)
    return [start]

#########################
# Evaluation / Testing
#########################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If script called with arguments, use remote evaluator
        remote_evaluator(get_path, sys.argv)
    else:
        # Otherwise, run local test cases
        script_path = os.path.dirname(os.path.abspath(__file__))
        test_cases = glob.glob(os.path.join(script_path, "single_test_case/level*_test_*.pkl"))
        
        # Optionally run only one chosen test case
        if test_single_instance:
            test_cases = glob.glob(
                os.path.join(script_path, "single_test_case/level{}_test_{}.pkl".format(level, test))
            )
        
        test_cases.sort()
        evaluator(get_path, test_cases, debug, visualizer, 1)
