
from chrome_automation import automation as chrome_setup, test_selenium, edit_credentials
from djc_barmaker import setup as djc_setup

import os
import platform
#Verifying Integrity

def clear_screen():
    # Clear the command line screen.
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def main_menu():
    while True:
        clear_screen()
        print("\nMain Menu")
        print("1. Test Selenium")
        print("2. Edit Credentials")
        print("3. Download Files")
        print("4. Analyze Files")
        print("5. Exit")
        
        choice = input("Please enter your choice (1-5): ")

        if choice == '1':
            test_selenium()
            input("Press Enter to return to the main menu...")
        elif choice == '2':
            edit_credentials()
            input("Press Enter to return to the main menu...")
        elif choice == '3':
            download_files()
            input("Press Enter to return to the main menu...")
        elif choice == '4':
            djc_setup()
            input("Press Enter to return to the main menu...")
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 4.")


def download_files():
    while True:
        num = input("How many files do you want to download starting from the top? (Enter a number or 'all'): ")
        if num.isdigit() and 1 <= int(num):
            print(f"Downloading {num} files...")
            chrome_setup(num)
            break
        elif num.lower() == 'all':
            print("Downloading all files...")
            chrome_setup(num)
            break
        else:
            print("Invalid input. Please enter a number between 1 and 2000, or type 'all'.")


if __name__ == "__main__":
    main_menu()
