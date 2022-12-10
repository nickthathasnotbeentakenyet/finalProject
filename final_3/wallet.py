import json
import os
from datetime import datetime
import matplotlib.pyplot as plt  
from numpy import negative
import numpy_financial as npf
from colorama import Fore

AMOUNT_INDEX = 0
DATE_INDEX = 1
F_NAME = 'budget.json'

def main():
    '''
    Purpose: a simple program to keep track of money flow
    Author: Arkadii Lantukh
    Parameters: None
    Return: None
    '''
    print(f'{Fore.MAGENTA}-'*40+'\n'+'#'*10 +f'{Fore.RED}    SMART WALLET    '+f'{Fore.MAGENTA}#'*10+'\n'+'-'*40)
    try:
        wallet_json = check_create(F_NAME)
    # it will create a file even if it's not found. But just in case 
    # something happens to user permissions and she is not able to create a file
    except FileNotFoundError as not_found_err:
        print(f'{Fore.RED}')
        print(type(not_found_err).__name__, not_found_err, sep=": ")
        print("Something went wrong...")
        print(f"Can't create {F_NAME} file.{Fore.RESET}")
    # in case the file exists, but can't be accessed
    except PermissionError as perm_err:
        print(f"{Fore.RED}Error: {perm_err}")
        print(f"You don't have permission to read {F_NAME}.{Fore.RESET}")

    # keep looping until user enters 0
    exiting = False
    while not exiting:
        command = input(f"{Fore.GREEN}\n\
MAIN MENU:\n\
1 - income\n\
2 - expenses\n\
3 - calculators\n\
0 - exit\n\
enter code#:  \
{Fore.RESET}")
        
        match command.split():
            # income section
            case ['1']: 
                # keep looping until user enters 0 to exit to the main menu
                while True:
                    income_command = input(f"\n{Fore.BLUE}INCOME MENU:\n1 - add\n2 - show\n0 - exit\nenter code#: {Fore.RESET}")
                    # add income
                    if income_command == '1':
                        income_source = input(f'{Fore.MAGENTA}Enter income source [paycheck, bonus]: ')
                        # keep looping until user enters a number
                        while True:
                            try:
                                amount = float(input(f'{Fore.MAGENTA}Enter amount for {income_source} [89.99]: '))
                                break
                            # wrong input caught here
                            except ValueError as val_err:
                                print(f"{Fore.RED}Error: {type(val_err).__name__}")
                                print(f"Please don't include characters other than numbers{Fore.RESET}")
                        income = add_flow(income_source, amount)
                        try:
                            write_json(wallet_json, income,"income")
                        # in case json file was removed during the program run
                        except FileNotFoundError as not_found_err:
                            print(f'{Fore.RED}')
                            print(type(not_found_err).__name__, not_found_err, sep=": ")
                            print(f"The file {F_NAME} doesn't exist.")
                            print(f"Please check file name or path to the file{Fore.RESET}")
                        # in case file can't be accessed after entering this submenu
                        except PermissionError as perm_err:
                            print(f"{Fore.RED}Error: {perm_err}")
                            print(f"You don't have permission to read {F_NAME}.{Fore.RESET}")
                    # show income information
                    elif income_command == '2':
                        try:
                            all_income = read_budget(wallet_json,'income')
                        # trying to catch at every step to narrow the area where an error can occur
                        except FileNotFoundError as not_found_err:
                            print(f'{Fore.RED}')
                            print(type(not_found_err).__name__, not_found_err, sep=": ")
                            print(f"The file {wallet_json} doesn't exist.")
                            print("Please check file name or path to the file{Fore.RESET}")
                        # again, making sure permissions are stil granted
                        except PermissionError as perm_err:
                            print(f"{Fore.RED}Error: {perm_err}")
                            print(f"You don't have permission to read {wallet_json}.{Fore.RESET}")

                        print_budget(all_income,'income')   
                    # exiting to the main menu
                    elif income_command == '0': break
                    # notify user of wrong input
                    else: print(f'{Fore.LIGHTRED_EX}Check your input{Fore.RESET}')
            # expenses section
            case ['2']:  
                while True:
                    expense_command = \
input(f"{Fore.BLUE}\nEXPENSES MENU:\n1 - add\n2 - show\n3 - stats\n0 - exit\nenter code#: {Fore.RESET}")
                    # add an expense
                    if expense_command == '1': 
                        # keep looping until user enters something 
                        while True:
                            expense_purpose = input(f'{Fore.MAGENTA}Enter expense purpose [food, gas]: ')
                            if expense_purpose != "": break
                            else: print(f"{Fore.RED}Can't be empty{Fore.RESET}")
                        # keep looping until users enters a number
                        while True:
                            try:
                                amount = float(input(f'{Fore.MAGENTA}Enter amount for {expense_purpose} [89.99]: '))
                                break
                            # catching wrong input
                            except ValueError as val_err:
                                print(f"{Fore.RED}Error: {type(val_err).__name__}")
                                print(f"Please don't include characters other than numbers{Fore.RESET}")
                        expense = add_flow(expense_purpose, amount)
                        try:
                            write_json(wallet_json, expense,"expenses")
                        # in case file was removed after the program run
                        except FileNotFoundError as not_found_err:
                            print(f'{Fore.RED}')
                            print(type(not_found_err).__name__, not_found_err, sep=": ")
                            print(f"The file {F_NAME} doesn't exist.")
                            print(f"Please check file name or path to the file{Fore.RESET}")
                        # in case user loses permissions on the file during the program run
                        except PermissionError as perm_err:
                            print(f"{Fore.RED}Error: {perm_err}")
                            print(f"You don't have permission to read {F_NAME}.{Fore.RESET}")
                    # show expenses information
                    elif expense_command == '2':
                        try:
                            all_expenses = read_budget(wallet_json,'expenses')
                        # still checking if file exists
                        except FileNotFoundError as not_found_err:
                            print(f'{Fore.RED}')
                            print(type(not_found_err).__name__, not_found_err, sep=": ")
                            print(f"The file {F_NAME} doesn't exist.")
                            print(f"Please check file name or path to the file{Fore.RESET}")
                        # still checking if user has permissions to open it
                        except PermissionError as perm_err:
                            print(f"{Fore.RED}Error: {perm_err}")
                            print(f"You don't have permission to read {F_NAME}.{Fore.RESET}")
                            
                        print_budget(all_expenses, 'expenses')
                    # show statistics
                    elif expense_command == '3':
                        try:
                            expenses = read_budget(wallet_json,'expenses')
                        # is the file still there?
                        except FileNotFoundError as not_found_err:
                            print(f'{Fore.RED}')
                            print(type(not_found_err).__name__, not_found_err, sep=": ")
                            print(f"The file {F_NAME} doesn't exist.")
                            print(f"Please check file name or path to the file{Fore.RESET}")
                        # does the user still have correct rights to view the file?
                        except PermissionError as perm_err:
                            print(f"{Fore.RED}Error: {perm_err}")
                            print(f"You don't have permission to read {F_NAME}.{Fore.RESET}")
                        # looping to make sure user enters a digit value
                        while True:
                            try:
                                period = int(input(f'{Fore.MAGENTA}Enter period [7, 30, 365]: {Fore.RESET}'))
                                purposes, amounts = print_expenses_period(expenses, period)
                                break
                            # in case user enters something weird
                            except ValueError as val_err:
                                print(f"{Fore.RED}Error: {type(val_err).__name__}")
                                print(f"Period must be integer!{Fore.RESET}")                      
                        # if there is information to be shown - create plot; else - show message
                        try: 
                            create_plot(amounts, purposes)
                        except: print(f'{Fore.LIGHTRED_EX}oops...not enough data{Fore.RESET}')
                    # exit to the maon menu
                    elif expense_command == '0': break
                    # notify user of wrong input
                    else: print(f'{Fore.LIGHTRED_EX}Check input{Fore.RESET}')
            # calculators section
            case ['3']:     
                # made it easier this time. I know this is not the best way to catch errors  
                while True:
                    try:
                        calculator_command = input(f"{Fore.BLUE}\nCALCULATORS MENU:\n1 - financial security\n2 - initial payment\
                            \n3 - credit\n4 - debit\n0 - exit\nenter code#: {Fore.RESET}")
                        if calculator_command == '1':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            years = float(input("Enter period in years: "))
                            desired_amount = float(input("Enter desired amount [500000]: "))
                            result = npf.pmt(rate=rate/12, nper=years*12, pv=0, fv=desired_amount)
                            print("="*30,f"\nPeriod: {years} years\nRate: {rate} %\nDesired Amount: ${desired_amount}")
                            print("-"*30,f"\nMonthly payment: ${negative(result):.2f}\n","="*30)
                        elif calculator_command == '2':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            years = float(input("Enter period in months [3 yars = 36, 5 years = 60]: ")) / 12
                            annual_payment = float(input("Enter annual payment [0 for no payments]: "))
                            desired_amount = float(input("Enter desired amount [100000]: "))
                            result = npf.pv(rate=rate, nper=years, pmt=negative(annual_payment), fv=desired_amount)
                            print("="*30,f"\nYears: {years}\nRate: {rate} %\nAnnual Payment: {annual_payment} ₽\nDesired Amount: ${desired_amount}")
                            print("-"*30,f"\nInitial Payment: ${negative(result):.2f}\n","="*30)
                        elif calculator_command == '3':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            months = float(input("Enter period in months [3 years = 36, 5 years = 60]: "))
                            current_debt = float(input("Enter current debt amount [68000]: "))
                            result = npf.pmt(rate=rate/12, nper=months, pv=current_debt, fv=0)
                            print("="*30,f"\nPeriod: {months} months\nRate: {rate} %\nCurrent Debt: ${current_debt}")
                            print("-"*30,f"\nMonthly Payment: ${negative(result):.2f}\n","="*30)
                        elif calculator_command == '4':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            years = float(input("Enter period in months [3 years = 36, 5 years = 60]: ")) / 12
                            anual_payment = float(input("Enter anual payment [0 if no payments]: "))
                            one_time_payment = float(input("Enter one-time payment [10000]: "))
                            result = npf.fv(rate=rate, nper=years, pmt=negative(anual_payment), pv=negative(one_time_payment))
                            print("="*30,f"\nYears: {years}\nRate: {rate} %\nAnual Payment: ${anual_payment}\nOne-time Payment: ${one_time_payment}")
                            print("-"*30,f"\nAccumulation: ${result:.2f}\n","="*30)
                        elif calculator_command == '0': break
                        else: 
                            print(f'{Fore.LIGHTRED_EX}entered wrong number?{Fore.RESET}')
                    # in case user enters not a number. Yeah, this should have been a value error exception, but I'm breaking the rules here.
                    except:
                        print(f"{Fore.RED}Error. Check input values.{Fore.RESET}")
            # exit
            case ['0']:
                print("Good bye...")
                exiting = True
            # wrong user input
            case _:
                print(f"\n{Fore.LIGHTRED_EX}Unknown command {command!r}{Fore.RESET}")


def check_create(f_name):
    '''
    Purpose: check if the file exists, if not - create it for future needs
    Parameters: None
    Return: path to the file
    '''
    cwd = os.getcwd()
    filename = cwd + '\\' + f_name
    if not os.path.exists(f_name):
        data = '{"income": [],"expenses":[]}'
        with open(filename, "w") as file:
            file.write(data)
        file.close()
    return filename


def add_flow(source_purpose, amount):
    '''
    Purpose: make a dictionary, where either income source or
            expense purpose represents the key and amount of 
            money represents the value along with the datetime
    Parameters: 
            source_purpose = string value 
            amount = float number
    Return: dictionary
    '''
    date_stamp = str(datetime.now())
    return {source_purpose:[amount,date_stamp]}


def write_json(file, money_flow, section):
    '''
    Purpose: write to a file and notify user
    Parameters: 
            file = path to json file
            money_flow = dictionary containing data
            section = string value to place dictionary to apropriate section in json file
    Return: none
    '''
    with open(file,'r+', encoding='utf-8') as f:
        file_data = json.load(f)
        file_data[section].append(money_flow)
        f.seek(0)
        json.dump(file_data, f, indent = 4, ensure_ascii=False)
        print(f"{Fore.LIGHTMAGENTA_EX}Entered!{Fore.RESET}")


def read_budget(file,section):
    '''
    Purpose: read only specific section from json file
    Parameters: 
            file = path to json file
            section = a part of json file (income, expenses)
    Return: compound list with apropriate data
    '''
    with open(file,'r', encoding='utf-8') as f:
        data = json.load(f)
        return data[section]


def print_budget(budget,section):
    '''
    Purpose: read through the given compound list, make calculations and print the results
    Parameters:
            budget = compound list
            section = string value (income, expenses)
    Return: none
    '''
    sum = 0
    print(f'{Fore.YELLOW}')
    for _ in budget:
        for key, value in _.items():
            try:
                sum += float(value[AMOUNT_INDEX])
            # in case someone has changed the file
            # which resulted in wrong values
            except ValueError as val_err:
                print(f"{Fore.RED}Error: {type(val_err).__name__}")
                print(f"{value[AMOUNT_INDEX]} is not a number. \nWARNING: Someone had manually changed the file{Fore.RESET}")

            print(f'{key:<30}: ${value[AMOUNT_INDEX]}')
    print(f'\nTotal sum of {section}: ${sum:.2f}{Fore.RESET}')


def print_expenses_period(expenses,period):
    '''
    Purpose: read through the compound list, calculate and print 
            apropriate information based on given period, return 2 lists
    Parameters: 
            expenses = a compound list, the 'expenses' section of json file
            period = integer value for period in days
    Return: two lists containing information about expense purposes and corresponding amounts
    '''
    total = 0
    purposes = []
    amounts = []
    try:
        for _ in expenses:
            for key, value in _.items():
                exp_date = value[DATE_INDEX]
                exp_amount = value[AMOUNT_INDEX]
                format = "%Y-%m-%d %H:%M:%S.%f"
                exp_date = datetime.strptime(exp_date, format).date()
                today = datetime.now().date()
                fact_period = (today - exp_date).days
                if fact_period <= period:
                    purposes.append(key)
                    amounts.append(exp_amount)
                    total += exp_amount
                    print(f'{Fore.YELLOW}{exp_date} you spent {exp_amount} for {key}')
    # making sure the file was not modified (incorrectly) manually
    except:
        print(f"{Fore.RED}Something went wrong..Looks like someone had manually change the file{Fore.RESET}")
    print(f'Total amount of expenses for {period} days: {total}{Fore.RESET}')
    return purposes,amounts


def create_plot(sums, purposes):
    '''
    Purpose: create a plot to visualize information based on given data 
    Parameters: 
            sums = list of amounts (expenses)
            purposes = lists of purposes (expenses)
    Return: none
    '''
    expl = []
    expensive = max(sums)
    for _ in range(len(sums)): 
        if sums[_] == expensive: expl.append(0.1)
        else: expl.append(0)
    plt.pie(sums, labels = purposes,explode=expl)
    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(12,6)
    fig.canvas.manager.set_window_title('Expenses')
    plt.show() 
    plt.savefig('expenses.png')


# call to main function
if __name__ == '__main__':
    main()
 