import importlib
DeliveryEnv = None

# Try package-relative import first (when this module is part of a package), otherwise fall back to absolute import.
if __package__:
    try:
        env_mod = importlib.import_module(f"{__package__}.environment")
        DeliveryEnv = getattr(env_mod, "DeliveryEnv")
    except Exception:
        pass

if DeliveryEnv is None:
    try:
        env_mod = importlib.import_module("environment")
        DeliveryEnv = getattr(env_mod, "DeliveryEnv")
    except Exception as e:
        raise ImportError("Could not import DeliveryEnv from environment module") from e

def easy_task():
    return DeliveryEnv({
        "A": {"loc": (2, 3), "deadline": 10},
        "B": {"loc": (5, 1), "deadline": 12},
        "C": {"loc": (1, 6), "deadline": 8},
        "D": {"loc": (7, 7), "deadline": 15},
    })

def medium_task():
    return DeliveryEnv({
        "A": {"loc": (2, 2), "deadline": 10},
        "B": {"loc": (6, 3), "deadline": 15},
        "C": {"loc": (4, 7), "deadline": 12},
        "D": {"loc": (8, 2), "deadline": 18},
        "E": {"loc": (3, 5), "deadline": 14},
    })

def hard_task():
    return DeliveryEnv({
        "A": {"loc": (1, 2), "deadline": 8},
        "B": {"loc": (3, 9), "deadline": 10},
        "C": {"loc": (6, 4), "deadline": 9},
        "D": {"loc": (8, 1), "deadline": 6},
        "E": {"loc": (5, 7), "deadline": 12},
        "F": {"loc": (9, 6), "deadline": 14},
    })