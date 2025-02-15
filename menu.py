import os

def mainMenu():
    print('''[1] Wygeneruj klucze
[2] Szyfruj/Deszyfruj wiadomość
[3] Wyjście''')

def clear():
    os.system('cls' if os.name == 'windows' else 'clear')