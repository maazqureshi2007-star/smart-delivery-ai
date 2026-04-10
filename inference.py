from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import math

app = FastAPI()

# -----------------------------
# DATA MODELS
# -----------------------------
class ResetRequest(BaseModel):
    locations: List[List[float]]  # [[lat, lon], ...]

class StepRequest(BaseModel):
    current_index: int
    visited: List[int]

# -----------------------------
# GLOBAL STATE (simple env)
# -----------------------------
env = {
    "locations": [],
    "visited": [],
    "current_index": 0
}

# -----------------------------
# RESET ENDPOINT
# -----------------------------
@app.post("/openenv/reset")
def reset_env(req: ResetRequest):
    env["locations"] = req.locations
    env["visited"] = []
    env["current_index"] = 0

    return {
        "status": "reset successful",
        "num_locations": len(req.locations)
    }

# -----------------------------
# STEP (AI decision)
# -----------------------------
@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env["locations"]
    visited = set(req.visited)

    current = req.current_index

    best = None
    best_dist = float("inf")

    for i, loc in enumerate(locations):
        if i in visited:
            continue

        dist = math.sqrt(
            (locations[current][0] - loc[0])**2 +
            (locations[current][1] - loc[1])**2
        )

        if dist < best_dist:
            best_dist = dist
            best = i

    return {
        "next_index": best,
        "distance": best_dist
    }

# -----------------------------
# VALIDATE
# -----------------------------
@app.post("/openenv/validate")
def validate():
    return {
        "status": "valid",
        "message": "Environment working correctly"
    }