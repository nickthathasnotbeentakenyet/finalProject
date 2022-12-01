import json
import os
from datetime import datetime
import matplotlib.pyplot as plt  
from numpy import negative
import numpy_financial as npf
from colorama import Fore

AMOUNT_INDEX = 0
DATE_INDEX = 1

def main():
    print(f'{Fore.MAGENTA}-'*40+'\n'+'#'*10 +f'{Fore.RED}    SMART WALLET    '+f'{Fore.MAGENTA}#'*10+'\n'+'-'*40)
    wallet_json = check_create()
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
            case ['1']: 
                while True:
                    income_command = input(f"\n{Fore.BLUE}INCOME MENU:\n1 - add\n2 - show\n0 - exit\nenter code#: {Fore.RESET}")
                    if income_command == '1':
                        income = add_flow('Enter income source [paycheck, bonus]: ')
                        write_json(wallet_json, income,"income")
                    elif income_command == '2':
                        all_income = read_budget(wallet_json,'income')
                        print_budget(all_income,'income')   
                    elif income_command == '0': break
                    else: print(f'{Fore.LIGHTRED_EX}entered wrong number?{Fore.RESET}')
            case ['2']:  
                while True:
                    expense_command = \
input(f"{Fore.BLUE}\nEXPENSES MENU:\n1 - add\n2 - show\n3 - stats\n0 - exit\nenter code#: {Fore.RESET}")
                    if expense_command == '1': 
                        expense = add_flow('Enter expense purpose [food, gas]: ')
                        write_json(wallet_json, expense,"expenses")
                    elif expense_command == '2':
                        all_expenses = read_budget(wallet_json,'expenses')
                        print_budget(all_expenses, 'expenses')
                    elif expense_command == '3':
                        expenses = read_budget(wallet_json,'expenses')
                        period = int(input(f'Enter period [7, 30, 365]: '))
                        purposes, amounts = print_expenses_period(expenses, period)
                        try: 
                            create_plot(amounts, purposes)
                        except: print(f'{Fore.LIGHTRED_EX}oops...not enough data{Fore.RESET}')
                    elif expense_command == '0': break
                    else: print(f'{Fore.LIGHTRED_EX}entered wrong number?{Fore.RESET}')
            case ['3']:          
                while True:
                    try:
                        calculator_command = input(f"{Fore.BLUE}\nCALCULATORS MENU:\n1 - financial security\n2 - initial payment\
                            \n3 - credit\n4 - debit\n0 - exit\nenter code#: {Fore.RESET}")
                        if calculator_command == '1':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            years = float(input("Enter period in years: "))
                            desired_amount = float(input("Enter desired amount [500000]: "))
                            result = npf.pmt(rate=rate/12, nper=years*12, pv=0, fv=desired_amount)
                            print("="*30,f"Period: {years} years\nRate: {rate} %\nDesired Amount: ${desired_amount}")
                            print("-"*30,f"Monthly payment: ${negative(result):.2f}","="*30)
                        elif calculator_command == '2':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            years = float(input("Enter period in months [3 yars = 36, 5 years = 60]: ")) / 12
                            annual_payment = float(input("Enter annual payment [0 for no payments]: "))
                            desired_amount = float(input("Enter desired amount [100000]: "))
                            result = npf.pv(rate=rate, nper=years, pmt=negative(annual_payment), fv=desired_amount)
                            print("="*30,f"Years: {years}\nRate: {rate} %\nAnnual Payment: {annual_payment} ₽\nDesired Amount: ${desired_amount}")
                            print("-"*30,f"Initial Payment: ${negative(result):.2f}","="*30)
                        elif calculator_command == '3':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            months = float(input("Enter period in months [3 years = 36, 5 years = 60]: "))
                            current_debt = float(input("Enter current debt amount [68000]: "))
                            result = npf.pmt(rate=rate/12, nper=months, pv=current_debt, fv=0)
                            print("="*30,f"Period: {months} months\nRate: {rate} %\nCurrent Debt: ${current_debt}")
                            print("-"*30,f"Monthly Payment: ${negative(result):.2f}","="*30)
                        elif calculator_command == '4':
                            rate = float(input("\nEnter interest rate [0.06]: "))
                            years = float(input("Enter period in months [3 years = 36, 5 years = 60]: ")) / 12
                            anual_payment = float(input("Enter anual payment [0 if no payments]: "))
                            one_time_payment = float(input("Enter one-time payment [10000]: "))
                            result = npf.fv(rate=rate, nper=years, pmt=negative(anual_payment), pv=negative(one_time_payment))
                            print("="*30,f"Years: {years}\nRate: {rate} %\nAnual Payment: ${anual_payment}\nOne-time Payment: ${one_time_payment}")
                            print("-"*30,f"Accumulation: ${result:.2f}","="*30)
                        elif calculator_command == '0': break
                        else: 
                            print(f'{Fore.LIGHTRED_EX}entered wrong number?{Fore.RESET}')
                    except:
                        print(f"{Fore.RED}Error. Сheck input values.{Fore.RESET}")
            case ['0']:
                print("Good bye...")
                exiting = True
            case _:
                print(f"\n{Fore.LIGHTRED_EX}Unknown command {command!r}{Fore.RESET}")

def check_create():
    cwd = os.getcwd()
    filename = cwd + '\\' + 'budget.json'
    if not os.path.exists('budget.json'):
        data = '{"income": [],"expenses":[]}'
        with open(filename, "w") as file:
            file.write(data)
        file.close()
    return filename


def add_flow(message):
    source_purpose = input(f'{Fore.MAGENTA}{message}')
    if source_purpose:
        amount = float(input(f'Enter amount for {source_purpose} [89.99]: '))
        date_stamp = str(datetime.now())
    flow = {source_purpose:[amount,date_stamp]}
    return flow


def write_json(file, money_flow, section):
    with open(file,'r+', encoding='utf-8') as f:
        file_data = json.load(f)
        file_data[section].append(money_flow)
        f.seek(0)
        json.dump(file_data, f, indent = 4, ensure_ascii=False)
        print(f"{Fore.LIGHTMAGENTA_EX}Entered!{Fore.RESET}")


def read_budget(file,section):
    with open(file,'r', encoding='utf-8') as f:
        data = json.load(f)
        return data[section]


def print_budget(budget,section):
        sum = 0
        print(f'{Fore.YELLOW}')
        for _ in budget:
            for key, value in _.items():
                sum += float(value[AMOUNT_INDEX])
                print(f'{key:<30}: ${value[AMOUNT_INDEX]}')
        print(f'\nTotal sum {section}: ${sum}{Fore.RESET}')


def print_expenses_period(expenses,period):
    total = 0
    purposes = []
    amounts = []
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
                print(f'{exp_date} you spent {exp_amount} for {key}')
    print(f'Total amount of expenses for {period} days: {total}')
    return purposes,amounts

def create_plot(sums, purposes):
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

if __name__ == '__main__':
    main()



    # TODO:
    '''
    exceptions
    test functions
    documentation
    '''