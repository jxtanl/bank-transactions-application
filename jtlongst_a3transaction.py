# Jessica Longstreth, CIS 345 T/Th 12:00 -1:15 PM, PE5
import os
import json
import random
import time
from jtlongst_logger import log_transactions, create_pin

logger = {}

print("Welcome to Cactus Bank !")
print("***********************************")
print("* Enter 1 to add a new customer   *")
print("* Enter 2 to delete a customer    *")
print("* Enter 3 to make transactions    *")
print("* Enter 4 to exit                 *")
print("***********************************")

while True:
    try:
        selection = input('Make your selection: ')
        if selection not in ['1', '2', '3', '4']:
            raise ValueError('Invalid number entered. Try again ...')
        break
    except ValueError as e:
        print(e)

with open('customers.json') as file_handle:
    accounts = json.load(file_handle)

if selection == '1':
    username = input('Please enter a username: ')
    if username in accounts:
        print('ERROR: Username already exists. Please choose another one')
    else:
        pin_choice = input('Enter 1 to create a pin yourself or 2 and the system will create a pin for you: ')
        if pin_choice == '1':
            print('You have 3 tries to enter a number between 1 and 9999 as your pin')
            print("If you didn't reset your print after 3 tries, the system will create a pin for you")
            pin = create_pin()
        elif pin_choice == '2':
            pin = random.randint(1, 9999)
            print(f"Your new pin is: {pin}")
        name = input('Please enter your name: ')
        try:
            checking_amount = float(input('Enter the amount you will deposit to the checking account: '))
            if checking_amount < 0:
                raise ValueError
        except ValueError:
            checking_amount = 0.0
            print('Invalid number entered. The current balance will be 0.0')
        try:
            savings_amount = float(input('Enter the amount you will deposit to the saving account: '))
            if savings_amount < 0:
                raise ValueError
        except ValueError:
            savings_amount = 0.0
            print('Invalid number entered. The current balance will be 0.0')
        accounts[username] = {'Pin': pin, 'Name': name, 'C': checking_amount, 'S': savings_amount}
        print("Your account has been created")
        print('Please visit the system again to make transaction')
        print('Press Enter to continue...')
elif selection == '2':
    username = input('Please enter your username: ')
    if username not in accounts:
        print('ERROR: Username is not in the system.')
    else:
        del accounts[username]
        print(f'Account for {username} has been deleted.')
elif selection == '3':
    username = input('Please enter your username: ')
    if username not in accounts:
        print('ERROR: Username is not in the system.')
    else:
        tries = 1
        max_tries = 3
        while tries <= 3:
            print('Cactus Bank - Making Transactions\n')
            pin_input = input('Enter pin or x to exit application: ').casefold()
            if pin_input == 'x':
                exit()
            elif int(pin_input) != accounts[username]['Pin']:
                os.system('clear')
                print(f'Invalid pin. Attempt {tries} of {max_tries}. Please try again.')
                tries += 1
                if tries > 3:
                    ask_user = input('Do you want to get a new pin (y/n): ')
                    if ask_user.lower() == 'y':
                        pin_choice = input('Enter 1 to create a pin yourself or 2 and the system will create a pin for you: ')
                        if pin_choice == '1':
                            print('You have 3 tries to enter a number between 1 and 9999 as your pin')
                            print("If you didn't reset your print after 3 tries, the system will create a pin for you")
                            accounts[username]['Pin'] = create_pin()
                        elif pin_choice == '2':
                            pin = random.randint(1, 9999)
                            print(f"Your new pin is: {pin}")
                            accounts[username]['Pin'] = pin
                            print('Please visit the system again to make transactions')
                            print('Press enter to continue .......')
                            with open('customers.json', 'w') as fp:
                                json.dump(accounts, fp, indent=4)
                    else:
                        break
            else:
                break

        if tries <= max_tries:
            for t in range(1, 5):
                print(f"Welcome {accounts[username]['Name']}")
                print(f'{"Select Account": ^20}')

                while True:
                    try:
                        selection = input('Enter C or S for (C)hecking or (S)avings: ').upper()
                        if selection != 'C' and selection != 'S':
                            raise ValueError('Incorrect selection. You must enter C or S.')
                    except ValueError as ex:
                        print(ex)
                    else:
                        os.system('clear')
                        print(f'Opening {selection} Account...\n')
                        break
                old_balance = accounts[username][selection]
                print('Transaction instructions:')
                print(' - Withdrawal enter a negative dollar amount: -20.00.')
                print(' - Deposit enter a positive dollar amount: 10.50')
                print(f'\nBalance: ${accounts[username][selection]: ,.2f}')
                amount = 0.00
                try:
                    amount = float(input(f'Enter transaction amount: '))
                except (ValueError, TypeError) as ex:
                    print('Invalid number entered. Number entered needs to be an integer or float number.')
                if (amount + old_balance) >= 0:
                    new_balance = round(old_balance + amount, 2)
                    accounts[username][selection] = new_balance
                    transaction = [time.ctime(), username, f"${old_balance:,.2f}", f"${amount:,.2f}", f"${new_balance:,.2f}"]
                    log_transactions([transaction])
                    print(f'Transaction complete. New balance is ${accounts[username][selection]: ,.2f}')
                else:
                    print('Insufficient Funds. Transaction Cancelled.')

                ans = input('Press n to make another transaction or x to exit application: ').casefold()
                if ans[0] == 'x':
                    break
elif selection == '4':
    exit()

print('\n\nSaving data...\n')
with open('customers.json', 'w') as fp:
    json.dump(accounts, fp, indent=4)
print('Data Saved.\nExiting...')

for username, details in accounts.items():
    name = details.get('Name', 'N/A')
    pin = details.get('Pin', 'N/A')
    try:
        checking_balance = float(details.get('C', 0.0))
        savings_balance = float(details.get('S', 0.0))
    except ValueError:
        checking_balance = 0.0
        savings_balance = 0.0
    print("{:<10} {:<20} {:<20} {:<20.2f} {:<20.2f}".format(username, pin, name, checking_balance, savings_balance))



