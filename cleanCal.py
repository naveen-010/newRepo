import datetime 
import csv
import os
from prettytable import PrettyTable
events_table_header = [ "Title", "Date", "Location", "Start Time", "End Time", "Duartion", "Category" ]
events = []

months = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", ]

# Shortcuts tables

simv = PrettyTable()
simv.field_names = ['Month shortcuts', 'Description']
simv.add_rows([
    ["n", "Next"],
    ["p", "Previous"],
    ["g", "Go to a specific month"],
    ["y", "Change to Year View"],
    ["m", "Manage events"],
    ["q", "Exit"],
    ["?", "Show this table"]
    ])

siyv = PrettyTable()
siyv.field_names = ['Year shortcuts', 'Description']
siyv.add_rows([
    ["n", "Next"],
    ["p", "Previous"],
    ["g", "Go to a specific year"],
    ["m", "Change to Month View"],
    ["q", "Exit"],
    ["?", "Show this table"],
])

siev = PrettyTable()
siev.field_names = ['Event shortcuts', 'Description']
siev.add_rows([
    ["a", "Add an event"],
    ["r", "Remove an eventsvent "],
    ["v", "View all events"],
    ["e", "Edit an existing event"],
    ["q", "Exit and save changes"],
    ["?", "Show this table"],
])

if not os.path.exists('events.csv'):
    with open('events.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(events_table_header)

 
today = datetime.date.today()
month = today.month
year = today.year
view = 'month'

def is_leap(year):
    if year % 400 == 0 or year % 100 != 0 and year % 4 == 0:
        return True
    else:
        return False

def cal_no_of_days(month, year):
    if (month % 7) % 2 == 0 and month != 2 and month != 7:
        no_of_days = 30
    elif month == 2:
        no_of_days = 29 if is_leap(year) else 28
    else:
        no_of_days = 31
    return no_of_days

def isDate(date):
    if len(date) != 10 or date[2] != "-" or date[5] != "-":
        return None

    day, month, year = date.split("-")

    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return None

    day = int(day)
    month = int(month)
    year = int(year)

    if year < 1 or year > 9999 or month < 1 or month > 12:
        return None

    days_in_month = cal_no_of_days(month, year)

    if day < 1 or day > days_in_month:
        return None

    return day, month, year

def isTime(time):
    if len(time) != 5 or time[2] != ":":
        return False
    if not 0 <= int(time[0:2]) <= 24:
        return False
    if not 0 <= int(time[3:5]) < 60:
        return False
    return True

def cal_d(month, year):
    num_of_leaps = 0
    for i in range(1, year, 1):
        if is_leap(i):
            num_of_leaps += 1

    num_of_leaps_till_year = 0
    for i in range(1, year + 1, 1):
        if is_leap(i):
            num_of_leaps_till_year += 1

    if month == 1:
        a = (year + num_of_leaps + 1) % 7
        if a == 0:
            a = 7
    elif month == 2:
        a = (year + num_of_leaps + 4) % 7
        if a == 0:
            a = 7
    elif month >= 3:
        x = 4  # substitue of 4 in jan
        for m in range(3, 13, 1):
            a = (year + num_of_leaps_till_year + x) % 7
            if (m % 7) % 2 == 0 and m != 7:
                x = (x + 2) % 7
            else:
                x = (x + 3) % 7
            if a == 0:
                a = 7
            if m == month:
                break
    d = 2 - a
    return d

def one_line(d, no_of_days):
    for i in range(1, 8, 1):
        if d <= 0 or d > no_of_days:
            print(" ", end="   ")
        elif no_of_days >= d > 9:
            print(d, end="  ")
        else:
            print(d, end="   ")
        d = d + 1

def year_view(year):

    if not 0 < year:
        print("Year cannot be 0 or negative")
        return

    for monthrow in range(3):
        x = 1 + (monthrow) * 4
        y = x + 4
        for monthcol in range(x, y):
            print(f'{f"     {months[monthcol-1]},  {year}":<28}', end="")
            print("\t", end="")
        print()
        for monthcol in range(x, y):
            print(f"Su  M   Tu  W   Th  F   Sa  ", end="")
            print("\t", end="")
        print()

        for row in range(7):
            for monthcol in range(x, y):
                d = cal_d(monthcol, year) + row * 7
                no_of_days = cal_no_of_days(monthcol, year)
                one_line(d, no_of_days)
                print("\t", end="")
            print()


def month_view(month, year):
    if not 1 < year:
        print("Year cannot be negative")
        return
    if not 0 < month < 13:
        print("Month should be between 1 and 12")
        return

    print(f'{f"     {months[month-1]},  {year}":<28}')
    print(f"Su  M   Tu  W   Th  F   Sa  ")

    for row in range(7):
        d, no_of_days = cal_d(month, year) + row * 7, cal_no_of_days(month, year)
        one_line(d, no_of_days)
        print()


       
month_view(month,year)




