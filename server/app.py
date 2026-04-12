from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---------------------------
# ENV STATE
# ---------------------------
state = {
    "current": (0, 0),
    "remaining": [(2,3), (5,4), (1,7), (6,1)]
}

# ---------------------------
# RESET ENDPOINT
# ---------------------------
@app.post("/reset")
def reset():
    global state
    state = {
        "current": (0, 0),
        "remaining": [(2,3), (5,4), (1,7), (6,1)]
    }
    return {"state": state}

# ---------------------------
# STEP INPUT MODEL
# ---------------------------
class StepInput(BaseModel):
    action: int

# ---------------------------
# STEP ENDPOINT
# ---------------------------
@app.post("/step")
def step(data: StepInput):
    global state

    if not state["remaining"]:
        return {
            "state": state,
            "reward": 0,
            "done": True
        }

    idx = data.action

    if idx >= len(state["remaining"]):
        return {
            "state": state,
            "reward": -10,
            "done": False
        }

    next_loc = state["remaining"].pop(idx)

    # simple reward = -distance
    import math
    curr = state["current"]
    dist = math.sqrt((curr[0]-next_loc[0])**2 + (curr[1]-next_loc[1])**2)

    state["current"] = next_loc

    return {
        "state": state,
        "reward": -dist,
        "done": len(state["remaining"]) == 0
    }