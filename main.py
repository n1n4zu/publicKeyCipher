import menu, makePublicPrivateKeys, publicKeyCipher, sys

"""
Author: n1n4zu
Copyright (C) 2025 n1n4zu
License: MIT license
Version: 1.0

This program encrypts and decrypts data using public and private keys and
generates them.
"""

while True:
    menu.clear()
    menu.mainMenu()
    option = input('Choose option:\n> ')

    match option:
        case '1':
            makePublicPrivateKeys.main()
            input('Press Enter to continue...')
        case '2':
            publicKeyCipher.main()
            input('Press Enter to continue...')
        case '3':
            sys.exit()