import os
import math
from fastapi import FastAPI

# -------------------------------
# FASTAPI APP (HF requirement)
# -------------------------------
app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

# -------------------------------
# SAFE LLM SETUP
# -------------------------------
api_key = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("API_BASE_URL")

print(f"[DEBUG] API_KEY exists: {api_key is not None}", flush=True)
print(f"[DEBUG] API_BASE_URL exists: {base_url is not None}", flush=True)

client = None

# Only initialize if available
if api_key and base_url:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        print("[DEBUG] LLM client initialized", flush=True)
    except Exception as e:
        print(f"[DEBUG] LLM init failed: {e}", flush=True)
else:
    print("[DEBUG] Running without LLM (HF mode)", flush=True)

# -------------------------------
# UTILS
# -------------------------------
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def total_distance(route):
    return sum(distance(route[i], route[i+1]) for i in range(len(route)-1))

# -------------------------------
# DECISION LOGIC
# -------------------------------
def choose_next(current, remaining):
    # USE LLM IF AVAILABLE (this will run in evaluator)
    if client:
        try:
            print("[DEBUG] Calling LLM...", flush=True)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"""
Solve delivery routing.

Current: {current}
Remaining: {remaining}

Return ONLY index of best next location.
"""
                }],
                temperature=0
            )

            idx = int(response.choices[0].message.content.strip())
            print(f"[DEBUG] LLM chose: {idx}", flush=True)

            if 0 <= idx < len(remaining):
                return idx

        except Exception as e:
            print(f"[DEBUG] LLM error: {e}", flush=True)

    # Fallback (HF + safety)
    print("[DEBUG] Using greedy fallback", flush=True)
    dists = [distance(current, loc) for loc in remaining]
    return dists.index(min(dists))

# -------------------------------
# MAIN EXECUTION
# -------------------------------
def main():
    locations = [(0,0), (2,3), (5,4), (1,7), (6,1)]

    current = locations[0]
    remaining = locations[1:]

    print("[START] task=delivery", flush=True)

    step = 0
    route = [current]

    while remaining:
        idx = choose_next(current, remaining)
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