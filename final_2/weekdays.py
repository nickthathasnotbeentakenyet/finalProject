import datetime
import matplotlib.pyplot as plt
from colorama import Fore
from pyfiglet import Figlet


def main():

    '''
    Author: Arkadii Lantukh
    Purpose: refer to the print statement on line 18
    Parameters: None
    Return: None
    '''
    
    # welcome message
    print(f'{Fore.CYAN}')
    figlet = Figlet(font='Slant', width=150)
    print(figlet.renderText('WEEKDAY  FINDER'))
    decorator()
    print(f"{Fore.MAGENTA}Have you ever wondered what Weekday it was on a specific date?\n\
In some cultures, one who was born on Monday is called a 'Monday's child'\n\
Do you know the Weekday of the day you were born?\n\n\
This program will find:\n\
◦ the weekday for a specific date\n\
◦ the weekdays for that date for every year within specified range of years before the date\n\
◦ create a table of weekdays with lists of corresponding years\n\
◦ create a plot to visualize how weekdays are distributed for the date within the specified range\n{Fore.RESET}")

    # getting and validating user input
    decorator()
    user_date = validate_date()
    period = validate_period()

    # splitting user date into a list
    spl = get_date_splitted(user_date)

    YEAR = int(spl[0])
    MONTH = int(spl[1])
    DAY = int(spl[2])

    # weekday number of user date
    wkd_num = get_weekday_num(YEAR, MONTH, DAY)

    # weekday of user date
    wkd_name = get_weekday_name(wkd_num)
    decorator()
    print(f'{Fore.BLUE}{user_date} : {wkd_name}{Fore.RESET}')
    print()

    # keep records (year, weekday) for specified period
    dict = get_period_years(YEAR,MONTH,DAY,period)

    # output table of years and corresponding weekday names
    print_year_weekday_pairs(dict, period,user_date)
    print()

    # create and output table of weekday names and matching years
    table = get_table(dict)
    print_weekdays_table(table)
    print()
    decorator()
    decorator()
    
    # plot
    create_plot(table, user_date, period)

def decorator():
    '''
    Print a bunch of "=" characters to separate parts of the program
    Parameters: None
    Return: None
    '''
    print(f'{Fore.MAGENTA}='*60)

def validate_date():
    '''
    Get user input, validate if it matches specified format.
    If user enters incorrect values or input format doesn't match - exception is handled
    Keeps looping until user provides correct input value
    Parameters: None
    Return: user_date string
    '''
    exiting = 0
    while exiting != 1:
        try:
            user_date = input(f'{Fore.CYAN}Enter date {Fore.YELLOW}[YYYY-MM-DD]{Fore.RESET} : ')
            datetime.datetime.strptime(user_date,"%Y-%m-%d")
            if user_date == '2022-12-25': e_egg()
            exiting = 1
        except ValueError: 
            print(f'{Fore.RED}Error: incorrect input{Fore.RESET}')
    return user_date

def validate_period():
    '''
    Get user input for period of years. Validate input to only accept integer values.
    If incorrect value is entered - exception is handled
    Keeps asking until user enters valid number
    Parameters: None
    Return: period as an integer value
    '''
    exiting = 0
    while exiting != 1:
        try:
            period = int(input(f'{Fore.CYAN}Enter period of years{Fore.YELLOW} [10]{Fore.RESET} : '))
            exiting = 1
        except ValueError:
            print(f'{Fore.RED}Error: incorrect input. Must be integer{Fore.RESET}')
    return period

def get_date_splitted(date_string):
    '''
    Split a date string on dashes into a list of strings
    Parameters: date_string String
    Return: date_string List 
    '''
    return date_string.split('-')

def get_weekday_num(y,m,d):
    '''
    Finds a weekday number for a specific date
    Parameters: 
            y = year
            m = month
            d = day
    Return: weekday number
    '''
    return datetime.date(y,m,d).weekday()

def get_weekday_name(day_number):
    '''
    Find a weekday name based on weekday number
    Parameters: day_number
    Return: day_name
    '''

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    return day_names[day_number]

def get_period_years(y,m,d,period):
    '''
    Creates a dictionary for a specified period of years,
    where each key is a year and corresponding value is a weekday
    Dictionary starts at the 'oldest' year of specified period
    and ends at the closest year to the date specified by user
    Exceptions: 
            ValueError: is handled if user specifies period of years, 
                        where year can be 0. 
                        For example:
                            date: 1985-01-01
                            period: 1985 will throw an error message. 
                            The lowest year in this case should be 1984.
    Parameters:
            y = year
            m = month
            d = day
            period = period of years before 'y'
    Return: Dictionary {year : ['weekday_name']}
    '''
    dict = {}
    ITERATOR = 1
    try:
        y = y - period
        for _ in range(period):
            wkd = str(datetime.date(y, m, d).weekday())
            dict[y] = wkd
            y = y + ITERATOR
    except ValueError:
        print(f'{Fore.RED}Error: Year is out of range: 0. \nSpecify period that doesn\'t include 0 year')
    
    return dict

def get_table(dictionary):
    '''
    Creates a dictionary, where each key is a weekday and values are years,
    when the weekday name of date specified by user matches with the key
    Parameters: 
            dictionary {year : ['weekday_name']}
    Return:
            table dictionary {'weekday_name' : [year, year2 ... yearN]}
    '''
    monday    = []
    tuesday   = []
    wednesday = []
    thursday  = []
    friday    = []
    saturday  = []
    sunday    = []
    table     = {}
    for year, day in dictionary.items():
        if   day == '0': monday.append(year)
        elif day == '1': tuesday.append(year)
        elif day == '2': wednesday.append(year)
        elif day == '3': thursday.append(year)
        elif day == '4': friday.append(year)
        elif day == '5': saturday.append(year)
        elif day == '6': sunday.append(year)

    table['monday']    = monday
    table['tuesday']   = tuesday
    table['wednesday'] = wednesday
    table['thursday']  = thursday
    table['friday']    = friday
    table['saturday']  = saturday
    table['sunday']    = sunday
    
    return table

def create_plot(data, date, period):
    '''
    Creates a plot to visualize data.
    Weekday names are distributed by columns. 
    Hight(values) of the columns depends on how many times each weekday name is associated 
    with the date within specified period of years
    Parameters:
            data = dictionary with weekday names as keys and years as values
            date = user date, used in the plot title
            period = user period, used in the plot title
    Output: Graphics
    Return: None
    '''
    for k, v in data.items():
        plt.bar(str(k).capitalize(), len(v), align='center')
        plt.title(f'Weekday names for the period of {period} years before {date}')
        
    fig = plt.gcf()
    fig.set_size_inches(8,3)
    fig.canvas.manager.set_window_title('Weekdays')
    plt.show()

def print_year_weekday_pairs(dictionary,period,date):
    '''
    Prints a table, where left side of each line is a year
    from the specified period, and right side is a corresponding
    weekday name.
    Years are divided by tens for readability
    Parameters: 
            data = dictionary {year : ['weekday_name']}
            period = user defined period of years
            date = user defined date
    Output: 
            year : weekday_name
    Return: None
    '''
    print(f'{Fore.GREEN}Table of records for {period} years period before {str(date).replace("-",".")}{Fore.RESET}')
    for k, v in dictionary.items():
        print(f'{Fore.BLUE}{k} : {get_weekday_name(int(v))}{Fore.RESET}')
        if str(k).endswith('9'): print()

def print_weekdays_table(table):
    '''
    Prints a table of weekday names with corresponding lists of years
    Parameters:
            dictionary = Dictionary {'weekday_name' : [year, year1...yearN]}
            period = user defined period of years
            date = user defined date
    Output:
            Weekday_name1  : [year, year1, year2...yearN]
            Weekday_name2  : [year, year1, year2...yearN]
    Return: None
    '''
    print(f"{Fore.GREEN}Distribution of years by day of the week{Fore.RESET}")
    for k, v in table.items():
        print(f'{Fore.BLUE}{str(k).capitalize():<10} : {v}{Fore.RESET}')

def e_egg():
    print(f"""{Fore.YELLOW}
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠋⠉⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⣤⣤⣤⣤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠴⠒⠊⠉⠉⠀⠀⣿⣿⣿⠿⠋⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⡠⠼⠴⠒⠒⠒⠒⠦⠤⠤⣄⣀⠀⢀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⣼⠿⠋⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣇⠔⠂⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡟⠀⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⡤⠤⢴
⠀⠀⠀⠀⠀⠀⣸⠁⣾⣿⣀⣽⡆⠀⠀⠀⠀⠀⠀⠀⢠⣾⠉⢿⣦⠀⠀⠀⢸⡀⠀⠀⢀⣠⠤⠔⠒⠋⠉⠉⠀⠀⠀⠀⢀⡞
⠀⠀⠀⠀⠀⢀⡏⠀⠹⠿⠿⠟⠁⠀⠰⠦⠀⠀⠀⠀⠸⣿⣿⣿⡿⠀⠀⠀⢘⡧⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀
⠀⠀⠀⠀⠀⣼⠦⣄⠀⠀⢠⣀⣀⣴⠟⠶⣄⡀⠀⠀⡀⠀⠉⠁⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀
⠀⠀⠀⠀⢰⡇⠀⠈⡇⠀⠀⠸⡾⠁⠀⠀⠀⠉⠉⡏⠀⠀⠀⣠⠖⠉⠓⢤⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀
⠀⠀⠀⠀⠀⢧⣀⡼⠃⠀⠀⠀⢧⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⣧⠀⠀⠀⣸⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀⠀⠀⠘⣆⠀⠀⠀⢠⠏⠀⠀⠀⠀⠈⠳⠤⠖⠃⡟⠀⠀⠀⢾⠛⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣆⠀⠀⠀⠀⠈⠦⣀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠙⢦⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⡇⠙⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠋⠸⡇⠈⢳⡀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡼⣀⠀⠀⠈⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⣷⠴⠚⠁⠀⣀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡴⠁⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⡴⠚⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⢷⡆⠀⣠⡴⠧⣄⣇⠀⠀⠀⠀⠀⠀⠀⢲⠀⡟⠀⠀⠀⠀⠀⠀⠀⢀⡇⣠⣽⢦⣄⢀⣴⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡿⣼⣽⡞⠁⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠈⣷⠃⠀⠀⠀⠀⠀⠀⠀⣼⠉⠁⠀⠀⢠⢟⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣷⠉⠁⢳⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⣻⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠏⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠹⡆⠀⠈⡇⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢳⡀⠀⠙⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⢀⡄⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢳⡀⣰⣀⣀⣀⠀⠀⠀⠘⣦⣀⠀⠀⠀⡇⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⢸⡇⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠉⠉⠀⠀⠈⠉⠉⠉⠙⠻⠿⠾⠾⠻⠓⢦⠦⡶⡶⠿⠛⠛⠓⠒⠒⠚⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
       {Fore.RESET}""")

if __name__ == '__main__':
    main()

