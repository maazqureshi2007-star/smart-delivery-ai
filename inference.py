from fastapi import FastAPI
import math
import random

app = FastAPI()

random.seed(42)

# ==============================
# Distance
# ==============================
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# ==============================
# API (for Phase 1)
# ==============================
env = {"locations": []}

@app.post("/reset")
@app.post("/openenv/reset")
def reset_env(data: dict = None):
    if data and "locations" in data:
        env["locations"] = data["locations"]
    else:
        env["locations"] = []
    return {"status": "ok"}


@app.post("/step")
@app.post("/openenv/step")
def step(data: dict):
    locations = env["locations"]
    current = data["current_index"]
    visited = set(data["visited"])

    best = None
    best_dist = float("inf")

    for i, loc in enumerate(locations):
        if i not in visited:
            d = distance(locations[current], loc)
            if d < best_dist:
                best_dist = d
                best = i

    return {"next_index": best}


@app.post("/validate")
@app.post("/openenv/validate")
def validate():
    return {"status": "ok"}


@app.get("/")
def home():
    return {"msg": "API running"}


# ==============================
# INFERENCE LOGIC (Phase 2)
# ==============================
def total_distance(route, locations):
    return sum(
        distance(locations[route[i]], locations[route[i+1]])
        for i in range(len(route) - 1)
    )


def nearest_neighbor(locations, start):
    n = len(locations)
    visited = [False] * n
    route = [start]
    visited[start] = True

    for _ in range(n - 1):
        last = route[-1]
        best = None
        best_dist = float("inf")

        for i in range(n):
            if not visited[i]:
                d = distance(locations[last], locations[i])
                if d < best_dist:
                    best_dist = d
                    best = i

        route.append(best)
        visited[best] = True

    return route


def two_opt(route, locations):
    improved = True
    best = route[:]

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue

                new_route = best[:]
                new_route[i:j] = reversed(new_route[i:j])

                if total_distance(new_route, locations) < total_distance(best, locations):
                    best = new_route
                    improved = True

        route = best

    return best


def solve_route(locations):
    n = len(locations)
    best_route = None
    best_dist = float("inf")

    for start in range(min(n, 5)):
        route = nearest_neighbor(locations, start)
        route = two_opt(route, locations)

        dist = total_distance(route, locations)

        if dist < best_dist:
            best_dist = dist
            best_route = route

    return best_route


def solve_task(task_name, locations):
    print(f"[START] task={task_name}", flush=True)

    route = solve_route(locations)

    total_reward = 0
    steps = 0
    current = route[0]

    for next_node in route[1:]:
        reward = -distance(locations[current], locations[next_node])
        total_reward += reward

        print(f"[STEP] step={steps} reward={reward:.6f}", flush=True)

        current = next_node
        steps += 1

    score = -total_reward

    print(f"[END] task={task_name} score={score:.6f} steps={steps}", flush=True)


def main():
    tasks = {
        "easy": [[0, 0], [1, 2], [3, 1], [4, 4]],
        "medium": [[0, 0], [2, 3], [5, 2], [6, 6], [8, 3]],
        "hard": [[0, 0], [1, 5], [3, 3], [6, 7], [8, 2], [9, 9]]
    }

    for name, locs in tasks.items():
        solve_task(name, locs)


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    main()