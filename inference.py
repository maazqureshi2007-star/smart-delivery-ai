from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional
import math
import random

app = FastAPI()

# -----------------------------
# Request Models
# -----------------------------
class ResetRequest(BaseModel):
    locations: List[List[float]]

class StepRequest(BaseModel):
    current_index: int
    visited: List[int]

# -----------------------------
# In-memory environment
# -----------------------------
env = {
    "locations": []
}

# -----------------------------
# Utility
# -----------------------------
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# -----------------------------
# RESET
# -----------------------------
@app.post("/reset")
@app.post("/openenv/reset")
def reset_env(req: Optional[ResetRequest] = Body(None)):
    if req and req.locations:
        env["locations"] = req.locations
    else:
        env["locations"] = []
    return {"status": "ok"}

# -----------------------------
# 🔥 BEAM SEARCH STEP (TOP LEVEL)
# -----------------------------
@app.post("/step")
@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env["locations"]
    n = len(locations)
    visited = set(req.visited)
    current = req.current_index

    # candidates
    candidates = [i for i in range(n) if i not in visited]

    if not candidates:
        return {"next_index": current}

    BEAM_WIDTH = 3      # try multiple paths
    DEPTH = 3           # lookahead steps

    def simulate(path, current_node, visited_set, depth):
        """simulate future cost"""
        if depth == 0:
            return 0

        best_cost = float("inf")

        for nxt in range(n):
            if nxt not in visited_set:
                d = distance(locations[current_node], locations[nxt])
                cost = d + simulate(
                    path + [nxt],
                    nxt,
                    visited_set | {nxt},
                    depth - 1
                )
                best_cost = min(best_cost, cost)

        return best_cost if best_cost != float("inf") else 0

    # evaluate each candidate using beam-like scoring
    scored = []

    for i in candidates:
        d1 = distance(locations[current], locations[i])

        future_cost = simulate(
            [i],
            i,
            visited | {i},
            DEPTH - 1
        )

        score = d1 + 0.7 * future_cost

        scored.append((score, i))

    # sort candidates
    scored.sort()

    # pick best but add slight randomness (important)
    top_k = scored[:BEAM_WIDTH]
    _, best = random.choice(top_k)

    return {"next_index": best}

# -----------------------------
# VALIDATE
# -----------------------------
@app.post("/validate")
@app.post("/openenv/validate")
def validate():
    return {"status": "ok"}

# -----------------------------
# HEALTH
# -----------------------------
@app.get("/")
def home():
    return {"msg": "API running"}