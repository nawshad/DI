# From Gemini Output
import functools
import sys

def debug_func_decorator(func):
    """Decorator to log function calls and return values."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log function entry and arguments to stderr
        sys.stderr.write(f"[DEBUG] Calling {func.__name__} with args: {args}, kwargs: {kwargs}\n")

        try:
            # Call the original function
            result = func(*args, **kwargs)
        except Exception as e:
            # Log any exceptions that occur
            sys.stderr.write(f"[DEBUG] Function {func.__name__} raised an exception: {e}\n")
            raise

        # Log function exit and return value
        sys.stderr.write(f"[DEBUG] {func.__name__} returned: {result}\n")
        return result

    return wrapper

@debug_func_decorator
def add(a, b):
    """Adds two numbers."""
    return a + b

@debug_func_decorator
def multiply(x, y, z=1):
    """Multiplies three numbers, with a default value for z."""
    return x * y * z

def test():
    print("Result of add(5, 3):")
    result_add = add(5, 3)
    print(result_add)

    print("\nResult of multiply(2, 4, z=2):")
    result_multiply = multiply(2, 4, z=2)
    print(result_multiply)

if __name__ == "__main__":
    test()