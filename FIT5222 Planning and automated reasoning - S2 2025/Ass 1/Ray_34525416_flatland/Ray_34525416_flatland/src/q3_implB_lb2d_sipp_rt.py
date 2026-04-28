
from lib_piglet.utils.tools import eprint
from typing import List, Tuple, Dict, Set, Optional
import glob, os, sys, heapq, time, random
from collections import deque

try:
    from flatland.core.transition_map import GridTransitionMap
    from flatland.envs.agent_utils import EnvAgent
    from flatland.utils.controller import get_action, Train_Actions, Directions, check_conflict, path_controller, evaluator, remote_evaluator
except Exception as e:
    eprint("Cannot load flatland modules!")
    eprint(e)
    exit(1)




#########################
# Debugger and visualizer options
#########################

# Set these debug option to True if you want more information printed
debug = False
visualizer = False

# If you want to test on specific instance, turn test_single_instance to True and specify the level and test number
test_single_instance = False
level = 6
test = 5

#########################
# Reimplementing the content in get_path() function and replan() function.
#
# They both return a list of paths. A path is a list of (x,y) location tuples.
# The path should be conflict free.
# Hint, you could use some global variables to reuse many resources across get_path/replan frunction calls.
#########################

#########################
# Global caches (cleared per run)
#########################
_NEIGH_CACHE: Dict[Tuple[int,int,int], List[Tuple[int,int,int]]] = {}
_LB2D_CACHE: Dict[Tuple[int,int,Tuple[int,int]], List[List[int]]] = {}
_CORRIDOR_CACHE: Dict[int, Dict[Tuple[int,int], int]] = {}

#########################
# Rail helpers
#########################
DIRS = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)

def _in_bounds(rail: GridTransitionMap, x: int, y: int) -> bool:
    return 0 <= x < rail.height and 0 <= y < rail.width

def _neighbors_uncached(rail: GridTransitionMap, x: int, y: int, d: int):
    trans = rail.get_transitions(x, y, d)
    out = []
    for i, nd in enumerate(DIRS):
        if trans[i]:
            nx, ny = x, y
            if nd == Directions.NORTH: nx -= 1
            elif nd == Directions.EAST: ny += 1
            elif nd == Directions.SOUTH: nx += 1
            elif nd == Directions.WEST: ny -= 1
            out.append((nx, ny, nd))
    return out

def _neighbors(rail: GridTransitionMap, x: int, y: int, d: int):
    key = (x, y, d)
    lst = _NEIGH_CACHE.get(key)
    if lst is not None:
        return lst
    lst = _neighbors_uncached(rail, x, y, d)
    _NEIGH_CACHE[key] = lst
    return lst

def _undir_neighbors(rail: GridTransitionMap, x: int, y: int) -> List[Tuple[int,int]]:
    neigh = set()
    for d in DIRS:
        for nx, ny, _ in _neighbors(rail, x, y, d):
            if _in_bounds(rail, nx, ny):
                neigh.add((nx, ny))
    return list(neigh)

def _adjacent(u: Tuple[int,int], v: Tuple[int,int]) -> bool:
    return u == v or (abs(u[0]-v[0]) + abs(u[1]-v[1]) == 1)

def _dir_to(u: Tuple[int,int], v: Tuple[int,int], fallback: Optional[int]=None) -> int:
    dx, dy = v[0]-u[0], v[1]-u[1]
    if dx == -1 and dy == 0: return Directions.NORTH
    if dx ==  1 and dy == 0: return Directions.SOUTH
    if dx ==  0 and dy == 1: return Directions.EAST
    if dx ==  0 and dy ==-1: return Directions.WEST
    return fallback if fallback is not None else Directions.NORTH

def _is_dead_end(rail: GridTransitionMap, x:int, y:int) -> bool:
    return len(_undir_neighbors(rail, x, y)) == 1

#########################
# 2D goal-based lower bound (tiny memory)
#########################
def _lb2d(rail: GridTransitionMap, goal: Tuple[int,int]) -> List[List[int]]:
    key = (rail.height, rail.width, goal)
    if key in _LB2D_CACHE:
        return _LB2D_CACHE[key]
    H, W = rail.height, rail.width
    INF = 10**9
    dist = [[INF]*W for _ in range(H)]
    gx, gy = goal
    if not (0 <= gx < H and 0 <= gy < W):
        _LB2D_CACHE[key] = dist
        return dist
    q = deque()
    dist[gx][gy] = 0
    q.append((gx, gy))
    while q:
        x, y = q.popleft()
        dxy = dist[x][y] + 1
        for nx, ny in _undir_neighbors(rail, x, y):
            if dist[nx][ny] > dxy:
                dist[nx][ny] = dxy
                q.append((nx, ny))
    _LB2D_CACHE[key] = dist
    return dist

#########################
# Reservations, conflicts, corridors
#########################
def _pad_to(paths: List[List[Tuple[int,int]]], T: int) -> None:
    for p in paths:
        if not p: continue
        while len(p) < T:
            p.append(p[-1])

def _pad(paths: List[List[Tuple[int,int]]]) -> None:
    T = max((len(p) for p in paths if p), default=0)
    _pad_to(paths, T)

def _reservations(paths: List[List[Tuple[int,int]]]) -> Dict[int, List[Tuple[Tuple[int,int],Tuple[int,int]]]]:
    res: Dict[int, List[Tuple[Tuple[int,int],Tuple[int,int]]]] = {}
    if not paths: return res
    T = max((len(p) for p in paths if p), default=0)
    for t in range(max(T, 1)):
        lst = []
        for p in paths:
            if not p: continue
            u = p[t] if t < len(p) else p[-1]
            v = p[t+1] if t+1 < len(p) else p[-1]
            lst.append((u, v))
        res[t] = lst
    return res

def _violates_res(t:int, u:Tuple[int,int], v:Tuple[int,int], res_t:List[Tuple[Tuple[int,int],Tuple[int,int]]]) -> bool:
    for ou, ov in res_t:
        if v == ov: return True
        if u == ov and v == ou: return True
    return False

def _earliest_conflicts(paths: List[List[Tuple[int,int]]]) -> List[Tuple[int,int,int]]:
    out=[]
    if not paths: return out
    T=max((len(p) for p in paths if p), default=0)
    n=len(paths)
    for t in range(T-1):
        pos_t  = [p[t]   if t   < len(p) else p[-1] for p in paths]
        pos_t1 = [p[t+1] if t+1 < len(p) else p[-1] for p in paths]
        # vertex
        seen: Dict[Tuple[int,int], int]={}
        for i,v in enumerate(pos_t1):
            j = seen.get(v)
            if j is not None: out.append((t,i,j))
            else: seen[v]=i
        # edge swap O(n)
        mv_owner: Dict[Tuple[Tuple[int,int],Tuple[int,int]], int] = {}
        for i in range(n):
            a=(pos_t[i],pos_t1[i])
            j = mv_owner.get((a[1],a[0]))
            if j is not None:
                out.append((t,i,j))
            mv_owner[a]=i
    out.sort()
    return out

def _clusters(paths: List[List[Tuple[int,int]]]) -> List[Set[int]]:
    confs=_earliest_conflicts(paths)
    if not confs: return []
    G: Dict[int, Set[int]]={}
    for _,i,j in confs:
        G.setdefault(i,set()).add(j)
        G.setdefault(j,set()).add(i)
    seen=set(); clusters=[]
    for v in G:
        if v in seen: continue
        comp=set([v]); q=[v]; seen.add(v)
        while q:
            u=q.pop()
            for w in G.get(u,()):
                if w not in seen:
                    seen.add(w); q.append(w); comp.add(w)
        clusters.append(comp)
    return clusters

# Corridor detection and tokens
def _compute_corridors(rail: GridTransitionMap) -> Dict[Tuple[int,int], int]:
    H, W = rail.height, rail.width
    deg: Dict[Tuple[int,int], int] = {}
    rail_cells: Set[Tuple[int,int]] = set()
    for x in range(H):
        for y in range(W):
            neigh = _undir_neighbors(rail, x, y)
            if neigh:
                rail_cells.add((x, y))
                deg[(x, y)] = len(neigh)
    corridor_cells = {c for c in rail_cells if deg.get(c, 0) == 2}
    cell2seg: Dict[Tuple[int,int], int] = {}
    seg_id = 0
    visited: Set[Tuple[int,int]] = set()
    for c in corridor_cells:
        if c in visited: continue
        seg_id += 1
        stack = [c]; visited.add(c)
        while stack:
            u = stack.pop()
            cell2seg[u] = seg_id
            for v in _undir_neighbors(rail, u[0], u[1]):
                if v in corridor_cells and v not in visited:
                    visited.add(v); stack.append(v)
    return cell2seg

def _get_cell2seg(rail: GridTransitionMap) -> Dict[Tuple[int,int], int]:
    key = id(rail)
    if key not in _CORRIDOR_CACHE:
        _CORRIDOR_CACHE[key] = _compute_corridors(rail)
    return _CORRIDOR_CACHE[key]

def _move_sign(u: Tuple[int,int], v: Tuple[int,int]) -> int:
    dx, dy = v[0]-u[0], v[1]-u[1]
    if dx == 1: return +1
    if dx == -1: return -1
    if dy == 1: return +1
    if dy == -1: return -1
    return 0

def _segment_timetable(fixed_paths: List[List[Tuple[int,int]]], cell2seg: Dict[Tuple[int,int], int]) -> Dict[int, Dict[int, int]]:
    tokens: Dict[int, Dict[int, int]] = {}
    for p in fixed_paths:
        if not p or len(p) < 2: continue
        t = 0
        while t < len(p)-1:
            u, v = p[t], p[t+1]
            s1 = cell2seg.get(u); s2 = cell2seg.get(v)
            if s1 is None or s2 != s1:
                t += 1; continue
            sign = _move_sign(u, v)
            t0 = t; t += 1
            while t < len(p)-1:
                u2, v2 = p[t], p[t+1]
                if cell2seg.get(u2) != s1 or cell2seg.get(v2) != s1: break
                if _move_sign(u2, v2) != sign: break
                t += 1
            tab = tokens.setdefault(s1, {})
            for tt in range(t0, t):
                tab[tt] = sign
    return tokens

def _violates_corridor_token(t:int, u:Tuple[int,int], v:Tuple[int,int], seg_tokens: Dict[int, Dict[int,int]], cell2seg: Dict[Tuple[int,int], int]) -> bool:
    s1 = cell2seg.get(u); s2 = cell2seg.get(v)
    if s1 is None or s1 != s2: return False
    want = _move_sign(u, v)
    have = seg_tokens.get(s1, {}).get(t, None)
    if have is None: return False
    return have != want

#########################
# Sparse occupancy (intervals) + SIPP-RT
#########################
def _merge_intervals(iv: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    if not iv: return iv
    iv.sort()
    out=[iv[0]]
    for a,b in iv[1:]:
        pa,pb = out[-1]
        if a <= pb+1:
            if b>pb: out[-1]=(pa,b)
        else:
            out.append((a,b))
    return out

def _build_occ_sparse(fixed_paths: List[List[Tuple[int,int]]], H:int) -> Dict[Tuple[int,int], List[Tuple[int,int]]]:
    occ: Dict[Tuple[int,int], List[Tuple[int,int]]] = {}
    for p in fixed_paths:
        if not p: continue
        for t,c in enumerate(p):
            occ.setdefault(c, []).append((t,t))
        if 0 < len(p) <= H:
            last = p[-1]
            occ.setdefault(last, []).append((len(p), H))
    for c in list(occ.keys()):
        occ[c] = _merge_intervals(occ[c])
    return occ

def _safe_from_occ(occ_iv: List[Tuple[int,int]], H:int) -> List[Tuple[int,int]]:
    if not occ_iv: return [(0,H)]
    out=[]; cur=0
    for a,b in occ_iv:
        if cur<=H and cur < a: out.append((cur, min(H, a-1)))
        cur = b+1
    if cur <= H: out.append((cur, H))
    return out

def _iv_idx(iv: List[Tuple[int,int]], t:int) -> int:
    lo,hi=0,len(iv)-1
    while lo<=hi:
        m=(lo+hi)//2
        a,b=iv[m]
        if t<a: hi=m-1
        elif t>b: lo=m+1
        else: return m
    return -1

def _effective_horizon(H:int, lb_from_start:int, slack:int=40) -> int:
    if lb_from_start >= 10**9: return min(H, 500)
    return min(H, lb_from_start + slack)

def _sipp_rt(rail: GridTransitionMap, start: Tuple[int,int], d0:int, goal:Tuple[int,int],
             horizon:int, fixed_paths: List[List[Tuple[int,int]]],
             lb2d: List[List[int]],
             use_corridor_tokens: bool = False,
             cell2seg: Optional[Dict[Tuple[int,int], int]] = None,
             self_wait:int = 0,
             heat_w: float = 0.0) -> List[Tuple[int,int]]:

    lb0 = lb2d[start[0]][start[1]]
    horizon = _effective_horizon(horizon, lb0, slack=40)

    occ = _build_occ_sparse(fixed_paths, horizon)
    if start not in occ: occ[start] = []
    if goal  not in occ: occ[goal]  = []
    iv: Dict[Tuple[int,int], List[Tuple[int,int]]] = {}
    for c, busy in occ.items():
        iv[c] = _safe_from_occ(busy, horizon)
    if _iv_idx(iv[start], 0) == -1: return []

    res = _reservations(fixed_paths)
    seg_tokens = _segment_timetable(fixed_paths, cell2seg or {}) if (use_corridor_tokens and cell2seg) else {}

    heat: Dict[Tuple[Tuple[int,int], int], int] = {}
    if heat_w > 0:
        for p in fixed_paths:
            if not p: continue
            for t in range(min(len(p), horizon+1)):
                heat[(p[t], t)] = heat.get((p[t], t), 0) + 1

    sx,sy=start; gx,gy=goal; INF=10**9
    def H(x,y,_d): 
        h = lb2d[x][y]
        return h if h<INF else abs(x-gx)+abs(y-gy)

    openq: List[Tuple[float,float,int,int,int]]=[]
    parent: Dict[Tuple[int,int,int,int], Tuple[int,int,int,int]]={}
    best_g: Dict[Tuple[int,int,int,int], float] = {}
    heapq.heappush(openq, (H(sx,sy,d0), 0.0, 0, sx, sy, d0))
    best_g[(sx,sy,d0,0)] = 0.0

    while openq:
        f,g,t,x,y,d=heapq.heappop(openq)
        if (x,y)==goal:
            path=[]; node=(x,y,d,t)
            while node in parent:
                path.append((node[0],node[1]))
                node=parent[node]
            path.append((sx,sy)); path.reverse()
            return path
        if t>=horizon: continue

        iv_id=_iv_idx(iv[(x,y)], t)
        if iv_id==-1: continue
        a,b=iv[(x,y)][iv_id]

        # wait
        if t+1<=b:
            u=(x,y); v=(x,y); t2=t+1
            if not _violates_res(t, u, v, res.get(t, [])):
                step = 1.0 + (heat_w * heat.get((v, t2), 0))
                nk=(x,y,d,t2); g2=g+step
                if best_g.get(nk, INF)>g2:
                    best_g[nk]=g2
                    heapq.heappush(openq, (g2+H(x,y,d), g2, t2, x,y, d))
                    parent[nk]=(x,y,d,t)

        # dead-end flip-in-place (handles start-at-dead-end & mid-run)
        if _is_dead_end(rail, x, y) and t+1<=b:
            nbrs = _undir_neighbors(rail, x, y)
            if nbrs:
                ex, ey = nbrs[0]
                nd = _dir_to((x,y), (ex,ey), d)
                if nd != d:
                    u=(x,y); v=(x,y); t2=t+1
                    if not _violates_res(t, u, v, res.get(t, [])):
                        step = 1.0 + (heat_w * heat.get((v, t2), 0))
                        nk=(x,y,nd,t2); g2=g+step
                        if best_g.get(nk, INF)>g2:
                            best_g[nk]=g2
                            heapq.heappush(openq, (g2+H(x,y,nd), g2, t2, x, y, nd))
                            parent[nk]=(x,y,d,t)

        # moves
        if t >= self_wait:
            for nx,ny,nd in _neighbors(rail,x,y,d):
                t2=t+1
                if t2>horizon: continue
                if (nx,ny) not in iv: iv[(nx,ny)] = _safe_from_occ([], horizon)
                if _iv_idx(iv[(nx,ny)], t2)==-1: continue
                u=(x,y); w=(nx,ny)
                if _violates_res(t, u, w, res.get(t, [])): continue
                if use_corridor_tokens and cell2seg:
                    if _violates_corridor_token(t, u, w, seg_tokens, cell2seg): continue
                step = 1.0 + (heat_w * heat.get((w, t2), 0))
                nk=(nx,ny,nd,t2); g2=g+step
                if best_g.get(nk, INF)<=g2: continue
                best_g[nk]=g2
                heapq.heappush(openq, (g2+H(nx,ny,nd), g2, t2, nx, ny, nd))
                parent[nk]=(x,y,d,t)
    return []

#########################
# Deadlines and priority
#########################
def _agent_deadline(a: EnvAgent) -> Optional[int]:
    for key in ("deadline", "ddl", "latest_arrival"):
        if hasattr(a, key):
            try:
                val = int(getattr(a, key))
                return max(0, val)
            except:
                pass
        if hasattr(a, "metadata") and isinstance(a.metadata, dict) and key in a.metadata:
            try:
                return int(a.metadata[key])
            except:
                pass
    return None

def _priority_key(i:int, agents:List[EnvAgent], lb2d:List[List[int]], max_timestep:int):
    a=agents[i]
    sx,sy=a.initial_position
    dist = lb2d[sx][sy]
    ddl  = _agent_deadline(a)
    if ddl is None: ddl = max_timestep
    slack = max(0, ddl - (dist if dist < 10**9 else ddl))
    return (slack, -(dist if dist < 10**9 else 0))

#########################
# CBS for small conflict clusters
#########################
class CBSConstraint:
    def __init__(self, agent:int, t:int, v:Optional[Tuple[int,int]]=None, u:Optional[Tuple[int,int]]=None, w:Optional[Tuple[int,int]]=None):
        self.agent=agent; self.t=t; self.v=v; self.u=u; self.w=w

def _low_level_with_constraints(rail, start, d0, goal, H, fixed_paths, lb2d,
                                cons: List[CBSConstraint],
                                self_wait: int = 0) -> List[Tuple[int,int]]:
    lb0 = lb2d[start[0]][start[1]]
    H = _effective_horizon(H, lb0, slack=40)

    occ = _build_occ_sparse(fixed_paths, H)
    if start not in occ: occ[start] = []
    if goal  not in occ: occ[goal]  = []
    iv: Dict[Tuple[int,int], List[Tuple[int,int]]] = {}
    for c, busy in occ.items():
        iv[c] = _safe_from_occ(busy, H)
    if _iv_idx(iv[start], 0) == -1: return []
    res = _reservations(fixed_paths)

    vtab: Dict[int, Set[Tuple[int,int]]] = {}
    etab: Dict[int, Set[Tuple[Tuple[int,int],Tuple[int,int]]]] = {}
    for c in cons:
        if c.v is not None:
            vtab.setdefault(c.t, set()).add(c.v)
        elif c.u is not None and c.w is not None:
            etab.setdefault(c.t, set()).add((c.u, c.w))

    sx,sy=start; gx,gy=goal; INF=10**9
    def H2(x,y,_d):
        h=lb2d[x][y]
        return h if h<INF else abs(x-gx)+abs(y-gy)

    openq: List[Tuple[float,float,int,int,int]]=[]
    parent: Dict[Tuple[int,int,int,int], Tuple[int,int,int,int]]={}
    best_g: Dict[Tuple[int,int,int,int], float] = {}
    heapq.heappush(openq, (H2(sx,sy,d0), 0.0, 0, sx, sy, d0))
    best_g[(sx,sy,d0,0)] = 0.0

    while openq:
        f,g,t,x,y,d=heapq.heappop(openq)
        if (x,y)==goal:
            path=[]; node=(x,y,d,t)
            while node in parent:
                path.append((node[0],node[1]))
                node=parent[node]
            path.append((sx,sy)); path.reverse()
            return path
        if t>=H: continue

        iv_id=_iv_idx(iv[(x,y)], t)
        if iv_id==-1: continue
        a,b=iv[(x,y)][iv_id]

        # wait
        if t+1<=b:
            u=(x,y); v=(x,y); t2=t+1
            if (t2 not in vtab or v not in vtab[t2]) and not _violates_res(t, u, v, res.get(t, [])):
                step = 1.0
                nk=(x,y,d,t2); g2=g+step
                if best_g.get(nk, INF)>g2:
                    best_g[nk]=g2
                    heapq.heappush(openq, (g2+H2(x,y,d), g2, t2, x, y, d))
                    parent[nk]=(x,y,d,t)

        # dead-end flip-in-place under constraints
        if _is_dead_end(rail, x, y) and t+1<=b:
            nbrs = _undir_neighbors(rail, x, y)
            if nbrs:
                ex, ey = nbrs[0]
                nd = _dir_to((x,y), (ex,ey), d)
                if nd != d:
                    u=(x,y); v=(x,y); t2=t+1
                    if (t2 not in vtab or v not in vtab[t2]) and not _violates_res(t, u, v, res.get(t, [])):
                        step = 1.0
                        nk=(x,y,nd,t2); g2=g+step
                        if best_g.get(nk, INF)>g2:
                            best_g[nk]=g2
                            heapq.heappush(openq, (g2+H2(x,y,nd), g2, t2, x, y, nd))
                            parent[nk]=(x,y,d,t)

        # moves
        if t >= self_wait:
            for nx,ny,nd in _neighbors(rail,x,y,d):
                t2=t+1
                if t2>H: continue
                if (nx,ny) not in iv: iv[(nx,ny)] = _safe_from_occ([], H)
                if _iv_idx(iv[(nx,ny)], t2)==-1: continue
                u=(x,y); w=(nx,ny)
                if (t2 in vtab and w in vtab[t2]): continue
                if (t in etab and (u,w) in etab[t]): continue
                if _violates_res(t, u, w, res.get(t, [])): continue
                step = 1.0
                nk=(nx,ny,nd,t2); g2=g+step
                if best_g.get(nk, INF)<=g2: continue
                best_g[nk]=g2
                heapq.heappush(openq, (g2+H2(nx,ny,nd), g2, t2, nx, ny, nd))
                parent[nk]=(x,y,d,t)
    return []

def _cbs_cluster_solve(agents: List[EnvAgent], rail: GridTransitionMap, max_timestep:int,
                       cluster: Set[int], base_paths: List[List[Tuple[int,int]]],
                       starts: Optional[List[Tuple[int,int]]] = None,
                       dirs:   Optional[List[int]] = None,
                       horizon: Optional[int] = None,
                       waits: Optional[List[int]] = None,
                       time_budget: float = 0.8) -> List[List[Tuple[int,int]]]:
    n=len(agents)
    goals=[a.target for a in agents]
    lbs2d=[_lb2d(rail, goals[i]) for i in range(n)]
    H = horizon if horizon is not None else max_timestep

    class HLNode:
        __slots__=("cost","paths","cons")
        def __init__(self, paths, cons):
            self.paths=paths
            self.cons=cons
            self.cost=sum(len(p)-1 for p in paths if p)
        def __lt__(self, other): return self.cost < other.cost

    def replan_all(cons: List[CBSConstraint]) -> Optional[List[List[Tuple[int,int]]]]:
        paths=[list(p) for p in base_paths]
        cons_per: Dict[int, List[CBSConstraint]]={}
        for c in cons: cons_per.setdefault(c.agent, []).append(c)

        def fixed_for(j:int) -> List[Tuple[int,int]]:
            pj = paths[j]
            wj = 0 if waits is None else waits[j]
            if wj > 0: return [starts[j]]*wj + pj
            return pj

        order = list(cluster)
        order.sort(key=lambda i: _priority_key(i, agents, lbs2d[i], H))

        for i in order:
            s  = starts[i] if starts is not None else (base_paths[i][0] if base_paths[i] else agents[i].initial_position)
            d0 = dirs[i]   if dirs   is not None else agents[i].initial_direction
            fixed = [fixed_for(j) for j in range(n) if j != i]
            wi = 0 if waits is None else waits[i]
            p = _low_level_with_constraints(rail, s, d0, agents[i].target, H, fixed, lbs2d[i],
                                            cons_per.get(i, []), self_wait=wi)
            if not p: return None
            paths[i]=p
        _pad(paths)
        return paths

    init_paths = replan_all([])
    if init_paths is None: return base_paths

    pq: List[HLNode] = [HLNode(init_paths, [])]
    heapq.heapify(pq)
    t_end = time.time() + max(0.2, time_budget)

    while pq and time.time() < t_end:
        node = heapq.heappop(pq)
        confs = [(t,i,j) for (t,i,j) in _earliest_conflicts(node.paths) if (i in cluster or j in cluster)]
        if not confs: return node.paths

        t,i,j = confs[0]
        ui = node.paths[i][t] if t < len(node.paths[i]) else node.paths[i][-1]
        vi = node.paths[i][t+1] if t+1 < len(node.paths[i]) else node.paths[i][-1]
        uj = node.paths[j][t] if t < len(node.paths[j]) else node.paths[j][-1]
        vj = node.paths[j][t+1] if t+1 < len(node.paths[j]) else node.paths[j][-1]

        cons1 = node.cons + ([CBSConstraint(i, t+1, v=vi)] if vi==vj else [CBSConstraint(i, t, u=ui, w=vi)])
        p1 = replan_all(cons1)
        if p1 is not None: heapq.heappush(pq, HLNode(p1, cons1))

        cons2 = node.cons + ([CBSConstraint(j, t+1, v=vj)] if vi==vj else [CBSConstraint(j, t, u=uj, w=vj)])
        p2 = replan_all(cons2)
        if p2 is not None: heapq.heappush(pq, HLNode(p2, cons2))

    return pq[0].paths if pq else base_paths

#########################
# Initial plan: Prioritized SIPP
#########################
def _prioritized_sipp_deadline(agents: List[EnvAgent], rail: GridTransitionMap, H:int) -> List[List[Tuple[int,int]]]:
    n=len(agents)
    goals=[a.target for a in agents]
    lbs2d=[_lb2d(rail, goals[i]) for i in range(n)]
    order=list(range(n))
    order.sort(key=lambda i: _priority_key(i, agents, lbs2d[i], H))
    if n>6:
        tail=max(1,n//8)
        random.shuffle(order[-tail:])

    cell2seg = _get_cell2seg(rail)
    heat_w = 0.1 if (n<=30 and H<=1200) else 0.0

    paths=[[] for _ in range(n)]
    for i in order:
        fixed=[paths[j] for j in range(n) if j != i and paths[j]]
        p=_sipp_rt(rail, agents[i].initial_position, agents[i].initial_direction,
                   agents[i].target, H, fixed, lbs2d[i],
                   use_corridor_tokens=False, cell2seg=cell2seg,
                   self_wait=0, heat_w=heat_w)
        paths[i] = p if p else [agents[i].initial_position]
    _pad(paths)
    return paths

#########################
# LNS (ruin & recreate) with tabu (budgeted)
#########################
def _lns_improve(paths: List[List[Tuple[int,int]]], agents: List[EnvAgent], rail: GridTransitionMap, H:int,
                 time_budget: float = 1.0, max_cluster_size:int = 8) -> List[List[Tuple[int,int]]]:
    start_time = time.time()
    best = [list(p) for p in paths]
    best_conf = len(_earliest_conflicts(best))
    if best_conf == 0: return best

    n=len(agents)
    goals=[a.target for a in agents]
    lbs2d=[_lb2d(rail, goals[i]) for i in range(n)]

    tabu: List[Tuple[int, ...]] = []
    TABU_LEN = 12
    def hash_subset(S:Set[int]) -> Tuple[int,...]:
        return tuple(sorted(S))

    while time.time() - start_time < time_budget:
        confs = _earliest_conflicts(best)
        if not confs: break
        cluster = set()
        t0 = confs[0][0]
        for t,i,j in confs:
            if t > t0 + 6: break
            cluster.update([i,j])
        if len(cluster) < max_cluster_size:
            T = max((len(p) for p in best if p), default=0)
            for t in range(t0, min(T-1, t0+6)):
                pos_t1 = [p[t+1] if t+1 < len(p) else p[-1] for p in best]
                seen: Dict[Tuple[int,int], int] = {}
                for k, v in enumerate(pos_t1):
                    j = seen.get(v)
                    if j is not None: cluster.update([k, j])
                    else: seen[v] = k
                if len(cluster) >= max_cluster_size: break
        if not cluster: break
        key = hash_subset(cluster)
        if key in tabu: continue
        tabu.append(key)
        if len(tabu) > TABU_LEN: tabu.pop(0)

        ct = t0
        cur_pos=[]; cur_dir=[]; waits=[]
        for i,a in enumerate(agents):
            pos = getattr(a,"position",None)
            if pos is None:
                pos = (best[i][ct] if ct < len(best[i]) and best[i] else a.initial_position)
            d = getattr(a,"direction",None)
            if d is None:
                if ct < len(best[i]) and ct > 0 and best[i]:
                    dx,dy = best[i][ct][0]-best[i][ct-1][0], best[i][ct][1]-best[i][ct-1][1]
                    if   dx==-1 and dy==0: d=Directions.NORTH
                    elif dx== 1 and dy==0: d=Directions.SOUTH
                    elif dx==0 and dy== 1: d=Directions.EAST
                    elif dx==0 and dy==-1: d=Directions.WEST
                    else: d=a.initial_direction
                else:
                    d=a.initial_direction
            w=0
            try:
                md=getattr(a,"malfunction_data",None)
                if isinstance(md,dict): w=int(md.get("malfunction",0))
            except: pass
            cur_pos.append(pos); cur_dir.append(d); waits.append(max(0,w))

        base=[]
        for i in range(n):
            if i in cluster: base.append([cur_pos[i]])
            else:
                tail = best[i][ct+1:] if ct+1 < len(best[i]) else []
                base.append([cur_pos[i]] + tail)

        polished=_cbs_cluster_solve(agents, rail, H, cluster, base,
                                    starts=cur_pos, dirs=cur_dir, horizon=max(0, H-ct), waits=waits,
                                    time_budget=0.5)
        new_paths=[[] for _ in range(n)]
        for i in range(n):
            tail = polished[i] if i < len(polished) else [cur_pos[i]]
            if not tail or tail[0] != cur_pos[i]: tail=[cur_pos[i]]+tail
            head = best[i][:ct] if ct <= len(best[i]) else best[i]
            if tail and head and tail[0]==head[-1]: tail=tail[1:]
            new_paths[i]=head+tail
        _pad_to(new_paths, H+1)

        new_conf = len(_earliest_conflicts(new_paths))
        if new_conf < best_conf:
            best, best_conf = new_paths, new_conf
        if best_conf == 0: break

    return best

#########################
# Polish pass (CBS on clusters)
#########################
def _cbs_polish(paths: List[List[Tuple[int,int]]], agents: List[EnvAgent], rail: GridTransitionMap, H:int, time_budget: float=1.0) -> List[List[Tuple[int,int]]]:
    start = time.time()
    best=[list(p) for p in paths]
    while time.time()-start < time_budget:
        confs=_earliest_conflicts(best)
        if not confs: break
        clusters=_clusters(best)
        if not clusters: break
        improved=False
        for C in clusters:
            if time.time()-start >= time_budget: break
            new_paths=_cbs_cluster_solve(agents, rail, H, C, best, time_budget=0.4)
            if len(_earliest_conflicts(new_paths)) < len(_earliest_conflicts(best)):
                best=new_paths; improved=True
        if not improved: break
    return best

#########################
# Replan: clustered repair + tiny LNS
#########################
def _detect_stalled(paths: List[List[Tuple[int,int]]], ct:int, K:int=8) -> Set[int]:
    stalled=set()
    for i,p in enumerate(paths):
        if not p or ct>=len(p): continue
        cell = p[ct]
        ok = True
        for j in range(1, K+1):
            t = ct - j
            if t < 0 or p[t] != cell:
                ok = False
                break
        if ok: stalled.add(i)
    return stalled

def _heading(prev:Tuple[int,int], cur:Tuple[int,int], fallback:int)->int:
    dx,dy = cur[0]-prev[0], cur[1]-prev[1]
    if dx==-1 and dy==0: return Directions.NORTH
    if dx== 1 and dy==0: return Directions.SOUTH
    if dx==0 and dy== 1: return Directions.EAST
    if dx==0 and dy==-1: return Directions.WEST
    return fallback

def _emergency_nudge(out: List[List[Tuple[int,int]]],
                     agents: List[EnvAgent],
                     rail: GridTransitionMap,
                     ct: int,
                     stalled: Set[int]) -> None:
    """Force a single safe step for stalled agents, then hold position (replanned next tick)."""
    n=len(out)
    # Precompute for conflict checks using rolling updates
    for i in sorted(stalled):
        if not out[i] or ct+1 >= len(out[i]): continue
        if out[i][ct] != out[i][ct+1]:
            continue  # already moving
        x,y = out[i][ct]
        cands = _undir_neighbors(rail, x, y)
        if not cands:
            continue
        # Prefer candidates that reduce 2D LB distance
        lb = _lb2d(rail, agents[i].target)
        # Build current others' positions
        def conflict_with(candidate: Tuple[int,int]) -> bool:
            nx,ny = candidate
            for j in range(n):
                if j == i or not out[j]: continue
                uj = out[j][ct]   if ct   < len(out[j]) else out[j][-1]
                vj = out[j][ct+1] if ct+1 < len(out[j]) else out[j][-1]
                # vertex conflict at t+1
                if (nx,ny) == vj: return True
                # edge swap with someone moving into us
                if (x,y) == vj and (nx,ny) == uj: return True
            return False

        best = None
        best_h = 10**9
        for cand in cands:
            if not _adjacent((x,y), cand): continue
            if conflict_with(cand): continue
            h = lb[cand[0]][cand[1]]
            if h < best_h:
                best_h = h
                best = cand

        if best is None:
            # Try any non-conflicting candidate (even if LB doesn't improve)
            for cand in cands:
                if _adjacent((x,y), cand) and not conflict_with(cand):
                    best = cand; break

        if best is not None:
            # Force the first step and then hold position; next replan will pick up
            out[i][ct+1] = best
            for tt in range(ct+2, len(out[i])):
                out[i][tt] = out[i][tt-1]

def _replan_clustered(agents: List[EnvAgent], rail: GridTransitionMap,
                      ct:int, paths: List[List[Tuple[int,int]]], H:int,
                      affected:Set[int], time_budget: float = 1.2) -> List[List[Tuple[int,int]]]:
    n=len(agents)
    stalled = _detect_stalled(paths, ct, K=8)
    affected = set(affected) | stalled

    cur_pos, cur_dir, waits = [], [], []
    for i,a in enumerate(agents):
        pos = getattr(a, "position", None)
        if pos is None:
            pos = (paths[i][ct] if ct < len(paths[i]) and paths[i] else a.initial_position)
        d = getattr(a, "direction", None)
        if d is None:
            if ct < len(paths[i]) and ct > 0 and paths[i]:
                d = _heading(paths[i][ct-1], paths[i][ct], a.initial_direction)
            else:
                d = a.initial_direction
        w=0
        try:
            md=getattr(a,"malfunction_data",None)
            if isinstance(md,dict): w=int(md.get("malfunction",0))
        except: pass
        cur_pos.append(pos); cur_dir.append(d); waits.append(max(0,w))

    prefix=[]
    for i in range(n):
        pre = (paths[i][:ct] if ct <= len(paths[i]) else list(paths[i]))
        if not pre or pre[-1] != cur_pos[i]: pre = pre + [cur_pos[i]]
        prefix.append(pre)

    base=[]
    for i in range(n):
        if i in affected: base.append([cur_pos[i]])
        else:
            tail = paths[i][ct+1:] if ct+1 < len(paths[i]) else []
            base.append([cur_pos[i]] + tail)

    W=6; T=max((len(p) for p in paths if p), default=0)
    cluster=set(affected)
    for t in range(ct, min(T-1, ct+W)):
        pos_t  = [p[t]   if t   < len(p) else p[-1] for p in paths]
        pos_t1 = [p[t+1] if t+1 < len(p) else p[-1] for p in paths]
        seen: Dict[Tuple[int,int], int] = {}
        for i,v in enumerate(pos_t1):
            j = seen.get(v)
            if j is not None: cluster.update([i, j])
            else: seen[v]=i
        for i in range(n):
            for j in range(i+1,n):
                if pos_t[i]==pos_t1[j] and pos_t1[i]==pos_t[j]:
                    cluster.update([i,j])

    rem_H = max(0, H - ct)
    t_end = time.time() + max(0.4, time_budget)

    polished=_cbs_cluster_solve(agents, rail, H, cluster, base,
                                starts=cur_pos, dirs=cur_dir, horizon=rem_H, waits=waits,
                                time_budget=min(0.8, max(0.3, time_budget*0.6)))
    out=[[] for _ in range(n)]
    for i in range(n):
        tail = polished[i] if i < len(polished) else [cur_pos[i]]
        if not tail or tail[0] != cur_pos[i]: tail = [cur_pos[i]] + tail
        if tail and prefix[i] and tail[0] == prefix[i][-1]: tail = tail[1:]
        out[i] = prefix[i] + tail

    # Emergency nudge for trains stuck too long: force any valid step, then hold and replan next tick
    _emergency_nudge(out, agents, rail, ct, stalled)

    remaining = t_end - time.time()
    if remaining > 0.25 and n <= 80:
        out = _lns_improve(out, agents, rail, H, time_budget=min(1.0, remaining), max_cluster_size=6 if n>=50 else 8)

    _pad_to(out, H+1)
    return out

#########################
# Public API
#########################
def _adaptive_budgets(n_agents:int, H:int) -> Tuple[float, float, float]:
    if n_agents <= 20:  return (0.8, 1.0, 1.2)
    if n_agents <= 50:  return (0.8, 0.6, 1.0)
    if n_agents <= 80:  return (0.6, 0.4, 0.9)
    return (0.5, 0.0, 0.8)

def get_path(agents: List[EnvAgent], rail: GridTransitionMap, max_timestep: int):
    _NEIGH_CACHE.clear()
    _LB2D_CACHE.clear()

    n = len(agents)
    base = _prioritized_sipp_deadline(agents, rail, max_timestep)

    polish_budget, lns_budget, _ = _adaptive_budgets(n, max_timestep)
    polished = _cbs_polish(base, agents, rail, max_timestep, time_budget=polish_budget)

    if lns_budget > 0:
        improved = _lns_improve(polished, agents, rail, max_timestep, time_budget=lns_budget,
                                max_cluster_size=(6 if n>=50 else 8))
    else:
        improved = polished

    _pad_to(improved, max_timestep+1)
    return improved

def replan(agents: List[EnvAgent], rail: GridTransitionMap, current_timestep: int,
           existing_paths: List[List[Tuple[int,int]]], max_timestep: int,
           new_malfunction_agents: List[int], failed_agents: List[int]):
    affected=set(new_malfunction_agents) | set(failed_agents)
    _, _, replan_budget = _adaptive_budgets(len(agents), max_timestep)
    out = _replan_clustered(agents, rail, current_timestep, existing_paths, max_timestep, affected,
                            time_budget=replan_budget)
    _pad_to(out, max_timestep+1)
    return out

#####################################################################
# Instantiate a Remote Client
# You should not modify codes below, unless you want to modify test_cases to test specific instance.
#####################################################################
if __name__ == "__main__":

    if len(sys.argv) > 1:
        remote_evaluator(get_path,sys.argv, replan = replan)
    else:
        script_path = os.path.dirname(os.path.abspath(__file__))
        test_cases = glob.glob(os.path.join(script_path, "multi_test_case/level*_test_*.pkl"))

        if test_single_instance:
            test_cases = glob.glob(os.path.join(script_path,"multi_test_case/level{}_test_{}.pkl".format(level, test)))
        test_cases.sort()
        deadline_files =  [test.replace(".pkl",".ddl") for test in test_cases]
        evaluator(get_path, test_cases, debug, visualizer, 3, deadline_files, replan = replan)




