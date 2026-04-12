import math
import random

random.seed(42)

# ==============================
# Distance
# ==============================
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# ==============================
# Total Distance
# ==============================
def total_distance(route, locations):
    return sum(
        distance(locations[route[i]], locations[route[i+1]])
        for i in range(len(route) - 1)
    )


# ==============================
# Nearest Neighbor from start
# ==============================
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


# ==============================
# 2-OPT Optimization
# ==============================
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


# ==============================
# Multi-start Optimization
# ==============================
def solve_route(locations):
    n = len(locations)
    best_route = None
    best_dist = float("inf")

    # Try multiple starting points
    for start in range(min(n, 5)):
        route = nearest_neighbor(locations, start)
        route = two_opt(route, locations)

        dist = total_distance(route, locations)

        if dist < best_dist:
            best_dist = dist
            best_route = route

    # Random small perturbations (extra improvement)
    for _ in range(3):
        route = best_route[:]
        i, j = sorted(random.sample(range(len(route)), 2))
        route[i:j] = reversed(route[i:j])
        route = two_opt(route, locations)

        dist = total_distance(route, locations)

        if dist < best_dist:
            best_dist = dist
            best_route = route

    return best_route


# ==============================
# Execute Task
# ==============================
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


# ==============================
# MAIN
# ==============================
def main():
    tasks = {
        "easy": [[0, 0], [1, 2], [3, 1], [4, 4]],
        "medium": [[0, 0], [2, 3], [5, 2], [6, 6], [8, 3]],
        "hard": [[0, 0], [1, 5], [3, 3], [6, 7], [8, 2], [9, 9]]
    }

    for name, locs in tasks.items():
        solve_task(name, locs)


# ==============================
# ENTRY POINT (MANDATORY)
# ==============================
if __name__ == "__main__":
    main()