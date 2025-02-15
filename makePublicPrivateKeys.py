import sys, os, primeNum, cryptomath, menu


def main():
    menu.clear()

    name = input('Podaj nazwę klucza:\n> ')
    print('Tworzenie kluczy...')
    makeKeyFiles(name, 4096)
    print('Wygenerowano klucze.')

def generateKey(keySize):
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
    if os.path.exists(f"{name}.pub") or os.path.exists(f"{name}"):
        sys.exit(f'UWAGA: Plik {name}.pub lub {name} już istnieje! Użyj innej nazwy lub usuń pliki i uruchom program ponownie.')

    publicKey, privateKey = generateKey(keySize)

    print(f'Zapisywanie klucza publicznego do pliku {name}.pub...')
    with open(f"{name}.pub", "w") as fo:
        fo.write(f"{keySize},{publicKey[0]},{publicKey[1]}")

    print(f'Zapisywanie klucza prywatnego do pliku {name}...')
    with open(f"{name}", "w") as fo:
        fo.write(f"{keySize},{privateKey[0]},{privateKey[1]}")


if __name__ == '__main__':
    main()
