from fastapi import FastAPI
from pydantic import BaseModel
import math
import uvicorn

app = FastAPI()

# ---------------------------
# ENV STATE
# ---------------------------
state = {}

def init_env():
    return {
        "current": (0, 0),
        "remaining": [(2,3), (5,4), (1,7), (6,1)]
    }

# ---------------------------
# RESET ENDPOINT
# ---------------------------
@app.post("/reset")
def reset():
    global state
    state = init_env()
    return {"state": state}

# ---------------------------
# STEP INPUT
# ---------------------------
class StepInput(BaseModel):
    action: int

# ---------------------------
# STEP ENDPOINT
# ---------------------------
@app.post("/step")
def step(data: StepInput):
    global state

    if not state:
        state.update(init_env())

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

    curr = state["current"]
    dist = math.sqrt((curr[0]-next_loc[0])**2 + (curr[1]-next_loc[1])**2)

    state["current"] = next_loc

    return {
        "state": state,
        "reward": -dist,
        "done": len(state["remaining"]) == 0
    }

# ---------------------------
# MAIN FUNCTION (REQUIRED)
# ---------------------------
def main():
    print("Starting OpenEnv server...", flush=True)

# ---------------------------
# ENTRY POINT (REQUIRED)
# ---------------------------
if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=7860)