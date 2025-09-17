from functools import wraps
import time
import random

def exponential_backoff(no_of_attempts: int = 10, factor: int = 2, initial_delay: float = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt_number = 0
            while attempt_number < no_of_attempts:
                try:
                    result = func(*args, **kwargs)
                    print(f"succeeded in {attempt_number} attempts")
                    return result
                except Exception as e:
                    delay = initial_delay*(factor**attempt_number)*random.uniform(0.8, 1.2)
                    print(f"Failed attempt {attempt_number + 1}: {e}. Retrying in {delay:.2f} seconds")
                    attempt_number += 1
                    time.sleep(delay)
            raise RuntimeError(f"Function '{func.__name__}' failed after {no_of_attempts} attempts")
        return wrapper
    return decorator


@exponential_backoff()
def throws_up_randomly(a: int, b :int, op: str = '+'):
    if random.random() < 0.75:
        raise RuntimeError("Simulated failure")
    
    operator_map = {
        '+': lambda x,y: x+y,
        '-': lambda x,y: x-y,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
    }
    return operator_map[op](a,b)


if __name__ == '__main__':
    a, b, op = 1,2,"+"
    print(throws_up_randomly(a, b, op))
    
                    
            
            