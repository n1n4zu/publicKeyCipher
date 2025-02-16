def gcd(a, b):
    """
    Returns the greatest common divisor of a and b
    :param a: first number
    :param b: second number
    :return: greatest common divisor
    """
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    """
    Returns the modular multiplicative inverse of a modulo m
    :param a: number
    :param m: modulo
    :return: modular multiplicative inverse
    """
    if gcd(a, m) != 1:
        return None # No mod inverse if a and m are not relatively prime

    # Calculates using the Extended Euclidean Algorithm
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
