import math
import random
import copy


class DeliveryEnv:
    def __init__(self, deliveries=None):
        self.deliveries = deliveries or {}
        self.reset()

    # ---------------- HELPERS ----------------
    def distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    # ---------------- RESET ----------------
    def reset(self):
        random.seed(42)
        
        self.current_location = (0, 0)

        # fallback default (only if nothing passed)
        if not self.deliveries:
            self.deliveries = {
                "A": {"loc": (2, 3), "deadline": 10},
                "B": {"loc": (5, 1), "deadline": 12},
                "C": {"loc": (1, 6), "deadline": 8},
                "D": {"loc": (7, 7), "deadline": 15},
            }

        self.remaining = set(self.deliveries.keys())
        self.completed = []
        self.time = 0
        self.total_distance = 0

        return self.state()

    # ---------------- STATE ----------------
    def state(self):
        return {
            "current_location": self.current_location,
            "remaining_deliveries": list(self.remaining),
            "completed": self.completed,
            "time": self.time,
            "total_distance": round(self.total_distance, 2)
        }

    
    def copy(self):
        return copy.deepcopy(self)

    # ---------------- STEP ----------------
    def step(self, action):
        if action not in self.remaining:
            return self.state(), -1.0, "Invalid or already completed delivery"

        delivery = self.deliveries[action]
        target_loc = delivery["loc"]

        # Travel
        dist = self.distance(self.current_location, target_loc)
        self.total_distance += dist
        self.time += dist

        # Move
        self.current_location = target_loc

        # Reward calculation
        reward = 0

        # Base reward
        reward += 1.0

        # Distance penalty
        reward -= 0.05 * dist

        # Deadline bonus/penalty
        if self.time > delivery["deadline"]:
            reward -= 1.0
            msg = "Late delivery"
        else:
            reward += 0.3
            msg = "On-time delivery"

        # Mark completed
        self.remaining.remove(action)
        self.completed.append(action)
        self.deliveries[action]["done"] = True


        # Bonus if finished all
        if not self.remaining:
            reward += 1.0
            msg += " | All deliveries completed"

        return self.state(), round(reward, 3), msg