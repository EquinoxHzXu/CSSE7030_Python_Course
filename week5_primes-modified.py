def is_prime(n):
    """Return True if n is a prime number.

    is_prime(int) -> bool
    """
    for i in range(2, n):
        # Check if i is a factor of n
        if n % i == 0:
            return False
    return True


def get_primes(n):
    """Return a list of the first n primes.

    get_primes(int) -> list(int)
    """
    primes = []
    i = 2
    while len(primes) < n:
        if is_prime(i):
            primes.append(i)
        i += 1
    return primes

n = int(input("How many primes? "))
primes = get_primes(n)
print("The first" + str(n) + "primes are:", primes)
