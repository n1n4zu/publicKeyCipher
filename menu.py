import os, platform

def mainMenu():
    print('''[1] Wygeneruj klucze
[2] Szyfruj/Deszyfruj wiadomość
[3] Wyjście''')

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')