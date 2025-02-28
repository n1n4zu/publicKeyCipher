import sys
import os
from primeNum import PrimeNum
from cryptomath import CryptoMath

class KeyGenerator:
    def __init__(self, keySize=4096):
        self.keySize = keySize

    def generateKey(self):
        """
Generates public and private keys.
:return: private and public key
        """
        d = None
        while d is None:
            p = PrimeNum.generateLargePrime(self.keySize // 2)
            q = PrimeNum.generateLargePrime(self.keySize // 2)
            while abs(p - q) < 2 ** (self.keySize // 2 - 100):
                q = PrimeNum.generateLargePrime(self.keySize // 2)
            phi = (p - 1) * (q - 1)
            n = p * q
            e = 65537
            d = CryptoMath.findModInverse(e, phi)
        publicKey = (n, e)
        privateKey = (n, d)
        return publicKey, privateKey

    def makeKeyFiles(self, name):
        """
Saves keys to files
:param name: filename
        """
        if os.path.exists(f"{name}.pub") or os.path.exists(f"{name}"):
            sys.exit(f'WARNING: File {name}.pub or {name} already exists! Use another name or delete the files and run the program again.')
        publicKey, privateKey = self.generateKey()
        print(f'Saving public key to {name}.pub...')
        with open(f"{name}.pub", "w") as fo:
            fo.write(f"{self.keySize},{publicKey[0]},{publicKey[1]}")
        print(f'Saving private key to {name}...')
        with open(f"{name}", "w") as fo:
            fo.write(f"{self.keySize},{privateKey[0]},{privateKey[1]}")