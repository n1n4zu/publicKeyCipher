from menu import Menu
from makePublicPrivateKeys import KeyGenerator
from publicKeyCipher import PublicKeyCipher
import sys

class MainApp:
    def __init__(self):
        self.menu = Menu()
        self.keyGenerator = KeyGenerator()
        self.publicKeyCipher = PublicKeyCipher()

    def run(self):
        while True:
            self.menu.clear()
            self.menu.mainMenu()
            option = input('Choose option:\n> ')

            if option == '1':
                name = input('Input key name:\n> ')
                print('Generating keys...')
                self.keyGenerator.makeKeyFiles(name)
                input('Press Enter to continue...')
            elif option == '2':
                filename = input('Input file name:\n> ')
                mode = input("Choose mode (encrypt/decrypt):\n> ").lower()
                if mode == 'encrypt':
                    pubKeyFilename = input('Input public key filename:\n> ')
                    with open(filename, 'rb') as fo:
                        message = fo.read()
                    print(f'Encrypting and saving to encrypted.bin...')
                    self.publicKeyCipher.encryptAndWriteToFile(pubKeyFilename, message, filename)
                elif mode == 'decrypt':
                    privKeyFilename = input('Input private key filename:\n> ')
                    print(f'Reading {filename} and decrypting...')
                    self.publicKeyCipher.readFromFileAndDecrypt(filename, privKeyFilename)
                else:
                    print("ERROR: Unknown mode. Choose 'encrypt' or 'decrypt'.")
                input('Press Enter to continue...')
            elif option == '3':
                sys.exit()

if __name__ == "__main__":
    app = MainApp()
    app.run()