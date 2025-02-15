import sys, os, primeNum, cryptomath, menu


def main():
    menu.clear()

    name = input('Input key name:\n> ')
    print('Generating keys...')
    makeKeyFiles(name, 4096)
    print('Keys generated.')


def generateKey(keySize):
    """
    Generates public and private keys.
    :param keySize: size of the keys
    :return: private and public key
    """
    d = None

    while d is None:
        p = primeNum.generateLargePrime(keySize // 2)
        q = primeNum.generateLargePrime(keySize // 2)

        # Zapewniamy, że p i q nie są zbyt bliskie
        while abs(p - q) < 2**(keySize // 2 - 100):
            q = primeNum.generateLargePrime(keySize // 2)

        phi = (p - 1) * (q - 1)
        n = p * q

        e = 65537
        d = cryptomath.findModInverse(e, phi)

    publicKey = (n, e)
    privateKey = (n, d)

    return (publicKey, privateKey)


def makeKeyFiles(name, keySize=4096):
    """
    Saves keys to files
    :param name: filename
    :param keySize: size of the key
    """
    if os.path.exists(f"{name}.pub") or os.path.exists(f"{name}"):
        sys.exit(f'WARNING: File {name}.pub or {name} already exists! Use anote name or delete the files and run the program again.')

    publicKey, privateKey = generateKey(keySize)

    print(f'Saving public key to {name}.pub...')
    with open(f"{name}.pub", "w") as fo:
        fo.write(f"{keySize},{publicKey[0]},{publicKey[1]}")

    print(f'Saving private key to {name}...')
    with open(f"{name}", "w") as fo:
        fo.write(f"{keySize},{privateKey[0]},{privateKey[1]}")


if __name__ == '__main__':
    main()
