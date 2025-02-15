import sys, os, menu


def main():
    menu.clear()
    filename = input('Podaj nazwę pliku:\n> ')

    if not os.path.exists(filename):
        sys.exit("Błąd: Plik nie istnieje!")

    mode = input("Wybierz tryb (encrypt/decrypt):\n> ").lower()

    if mode == 'encrypt':
        pubKeyFilename = input('Podaj nazwę pliku z kluczem publicznym:\n> ')
        if not os.path.exists(pubKeyFilename):
            sys.exit("Błąd: Plik z kluczem publicznym nie istnieje!")

        with open(filename, 'rb') as fo:
            message = fo.read()
        print(f'Szyfrowanie i zapisywanie do encrypted.bin...')
        encryptAndWriteToFile(pubKeyFilename, message, filename)

    elif mode == 'decrypt':
        privKeyFilename = input('Podaj nazwę pliku z kluczem prywatnym:\n> ')
        if not os.path.exists(privKeyFilename):
            sys.exit("Błąd: Plik z kluczem prywatnym nie istnieje!")

        print(f'Czytanie pliku {filename} i odszyfrowywanie...')
        decryptedData, original_filename = readFromFileAndDecrypt(filename, privKeyFilename)

        # Zapisz odszyfrowane dane z oryginalną nazwą pliku
        with open(original_filename, 'wb') as fo:
            fo.write(decryptedData)
        print(f'Odszyfrowane dane zapisano w pliku: {original_filename}')

    else:
        sys.exit("Błąd: Nieznany tryb. Wybierz 'encrypt' lub 'decrypt'.")

def getBlocksFromBytes(data, blockSize):
    """
    Dzieli dane binarne na bloki o określonym rozmiarze.
    Każdy blok jest traktowany jako liczba całkowita.
    """
    blockInts = []
    for blockStart in range(0, len(data), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(data))):
            blockInt += data[i] * (256 ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts

def getBytesFromBlocks(blockInts, messageLength, blockSize):
    """
    Konwertuje bloki liczb całkowitych z powrotem na dane binarne.
    """
    message = bytearray()
    for blockInt in blockInts:
        blockMessage = bytearray()
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                byte = blockInt // (256 ** i)
                blockInt = blockInt % (256 ** i)
                blockMessage.insert(0, byte)
        message.extend(blockMessage)
    return bytes(message)

def encryptMessage(message, key, blockSize):
    """
    Szyfruje dane binarne za pomocą klucza publicznego.
    """
    n, e = key
    return [pow(block, e, n) for block in getBlocksFromBytes(message, blockSize)]

def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    """
    Deszyfruje dane binarne za pomocą klucza prywatnego.
    """
    n, d = key
    decryptedBlocks = [pow(block, d, n) for block in encryptedBlocks]
    return getBytesFromBlocks(decryptedBlocks, messageLength, blockSize)

def readKeyFile(keyFilename):
    """
    Odczytuje klucz z pliku.
    """
    with open(keyFilename, 'r') as fo:
        content = fo.read()

    try:
        keySize, n, EorD = map(int, content.split(','))
    except ValueError:
        sys.exit("Błąd: Nieprawidłowy format pliku klucza!")

    return (keySize, n, EorD)

def encryptAndWriteToFile(keyFilename, message, original_filename, blockSize=None):
    """
    Szyfruje dane i zapisuje je do pliku.
    """
    keySize, n, e = readKeyFile(keyFilename)
    if blockSize is None:
        blockSize = keySize // 8 - 1

    if blockSize >= keySize // 8:
        sys.exit("ERROR: Rozmiar bloku jest zbyt duży dla klucza.")

    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    # Dodaj oryginalną nazwę pliku do zaszyfrowanych danych
    encryptedContent = f"{len(message)}_{blockSize}_{original_filename}_" + ",".join(map(str, encryptedBlocks))

    with open('encrypted.bin', 'wb') as fo:
        fo.write(encryptedContent.encode())

    return encryptedContent

def readFromFileAndDecrypt(messageFilename, keyFilename):
    """
    Odczytuje zaszyfrowane dane z pliku i deszyfruje je.
    """
    keySize, n, d = readKeyFile(keyFilename)

    with open(messageFilename, 'rb') as fo:
        content = fo.read().decode()

    try:
        # Odczytaj długość wiadomości, rozmiar bloku i oryginalną nazwę pliku
        parts = content.split('_')
        messageLength = int(parts[0])
        blockSize = int(parts[1])
        original_filename = parts[2]
        encryptedMessage = parts[3]
    except (ValueError, IndexError):
        sys.exit("Błąd: Uszkodzony plik szyfrogramu!")

    if blockSize >= keySize // 8:
        sys.exit("ERROR: Rozmiar bloku jest zbyt duży dla klucza.")

    encryptedBlocks = list(map(int, encryptedMessage.split(',')))

    decryptedData = decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)
    return decryptedData, original_filename
