import math
import random

# ==============================
# Distance Function
# ==============================
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# ==============================
# Nearest Neighbor (Greedy)
# ==============================
def nearest_neighbor(locations):
    n = len(locations)
    visited = [False] * n
    route = [0]
    visited[0] = True

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

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue

                a, b = route[i - 1], route[i]
                c, d = route[j - 1], route[j % len(route)]

                before = distance(locations[a], locations[b]) + distance(locations[c], locations[d])
                after = distance(locations[a], locations[c]) + distance(locations[b], locations[d])

                if after < before:
                    route[i:j] = reversed(route[i:j])
                    improved = True

    return route


# ==============================
# Route Distance
# ==============================
def total_distance(route, locations):
    dist = 0
    for i in range(len(route) - 1):
        dist += distance(locations[route[i]], locations[route[i+1]])
    return dist


# ==============================
# Solve Task
# ==============================
def solve_task(task_name, locations):
    print(f"[START] task={task_name}", flush=True)

    # Step 1: Greedy
    route = nearest_neighbor(locations)

    # Step 2: Improve with 2-opt
    route = two_opt(route, locations)

    visited = set([route[0]])
    total_reward = 0
    steps = 0

    current = route[0]

    for next_node in route[1:]:
        reward = -distance(locations[current], locations[next_node])
        total_reward += reward

        print(f"[STEP] step={steps} reward={reward:.6f}", flush=True)

        current = next_node
        visited.add(current)
        steps += 1

    score = -total_reward

    print(f"[END] task={task_name} score={score:.6f} steps={steps}", flush=True)


# ==============================
# MAIN FUNCTION (CRITICAL)
# ==============================
def main():
    # 3 tasks (required by OpenEnv)
    tasks = {
        "easy": [[0, 0], [1, 2], [3, 1], [4, 4]],
        "medium": [[0, 0], [2, 3], [5, 2], [6, 6], [8, 3]],
        "hard": [[0, 0], [1, 5], [3, 3], [6, 7], [8, 2], [9, 9]]
    }

    for name, locs in tasks.items():
        solve_task(name, locs)


# ==============================
# ENTRY POINT (VERY IMPORTANT)
# ==============================
if __name__ == "__main__":
    main()