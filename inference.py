import os
import math
from openai import OpenAI

# -------------------------------
# SAFE LLM CLIENT (FIXED)
# -------------------------------
api_key = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("API_BASE_URL")

client = None
if api_key and base_url:
    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

# -------------------------------
# UTILS
# -------------------------------
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def total_distance(route):
    return sum(distance(route[i], route[i+1]) for i in range(len(route)-1))

# -------------------------------
# 2-OPT OPTIMIZATION
# -------------------------------
def two_opt(route):
    best = route[:]
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue
                new_route = best[:]
                new_route[i:j] = best[j-1:i-1:-1]

                if total_distance(new_route) < total_distance(best):
                    best = new_route
                    improved = True
        route = best
    return best

# -------------------------------
# LLM DECISION (SAFE + FALLBACK)
# -------------------------------
def llm_choose_next(current, remaining):
    # If LLM not available → fallback
    if client is None:
        dists = [distance(current, loc) for loc in remaining]
        return dists.index(min(dists))

    try:
        prompt = f"""
You are a smart delivery optimizer.

Current location: {current}
Remaining locations: {remaining}

Return ONLY the index (0-based) of the best next location.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        idx = int(response.choices[0].message.content.strip())

        if 0 <= idx < len(remaining):
            return idx

    except Exception:
        pass

    # fallback → nearest
    dists = [distance(current, loc) for loc in remaining]
    return dists.index(min(dists))

# -------------------------------
# MAIN
# -------------------------------
def main():
    # Simple environment (safe default)
    locations = [
        (0, 0),
        (2, 3),
        (5, 4),
        (1, 7),
        (6, 1)
    ]

    current = locations[0]
    remaining = locations[1:]

    route = [current]

    print("[START] task=delivery", flush=True)

    step = 0
    total_reward = 0

    # -------------------------------
    # STEP LOOP (LLM + fallback)
    # -------------------------------
    while remaining:
        idx = llm_choose_next(current, remaining)
        next_loc = remaining.pop(idx)

        reward = -distance(current, next_loc)
        total_reward += reward

        print(f"[STEP] step={step} reward={reward}", flush=True)

        route.append(next_loc)
        current = next_loc
        step += 1

    # -------------------------------
    # FINAL OPTIMIZATION
    # -------------------------------
    optimized_route = two_opt(route)
    final_score = -total_distance(optimized_route)

    print(f"[END] task=delivery score={final_score} steps={step}", flush=True)


# -------------------------------
# ENTRY POINT (MANDATORY)
# -------------------------------
if __name__ == "__main__":
    main()