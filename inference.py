import os
import math
from openai import OpenAI

# -------------------------------
# FASTAPI APP (HF FIX)
# -------------------------------
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

# -------------------------------
# ENV + DEBUG (VERY IMPORTANT)
# -------------------------------
api_key = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("API_BASE_URL")

print(f"[DEBUG] API_KEY exists: {api_key is not None}", flush=True)
print(f"[DEBUG] API_BASE_URL exists: {base_url is not None}", flush=True)

client = None
if api_key and base_url:
    client = OpenAI(base_url=base_url, api_key=api_key)

print(f"[DEBUG] Using LLM client: {client is not None}", flush=True)

# -------------------------------
# UTILS
# -------------------------------
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def total_distance(route):
    return sum(distance(route[i], route[i+1]) for i in range(len(route)-1))

# -------------------------------
# LLM DECISION (DEBUG ADDED)
# -------------------------------
def llm_choose_next(current, remaining):
    if client is None:
        print("[DEBUG] LLM NOT USED → fallback greedy", flush=True)
        dists = [distance(current, loc) for loc in remaining]
        return dists.index(min(dists))

    try:
        print("[DEBUG] Calling LLM...", flush=True)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"Current: {current}, Remaining: {remaining}. Return index only."
            }],
            temperature=0
        )

        idx = int(response.choices[0].message.content.strip())

        print(f"[DEBUG] LLM chose index: {idx}", flush=True)

        if 0 <= idx < len(remaining):
            return idx

    except Exception as e:
        print(f"[DEBUG] LLM ERROR: {e}", flush=True)

    # fallback
    print("[DEBUG] Fallback after LLM failure", flush=True)
    dists = [distance(current, loc) for loc in remaining]
    return dists.index(min(dists))

# -------------------------------
# MAIN
# -------------------------------
def main():
    locations = [(0,0), (2,3), (5,4), (1,7), (6,1)]

    current = locations[0]
    remaining = locations[1:]

    print("[START] task=delivery", flush=True)

    step = 0
    route = [current]

    while remaining:
        idx = llm_choose_next(current, remaining)
        next_loc = remaining.pop(idx)

        reward = -distance(current, next_loc)

        print(f"[STEP] step={step} reward={reward}", flush=True)

        route.append(next_loc)
        current = next_loc
        step += 1

    score = -total_distance(route)

    print(f"[END] task=delivery score={score} steps={step}", flush=True)

# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()