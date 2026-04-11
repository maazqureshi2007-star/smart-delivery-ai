from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import math

app = FastAPI()

class ResetRequest(BaseModel):
    locations: List[List[float]]

class StepRequest(BaseModel):
    current_index: int
    visited: List[int]

env = {
    "locations": []
}

@app.post("/openenv/reset")
def reset_env(req: ResetRequest):
    env["locations"] = req.locations
    return {"status": "ok"}

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

    return {"next_index": best}

@app.post("/openenv/validate")
def validate():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"msg": "API running"}