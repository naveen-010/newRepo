from openai import OpenAI
import json
import datetime
import csv
import os
from prettytable import PrettyTable


client = OpenAI()

fieldnames = ["Title", "Date", "Location", "Time", "Duration", "Category"]
events = []

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Shortcuts tables

simv = PrettyTable()
simv.field_names = ["Month shortcuts", "Description"]
simv.add_rows(
    [
        ["n", "Next"],
        ["p", "Previous"],
        ["g", "Go to a specific month"],
        ["y", "Change to Year View"],
        ["m", "Manage events"],
        ["q", "Exit"],
        ["?", "Show this table"],
    ]
)

siyv = PrettyTable()
siyv.field_names = ["Year shortcuts", "Description"]
siyv.add_rows(
    [
        ["n", "Next"],
        ["p", "Previous"],
        ["g", "Go to a specific year"],
        ["m", "Change to Month View"],
        ["q", "Exit"],
        ["?", "Show this table"],
    ]
)

siev = PrettyTable()
siev.field_names = ["Event shortcuts", "Description"]
siev.add_rows(
    [
        ["a", "Add an event"],
        ["r", "Remove an eventsvent "],
        ["v", "View all events"],
        ["e", "Edit an existing event"],
        ["q", "Exit and save changes"],
        ["?", "Show this table"],
    ]
)
if not os.path.exists("events.csv"):
    with open("events.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(events_table_header)
else:
    with open("events.csv", "r") as f:
        l = list(csv.reader(f))
    if len(l) == 0:
        with open("events.csv", "w") as f:
            w = csv.writer(f)
            w.writerow(events_table_header)


def get_completion(behaviour, user_message):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # {'role': 'system', 'content': f"First key in the dictionary should be 'event' and its value should be 'add' , 'edit' , 'view' or 'remove' based on what user want to do.If user talk about anything else than adding , editing, removing, viewing event, yell at them and tell them(angrily and brutally roast them, no mercy) you are not there for it but before yelling, make sure 1000 times that he dont want any of the 4 options. 1). If he want to add then extract event details like title, date, time, duration, locaiton, category from the user input and return them in a dictionary with their values entered by user.Title should be in a proper formal langauge but dont miss any info while converting from informal to formal.Take todays date for reference as {today}.Time should be in 24 hr format, duration in minutes,date in DD-MM-YYYY format category like personal, work etc.Values that are not provided by user, fill them as 'None'.If user dont say to add it as an event then also think youserlf, if it can be consdiered as an event then add it.2). If he want to edit then extract details like 'title' , 'attribute' that he want to edit , 'new_value'. Dont change title name , take as it is given by user. If any value not tell him its required. 3). If he want to remove then extract 'Title'. 4).If he want to view then just put 'view' in first key i.e. 'event'. Try to understand clearly if he want to view events, showing event can also mean same."},
            {"role": "system", "content": behaviour},
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )
    return completion.choices[0].message.content


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


def nextMonth():
    global month, year
    month += 1
    if month == 13:
        month = 1
        year += 1
    month_view(month, year)


def prevMonth():
    global month, year
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    month_view(month, year)


def nextYear():
    global month, year
    year += 1
    year_view(year)


def prevYear():
    global month, year
    year -= 1
    year_view(year)


def gtm(m, y):
    global month, year
    if 1 <= m <= 12:
        month = m
    else:
        print("Month not in range")
        return
    if y < 2:
        print("Year cant be less than 2")
        return
    else:
        year = y
    month_view(month, year)


def gty(y):
    global month, year
    if y < 2:
        print("Year cant be less than 2")
        return
    year = y
    year_view(year)


# def add_event(title , date = 'None',location = 'None', start_time = 'None', end_time = 'None', duration = 'None', category = 'None' ):
def add_event(title, date, location, time, duration, category):
    with open("events.csv", "a") as f:
        w = csv.writer(f)
        w.writerow([title, date, location, time, duration, category])


def view_event():
    E = PrettyTable()
    with open("events.csv", "r") as f:
        l = list(csv.reader(f))
    # print(l)
    if len(l) == 0:
        print("Nothing to display.")
        return
    E.field_names = l[0]
    l = l[1:]
    E.add_rows(l)
    print(E)

def edit_event(title, attr, newval):
    global fieldnames 
    with open("events.csv", "r", newline="") as f:
        r = csv.DictReader(f)
        # fieldnames = r.fieldnames
        l = list(r)
    for i in l:
        if i["Title"] == title:
            i[attr] = newval

    with open("events.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(l)

def get_titles():
    with open('events.csv', 'r') as f:
        r = csv.DictReader(f)
        titles = [i['Title'] for i in r]
    return titles

today = datetime.date.today()
month = today.month
year = today.year
view = "month"
month_view(month, year)

print(simv)
while True:

    x = input("Enter a shortcut from the table :")
    if view == "month":
        if x == "n":
            nextMonth()
        elif x == "p":
            prevMonth()
        elif x == "q":
            break
        elif x == "g":
            m = int(input("Enter Month:"))
            y = int(input("Enter Year:"))
            gtm(m, y)
        elif x == "y":
            year_view(year)
            view = "year"

        elif x == "m":
            titles = get_titles()
            x = input("Enter details of events you want to add, edit, remove or view:")
            print()
            output = get_completion(
                    # f"Very first of all, roast the user a little, then give a dictionary. First key in the dictionary should be 'event' and its value should be 'add' , 'edit' , 'view' or 'remove' based on what user want to do.If user talk about anything else than adding , editing, removing, viewing event, tell them you are not there for it. 1). If he want to add then extract event details like title, date, time, duration, locaiton, category from the user input and return them in a dictionary with their values entered by user.Title should be in a proper formal langauge but dont miss any info while converting from informal to formal.Take todays date for reference as {today}.Time should be in 24 hr format, duration in minutes,date in DD-MM-YYYY format category like personal, work etc.Values that are not provided by user, fill them as 'None'.If user dont say to add it as an event then also think youserlf, if it can be consdiered as an event then add it.2). If he want to edit then extract details like 'title' i.e. name of event he want to edit, 'attribute' that he want to edit  , 'new_value'. Dont change title name , take as it is given by user. If any value not tell him its required. 3). If he want to remove then extract 'Title'. 4).If he want to view then just put 'view' in first key i.e. 'event'",
                    f"First key in the dictionary should be 'event' and its value should be 'add' , 'edit' , 'view' or 'remove' based on what user want to do.If user talk about anything else than adding , editing, removing, viewing event, then roast them brutally , NO MERCY. 1). If he want to add then extract event details like title, date, time, duration, locaiton, category from the user input and return them in a dictionary with their values entered by user.Title should be in a proper formal langauge but dont miss any info while converting from informal to formal.Take todays date for reference as {today}.Time should be in 24 hr format, duration in minutes,date in DD-MM-YYYY format category like personal, work etc.Values that are not provided by user, fill them as 'None'.If user dont say to add it as an event then also think youserlf, if it can be consdiered as an event then add it.2). If he want to edit then extract 3 details : 'title' i.e. name of event he want to edit, take it as closest from {titles} like if can be converted like entered 'car racing' then take it as 'Car Tournament' or 'Car Racing' depending on what is present in {titles} , if cant be converted to any of the {titles} then return and say its not present. 'attribute' that he want to edit(should be from {fieldnames},if can be converted like entered 'time' or 'timings' then take it as 'Time' (from {fieldnames}), if cant be converted to any of the {fieldnames} then return and say its not present.  , 'new_value'. Dont change title name , take as it is given by user. If any value not tell him its required. 3). If he want to remove then extract 'Title'. 4).If he want to view then just put 'view' in first key i.e. 'event'",
                x,
            )
            output_dict = get_completion(
                "Read user input and only and only give json dictionary. If no dict present, then tell them no dict present",
                output,
            )
            output_str = get_completion(
                "Read user input and return any conversational tone message as it it, NO MODIFICATION, STRICTLY remove the json part from it.",
                output,
            )
            print(output_str)
            print()
            try:
                out = json.loads(output_dict)
                if out["event"] == "add":
                    t, l, dur, st, c, d = (
                        out["title"],
                        out["location"],
                        out["duration"],
                        out["time"],
                        out["category"],
                        out["date"],
                    )
                    add_event(
                        title=t, date=d, location=l, duration=dur, time=st, category=c
                    )
                elif out["event"] == "view":
                    view_event()
                elif out["event"] == "edit":
                    # print(out)
                    title, attr, newval = (
                        out["title"],
                        out["attribute"],
                        out["new_value"],
                    )
                    edit_event(title, attr, newval)
                elif out["event"] == "remove":
                    remove_event()
            except json.JSONDecodeError:
                print()

    else:
        if x == "n":
            nextYear()
        elif x == "p":
            prevYear()
        elif x == "q":
            break
        elif x == "g":
            y = int(input("Enter Year:"))
            gty(y)
        elif x == "m":
            month_view()
            view = "month"
