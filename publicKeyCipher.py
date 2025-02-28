import sys
import os
from cryptomath import CryptoMath

class PublicKeyCipher:
    def __init__(self, keyFilename=None):
        self.keyFilename = keyFilename

    def getBlocksFromBytes(self, data, blockSize):
        """
Divides binary data into blocks of a specified size.
Each block is treated as an integer.
:param data: binary data
:param blockSize: block size
:return: list of integers
        """
        blockInts = []
        for blockStart in range(0, len(data), blockSize):
            blockInt = 0
            for i in range(blockStart, min(blockStart + blockSize, len(data))):
                blockInt += data[i] * (256 ** (i % blockSize))
            blockInts.append(blockInt)
        return blockInts

    def getBytesFromBlocks(self, blockInts, messageLength, blockSize):
        """
Converts blocks of integers into binary data.
:param blockInts: blocks of integers
:param messageLength: length of the message
:param blockSize: block size
:return: binary data
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

    def encryptMessage(self, message, key, blockSize):
        """
Encrypts data using the public key.
:param message: message to encrypt
:param key: public key
:param blockSize: block size
:return: list of encrypted blocks
        """
        n, e = key
        return [pow(block, e, n) for block in self.getBlocksFromBytes(message, blockSize)]

    def decryptMessage(self, encryptedBlocks, messageLength, key, blockSize):
        """
Decrypts binary data using the private key.
:param encryptedBlocks: list of encrypted blocks
:param messageLength: length of the message
:param key: private key
:param blockSize: block size
:return: decrypted binary data
        """
        n, d = key
        decryptedBlocks = [pow(block, d, n) for block in encryptedBlocks]
        return self.getBytesFromBlocks(decryptedBlocks, messageLength, blockSize)

    def readKeyFile(self, keyFilename):
        """
Reads key file.
:param keyFilename: name of the key file
:return: key
        """
        with open(keyFilename, 'r') as fo:
            content = fo.read()
        try:
            keySize, n, EorD = map(int, content.split(','))
        except ValueError:
            sys.exit("ERROR: Wrong format of the key file!")
        return (keySize, n, EorD)

    def encryptAndWriteToFile(self, keyFilename, message, original_filename, blockSize=None):
        """
Encrypts data and writes it to a file.
:param keyFilename: name of the key file
:param message: message to encrypt
:param original_filename: original filename
:param blockSize: block size
:return: encrypted data
        """
        keySize, n, e = self.readKeyFile(keyFilename)
        if blockSize is None:
            blockSize = keySize // 8 - 1
        if blockSize >= keySize // 8:
            sys.exit("ERROR: Block size is too large for the key.")
        encryptedBlocks = self.encryptMessage(message, (n, e), blockSize)
        encryptedContent = f"{len(message)}_{blockSize}_{original_filename}_" + ",".join(map(str, encryptedBlocks))
        with open('encrypted.bin', 'wb') as fo:
            fo.write(encryptedContent.encode())

    def readFromFileAndDecrypt(self, messageFilename, keyFilename):
        """
Reads encrypted data from a file and decrypts it.
:param messageFilename: name of the file with encrypted data
:param keyFilename: name of the key file
:return: decrypted data
        """
        keySize, n, d = self.readKeyFile(keyFilename)
        with open(messageFilename, 'rb') as fo:
            content = fo.read().decode()
        try:
            parts = content.split('_')
            messageLength = int(parts[0])
            blockSize = int(parts[1])
            original_filename = parts[2]
            encryptedMessage = parts[3]
        except (ValueError, IndexError):
            sys.exit("ERROR: Damaged data!")
        if blockSize >= keySize // 8:
            sys.exit("ERROR: Block size is too large for the key.")
        encryptedBlocks = list(map(int, encryptedMessage.split(',')))
        decryptedData = self.decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)
        with open(original_filename, 'wb') as fo:
            fo.write(decryptedData)
        print(f'Decrypted data saved to: {original_filename}')