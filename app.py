from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "<h1>UI missing</h1>"

# ---------------- SIMPLE ROUTE (dummy) ----------------
@app.get("/route")
def route():
    return {"msg": "ok"}

# ---------------- HEATMAP ----------------
@app.get("/heatmap")
def heatmap():
    return {"points": [[21.5, 72.8, 2]]}

# ---------------- RUN ----------------
@app.get("/run")
def run():
    return {
        "vehicles": [
            [{"location": [0.1, 0.2]}, {"location": [0.3, 0.4]}]
        ]
    }

# ---------------- OPENENV STATE ----------------
env_state = {
    "remaining": ["task1", "task2", "task3"],
    "completed": []
}

# 🚨 MOST IMPORTANT ENDPOINT (RESET)
@app.post("/openenv/reset")
def reset():
    global env_state

    env_state = {
        "remaining": ["task1", "task2", "task3"],
        "completed": []
    }

    return {
        "state": env_state
    }

# 🚨 STEP
@app.post("/openenv/step")
def step(action: str):
    global env_state

    if action in env_state["remaining"]:
        env_state["remaining"].remove(action)
        env_state["completed"].append(action)
        reward = 1
        done = len(env_state["remaining"]) == 0
    else:
        reward = 0
        done = False

    return {
        "state": env_state,
        "reward": reward,
        "done": done
    }

# OPTIONAL
@app.get("/openenv/status")
def status():
    return env_state