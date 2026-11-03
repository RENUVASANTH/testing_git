
from functools import lru_cache, wraps
from time import perf_counter


# 1. Decorator to measure execution time
def timed(func):
    """Decorator that prints function execution time."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)

        elapsed = perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f} seconds")

        return result

    return wrapper


# 2. Fibonacci using recursion and caching
@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


# 3. Generator to read a file line by line
def read_lines(filename):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()


# 4. Match-case number classifier
def classify_number(n):
    match n:
        case 0:
            return "Zero"
        case n if n > 0:
            return "Positive"
        case n if n < 0:
            return "Negative"


# 5. Main program
@timed
def main():
    print("Fibonacci:", fib(10))

    print("Number classification:", classify_number(5))

    print("Reading lines from sample.txt:")
    for line in read_lines("sample.txt"):
        print(line)


if __name__ == "__main__":
    main()
