import menu, makePublicPrivateKeys, publicKeyCipher, sys

while True:
    menu.clear()
    menu.mainMenu()
    option = input('Wybierz opcje:\n> ')

    match option:
        case '1':
            makePublicPrivateKeys.main()
            input('Naciśnij Enter, aby kontynuować...')
        case '2':
            publicKeyCipher.main()
            input('Naciśnij Enter, aby kontynuować...')
        case '3':
            sys.exit()