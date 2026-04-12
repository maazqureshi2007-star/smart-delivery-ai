from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import math

app = FastAPI()

<<<<<<< HEAD
# ------------------ MODELS ------------------

=======
>>>>>>> a96bbb8 (final fix - add reset route)
class ResetRequest(BaseModel):
    locations: List[List[float]]

class StepRequest(BaseModel):
    current_index: int
    visited: List[int]

<<<<<<< HEAD
# ------------------ MEMORY ------------------

=======
>>>>>>> a96bbb8 (final fix - add reset route)
env = {
    "locations": []
}

<<<<<<< HEAD
# ------------------ RESET ------------------

=======
# 🔥 SUPPORT BOTH ROUTES
@app.post("/reset")
>>>>>>> a96bbb8 (final fix - add reset route)
@app.post("/openenv/reset")
def reset_env(req: ResetRequest):
    env["locations"] = req.locations
    return {"status": "ok"}

<<<<<<< HEAD
# ------------------ STEP ------------------

@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env.get("locations", [])

    # SAFETY: empty locations
    if not locations:
        return {"next_index": 0}

    # SAFETY: invalid current index
    if req.current_index >= len(locations):
        return {"next_index": 0}

    visited = set(req.visited)
    current = req.current_index

=======

@app.post("/step")
@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env["locations"]
    visited = set(req.visited)

    current = req.current_index
>>>>>>> a96bbb8 (final fix - add reset route)
    best = current
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

    return {"next_index": best}

<<<<<<< HEAD
# ------------------ VALIDATE ------------------

=======

@app.post("/validate")
>>>>>>> a96bbb8 (final fix - add reset route)
@app.post("/openenv/validate")
def validate():
    return {"status": "ok"}

<<<<<<< HEAD
# ------------------ ROOT ------------------
=======
>>>>>>> a96bbb8 (final fix - add reset route)

@app.get("/")
def home():
    return {"msg": "API running"}