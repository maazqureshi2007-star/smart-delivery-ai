from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional
import math

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
# RESET (FIXED FOR EMPTY BODY)
# -----------------------------
@app.post("/reset")
@app.post("/openenv/reset")
def reset_env(req: Optional[ResetRequest] = Body(None)):
    if req and req.locations:
        env["locations"] = req.locations
    else:
        env["locations"] = []   # fallback if no body
    return {"status": "ok"}

# -----------------------------
# STEP
# -----------------------------
@app.post("/step")
@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env["locations"]
    visited = set(req.visited)

    current = req.current_index
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

# -----------------------------
# VALIDATE
# -----------------------------
@app.post("/validate")
@app.post("/openenv/validate")
def validate():
    return {"status": "ok"}

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def home():
    return {"msg": "API running"}