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
# Utility function
# -----------------------------
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# -----------------------------
# RESET (handles empty body)
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
# STEP (IMPROVED LOGIC 🚀)
# -----------------------------
@app.post("/step")
@app.post("/openenv/step")
def step(req: StepRequest):
    locations = env["locations"]
    visited = set(req.visited)

    current = req.current_index
    best = current
    best_score = float("inf")

    for i, loc in enumerate(locations):
        if i in visited:
            continue

        # 1️⃣ distance from current → candidate
        d1 = distance(locations[current], loc)

        # 2️⃣ lookahead: best next move from candidate
        d2 = float("inf")
        for j, loc2 in enumerate(locations):
            if j != i and j not in visited:
                d2 = min(d2, distance(loc, loc2))

        # 3️⃣ isolation penalty (avoid leaving far points last)
        isolation = 0
        count = 0
        for j, loc2 in enumerate(locations):
            if j != i and j not in visited:
                isolation += distance(loc, loc2)
                count += 1

        if count > 0:
            isolation = isolation / count

        # 🔥 FINAL SCORE
        score = d1 + 0.6 * d2 + 0.1 * isolation

        # 🎲 Tie-breaking randomness (important!)
        if score < best_score or (abs(score - best_score) < 1e-6 and random.random() < 0.3):
            best_score = score
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