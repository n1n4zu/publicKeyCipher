import math
import secrets

class PrimeNum:
    LOW_PRIMES = None

    @staticmethod
    def isPrimeTrialDiv(num):
        """
Returns True if the number is prime, False otherwise.
:param num: number
:return: True if the number is prime, False otherwise
        """
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    @staticmethod
    def primeSieve(sieveSize):
        """
Returns a list of prime numbers calculated using
the Sieve of Eratosthenes.
:param sieveSize: size of the sieve
:return: list of prime numbers
        """
        sieve = [True] * sieveSize
        sieve[0] = False
        sieve[1] = False
        for i in range(2, int(math.sqrt(sieveSize)) + 1):
            pointer = i * 2
            while pointer < sieveSize:
                sieve[pointer] = False
                pointer += i
        primes = [i for i, is_prime in enumerate(sieve) if is_prime]
        return primes

    @staticmethod
    def rabinMiller(num):
        """
Returns True if the number is prime, False otherwise.
:param num: number
:return: True if the number is prime, False otherwise
        """
        if num % 2 == 0 or num < 2:
            return False
        if num == 3:
            return True
        s = num - 1
        t = 0
        while s % 2 == 0:
            s = s // 2
            t += 1
        for trials in range(5):
            a = secrets.randbelow(num - 2) + 2
            v = pow(a, s, num)
            if v != 1:
                i = 0
                while v != (num - 1):
                    if i == t - 1:
                        return False
                    else:
                        i = i + 1
                        v = (v ** 2) % num
        return True

    @classmethod
    def isPrime(cls, num):
        """
Returns True if the number is prime, False otherwise.
:param num: number
:return: True if the number is prime, False otherwise
        """
        if num < 2:
            return False
        if cls.LOW_PRIMES is None:
            cls.LOW_PRIMES = cls.primeSieve(100)
        for prime in cls.LOW_PRIMES:
            if num == prime:
                return True
            if num % prime == 0:
                return False
        return cls.rabinMiller(num)

    @staticmethod
    def generateLargePrime(keysize=4096):
        """
Returns a random prime number that is keysize bits in size
:param keysize: size of the prime number
:return: prime number
        """
        while True:
            num = secrets.randbelow(2 ** keysize)
            if PrimeNum.isPrime(num):
                return num