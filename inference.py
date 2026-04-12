import os
import math
from openai import OpenAI

# -------------------------------
# FASTAPI APP (FIX FOR HF)
# -------------------------------
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "running"}

# -------------------------------
# LLM CLIENT
# -------------------------------
api_key = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("API_BASE_URL")

client = None
if api_key and base_url:
    client = OpenAI(base_url=base_url, api_key=api_key)

# -------------------------------
# UTILS
# -------------------------------
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def total_distance(route):
    return sum(distance(route[i], route[i+1]) for i in range(len(route)-1))

# -------------------------------
# LLM DECISION
# -------------------------------
def llm_choose_next(current, remaining):
    if client is None:
        return 0

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"Current: {current}, Remaining: {remaining}. Return index."
            }],
            temperature=0
        )
        return int(response.choices[0].message.content.strip())
    except:
        return 0

# -------------------------------
# MAIN LOGIC
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