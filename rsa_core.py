# rsa_core.py

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(e, phi):
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise Exception("Modular inverse does not exist")
    return x % phi


def generate_keys(p, q):
    if not is_prime(p) or not is_prime(q):
        raise ValueError("Both p and q must be prime numbers!")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while gcd(e, phi) != 1:
        e += 2

    d = mod_inverse(e, phi)

    return (n, e), (n, d), phi


def encrypt(text, public_key):
    n, e = public_key
    return [pow(ord(char), e, n) for char in text]


def decrypt(cipher, private_key):
    n, d = private_key
    return ''.join([chr(pow(char, d, n)) for char in cipher])


def factor_n(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i, n // i
    return None, None