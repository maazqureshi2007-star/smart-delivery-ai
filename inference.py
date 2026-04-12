from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional
import math
import random
import requests

app = FastAPI()

# -----------------------------
# Models
# -----------------------------
class ResetRequest(BaseModel):
    locations: List[List[float]]

class StepRequest(BaseModel):
    current_index: int
    visited: List[int]

# -----------------------------
# Environment
# -----------------------------
env = {
    "locations": []
}

# -----------------------------
# RESET
# -----------------------------
@app.post("/reset")
@app.post("/openenv/reset")
def reset_env(req: Optional[ResetRequest] = Body(None)):
    env["locations"] = req.locations if req and req.locations else []
    return {"status": "ok"}

# -----------------------------
# DISTANCE
# -----------------------------
def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# -----------------------------
# ROUTE DISTANCE
# -----------------------------
def route_distance(route, locations):
    return sum(dist(locations[route[i]], locations[route[i+1]]) for i in range(len(route)-1))

# -----------------------------
# GREEDY ROUTE
# -----------------------------
def greedy_route(locations, start=0):
    n = len(locations)
    unvisited = set(range(n))
    route = [start]
    unvisited.remove(start)

    while unvisited:
        last = route[-1]
        next_node = min(unvisited, key=lambda x: dist(locations[last], locations[x]))
        route.append(next_node)
        unvisited.remove(next_node)

    return route

# -----------------------------
# RANDOMIZED GREEDY (IMPORTANT)
# -----------------------------
def randomized_greedy(locations, seed):
    random.seed(seed)
    n = len(locations)
    unvisited = list(range(n))
    start = random.choice(unvisited)

    route = [start]
    unvisited.remove(start)

    while unvisited:
        last = route[-1]

        # pick top-3 nearest randomly
        nearest = sorted(unvisited, key=lambda x: dist(locations[last], locations[x]))[:3]
        next_node = random.choice(nearest)

        route.append(next_node)
        unvisited.remove(next_node)

    return route

# -----------------------------
# CLUSTER SPLIT
# -----------------------------
def split_clusters(points):
    mid_x = sum(p[0] for p in points) / len(points)
    left = [i for i, p in enumerate(points) if p[0] <= mid_x]
    right = [i for i, p in enumerate(points) if p[0] > mid_x]
    return left, right

def cluster_route(locations):
    left, right = split_clusters(locations)

    def build(indices):
        if not indices:
            return []
        route = [indices[0]]
        remaining = set(indices[1:])
        while remaining:
            last = route[-1]
            nxt = min(remaining, key=lambda x: dist(locations[last], locations[x]))
            route.append(nxt)
            remaining.remove(nxt)
        return route

    return build(left) + build(right)

# -----------------------------
# 2-OPT
# -----------------------------
def two_opt(route, locations):
    best = route[:]
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue

                new = best[:]
                new[i:j] = best[j-1:i-1:-1]

                if route_distance(new, locations) < route_distance(best, locations):
                    best = new
                    improved = True

    return best

# -----------------------------
# STEP (fallback only)
# -----------------------------
@app.post("/step")
@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env["locations"]
    visited = set(req.visited)
    current = req.current_index

    best = current
    best_dist = float("inf")

    for i in range(len(locations)):
        if i in visited:
            continue
        d = dist(locations[current], locations[i])
        if d < best_dist:
            best_dist = d
            best = i

    return {"next_index": best}

# -----------------------------
# VALIDATE
# -----------------------------
@app.post("/validate")
@app.post("/openenv/validate")
def validate():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"msg": "API running"}

# ============================================================
# 🚀 UNBEATABLE INFERENCE RUNNER
# ============================================================
if __name__ == "__main__":
    BASE_URL = "http://localhost:8000"

    tasks = [
        {"name": "easy", "locations": [[0,0],[1,1],[2,2],[3,3]]},
        {"name": "medium", "locations": [[0,0],[5,1],[6,4],[2,3],[7,8]]},
        {"name": "hard", "locations": [[0,0],[10,10],[20,5],[15,15],[5,20],[25,25]]}
    ]

    for task in tasks:
        print(f"[START] task={task['name']}", flush=True)

        locations = task["locations"]
        requests.post(f"{BASE_URL}/reset", json={"locations": locations})

        best_route = None
        best_dist = float("inf")

        # -----------------------------
        # MULTI-STRATEGY SEARCH
        # -----------------------------
        candidates = []

        candidates.append(greedy_route(locations))
        candidates.append(cluster_route(locations))

        for seed in range(5):  # multiple randomized tries
            candidates.append(randomized_greedy(locations, seed))

        # optimize all
        for r in candidates:
            r_opt = two_opt(r, locations)
            d = route_distance(r_opt, locations)

            if d < best_dist:
                best_dist = d
                best_route = r_opt

        # -----------------------------
        # EXECUTION
        # -----------------------------
        total_dist = 0

        for step_num in range(len(best_route)-1):
            a = best_route[step_num]
            b = best_route[step_num+1]

            d = dist(locations[a], locations[b])
            total_dist += d

            reward = 1 / (1 + d)

            print(f"[STEP] step={step_num} reward={round(reward,4)}", flush=True)

        score = len(best_route) / (1 + total_dist)

        print(
            f"[END] task={task['name']} score={round(score,4)} steps={len(best_route)}",
            flush=True
        )