import csv
import os
from os import path
import random

def log_transactions(transactions):
    file_path = 'transactions.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['DateTime', 'Username', 'Old Balance', 'Transaction Amount', 'New Balance']
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(fieldnames)

        writer.writerows(transactions)

def create_pin():
    """
    Function creates a pin entered by user or randomly generated.
    """
    pin_tries = 0
    max_tries = 3
    while pin_tries < max_tries:
        pin_input = input('Select a number between 1 and 9999 as your pin: ')
        try:
            pin = int(pin_input)
            if 1 <= pin <= 9999:
                return pin
            else:
                print('Pin needs to be an integer between 1 and 9999.')
        except ValueError:
            print(f'Invalid pin. Attempt {pin_tries + 1} of {max_tries}.')
        pin_tries += 1

    print("The system will create a pin randomly for you.")
    pin = random.randint(1, 9999)
    print(f"Your new pin is: {pin}")
    return pin
