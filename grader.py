def grade(env):
    total = len(env.deliveries)
    score = 0

    for d in env.deliveries.values():
        if d["done"]:
            score += 1

    # penalty for distance
    score -= 0.05 * env.total_distance

    # penalty for time
    score -= 0.02 * env.time

    return round(score, 2)