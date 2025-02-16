import math, secrets


def isPrimeTrialDiv(num):
    """
    Returns True if the number is prime, False otherwise.
    :param num: number
    :return: True if the number is prime, False otherwise
    """

    # All numbers less than 2 are not prime
    if num < 2:
        return False

    #  Checks if num is divisible by any number up to the square root of num
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def primeSieve(sieveSize):
    """
    Returns a list of prime numbers calculated using
    the Sieve of Eratosthenes.
    :param sieveSize: size of the sieve
    :return: list of prime numbers
    """

    sieve = [True] * sieveSize

    # Zero and one are not prime numbers
    sieve[0] = False
    sieve[1] = False

    # Creates the sieve
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # Compiles the list of primes
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes

def rabinMiller(num):
    """
    Returns True if the number is prime, False otherwise.
    :param num: number
    :return: True if the number is prime, False otherwise
    """

    # Rabin-Miller does not work on even integers
    if num % 2 == 0 or num < 2:
        return False
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        # Keeps halving s until it is odd
        # (and uses t to count how many times it was halved)
        s = s // 2
        t += 1

    # Tries to falsify num's primality 5 times
    for trials in range(5):
        a = secrets.randbelow(num - 2) + 2
        v = pow(a, s, num)
        # This does not apply if v == 1
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

# Most of the time we can quickly determine if num is not prime
# by dividing by the first few dozen prime numbers. This is quicker
# than rabinMiller(), but does not detect all composites.
LOW_PRIMES = primeSieve(100)


def isPrime(num):
    """
    Returns True if the number is prime, False otherwise.
    :param num: number
    :return: True if the number is prime, False otherwise
    """

    # Zeor, one and negative numbers are not prime
    if (num < 2):
        return False

    # Checks if the low prime numbers can divide num
    for prime in LOW_PRIMES:
        if (num == prime):
            return True
        if (num % prime == 0):
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime
    return rabinMiller(num)


def generateLargePrime(keysize=4096):
    """
    Returns a random prime number that is keysize bits in size
    :param keysize: size of the prime number
    :return: prime number
    """
    while True:
        num = secrets.randbelow(2**(keysize))
        if isPrime(num):
            return num