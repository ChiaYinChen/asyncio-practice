"""Utils function."""
import functools
import time


def timer(func):
    """Logging function run time."""
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'{func.__globals__["__file__"]!r} executed in {run_time:.4f} secs')  # noqa: E501
        return value
    return wrapper_decorator
