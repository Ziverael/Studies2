import pickle
from functools import wraps
from pathlib import Path

def with_pickle(default_pickle_path: Path | None = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pickle_path = kwargs.pop("pickle_path", default_pickle_path)
            if pickle_path is None:
                msg = "Path to pickle must be provided."
                raise ValueError(msg)
            else:
                pickle_path = Path(pickle_path)
            if pickle_path.is_file():
                with pickle_path.open("rb") as f:
                    return pickle.load(f)
            else:
                results = func(*args, **kwargs)
                with pickle_path.open("wb") as f:
                    pickle.dump(results, f)
                return results
        return wrapper
    return decorator
