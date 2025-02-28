import os
import platform

class Menu:
    @staticmethod
    def mainMenu():
        """
Displays the main menu
        """
        print('''[1] Generate keys
[2] Encrypt/Decrypt message
[3] Exit''')

    @staticmethod
    def clear():
        """
Clears the console
        """
        os.system('cls' if platform.system() == 'Windows' else 'clear')