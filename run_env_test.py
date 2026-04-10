"""Small test-run script to sanity-check the DeliveryEnv + grader behaviour.

Run from the project folder:
    python3 run_env_test.py

It will simulate the same tasks used by inference.py and print the scores.
"""

from environment import DeliveryEnv
from grader import grade


def run_simple(deliveries, actions):
    env = DeliveryEnv()
    env.deliveries = deliveries
    env.reset()

    total_reward = 0.0
    for a in actions:
        state, reward, info = env.step(a)
        print(f"Action: {a}, reward={reward}, info={info}")
        total_reward += reward

    s = grade(env)
    print("Final score (grader):", s)
    return s


def main():
    print('Easy task test:')
    easy = {
        "A": {"done": False, "distance": 3, "deadline": 15},
        "B": {"done": False, "distance": 5, "deadline": 20}
    }
    run_simple(easy, ["A", "B"])

    print('\nMedium task test:')
    medium = {
        "A": {"done": False, "distance": 5, "deadline": 10},
        "B": {"done": False, "distance": 8, "deadline": 15},
        "C": {"done": False, "distance": 6, "deadline": 12}
    }
    run_simple(medium, ["A", "B", "C"])


if __name__ == '__main__':
    main()
