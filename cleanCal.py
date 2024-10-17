from openai import OpenAI 
from fish_audio_sdk import Session, TTSRequest
import json
import datetime
import csv
import os
from prettytable import PrettyTable


print("\x1B[2J\x1B[H")
client = OpenAI()

today = datetime.date.today()
month = today.month
year = today.year
date = today.day
view = "month"


fieldnames = ["Title", "Date", "Location", "Time", "Duartion", "Category"]
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
        ["t", "Go to Today's Month"],
        ["n", "Next"],
        ["p", "Previous"],
        ["g", "Go to a specific month"],
        ["y", "Change to Year View"],
        ["m", "Manage events"],
        ["q", "Exit"],
        # ["?", "Show this table"],
    ]
)

siyv = PrettyTable()
siyv.field_names = ["Year shortcuts", "Description"]
siyv.add_rows(
    [
        ["t", "Go to Today's Year"],
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
        w.writerow(fieldnames)
else:
    with open("events.csv", "r") as f:
        l = list(csv.reader(f))
    if len(l) == 0:
        with open("events.csv", "w") as f:
            w = csv.writer(f)
            w.writerow(fieldnames)


def get_completion(behaviour, user_message):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
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
    try:
        if len(time) != 5 or time[2] != ":":
            return False
        if not 0 <= int(time[0:2]) <= 24:
            return False
        if not 0 <= int(time[3:5]) < 60:
            return False
        return True
    except Exception as e:
        print('\033[38;5;196mInvalid time\033[0m')


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


def one_line(d, no_of_days, today):
    for i in range(1, 8, 1):
        if d <= 0 or d > no_of_days:
            print(" ", end="   ")
        elif d == date and today == True:
            print(f"\033[38;5;204m{d}\033[0m", end="  ")
        elif no_of_days >= d > 9:
            print(f"\033[1;37m{d}\033[0m", end="  ")
        else:
            print(f"\033[1;37m{d}\033[0m", end="   ")
        d = d + 1


def year_view(year):

    if not 0 < year:
        print(f"\033[38;5;196mYear cannot be 0 or negative\033[0m")
        return

    for monthrow in range(3):
        x = 1 + (monthrow) * 4
        y = x + 4
        for monthcol in range(x, y):
            # print(f'{f"     {months[monthcol-1]},  {year}":<28}', end="")
            print(f'\033[38;5;230m{f"     {months[monthcol-1]},  {year}":<28}\033[0m', end="")
            print("\t", end="")
        print()
        for monthcol in range(x, y):
            print(f'\033[38;5;215mSu  M   Tu  W   Th  F   Sa  \033[0m', end="")
            print("\t", end="")
        print()

        for row in range(7):
            for monthcol in range(x, y):
                d = cal_d(monthcol, year) + row * 7
                no_of_days = cal_no_of_days(monthcol, year)
                if monthcol == today.month and year == today.year:
                    one_line(d, no_of_days, today = True)
                else:
                    one_line(d, no_of_days, today = False)

                print("\t", end="")
            print()

# print()
def month_view(month, year):
    if not 1 < year:
        print(f"\033[38;5;196mYear cannot be negative\033[0m")
        return
    if not 0 < month < 13:
        print(f"\033[38;5;196mMonth should be between 1 and 12\033[0m")
        return

    # print(f'{f"     {months[month-1]},  {year}":<28}')
    print(f'\033[38;5;230m{f"     {months[month-1]},  {year}":<28}\033[0m')
    # print(f"Su  M   Tu  W   Th  F   Sa  ")
    # print(f'\033[1;34mSu  M   Tu  W   Th  F   Sa  \033[0m')
    print(f'\033[38;5;215mSu  M   Tu  W   Th  F   Sa  \033[0m')

    for row in range(7):
        d, no_of_days = cal_d(month, year) + row * 7, cal_no_of_days(month, year)
        if month == today.month and year == today.year:
            one_line(d, no_of_days, today= True)
        else:
            one_line(d, no_of_days, today = False)

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
        print(f"\033[38;5;196mMonth not in range\033[0m")
        return
    if y < 2:
        print(f"\033[38;5;196mYear cant be less than 2\033[0m")
        return
    else:
        year = y
    print("\x1B[2J\x1B[H")
    print(f'\033[38;5;230m{simv}\033[0m')
    print()
    month_view(month, year)


def gty(y):
    global month, year
    if y < 2:
        print(f"\033[38;5;196mYear cant be less than 2\033[0m")
        return
    year = y
    print("\x1B[2J\x1B[H")
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
    print(f'\033[38;5;230m{E}\033[0m')
    print()

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

def remove_event(title):
    if title == 'all':
        with open("events.csv", "w") as f:
           w = csv.writer(f)
           w.writerow(fieldnames)
           return

    with open('events.csv' , 'r', newline = '') as f:
        rows = list(csv.reader(f))
        rowsCopy = [row for row in rows if row[0] != title]

    with open('events.csv' , 'w', newline = '') as f:
        w = csv.writer(f)
        w.writerows(rowsCopy)


def get_titles():
    with open('events.csv', 'r') as f:
        r = csv.DictReader(f)
        titles = [i['Title'] for i in r]
    return titles
msg = '''
$$\      $$\           $$\                                             $$\ 
$$ | $\  $$ |          $$ |                                            $$ |
$$ |$$$\ $$ | $$$$$$\  $$ | $$$$$$$\  $$$$$$\  $$$$$$\$$$$\   $$$$$$\  $$ |
$$ $$ $$\$$ |$$  __$$\ $$ |$$  _____|$$  __$$\ $$  _$$  _$$\ $$  __$$\ $$ |
$$$$  _$$$$ |$$$$$$$$ |$$ |$$ /      $$ /  $$ |$$ / $$ / $$ |$$$$$$$$ |\__|
$$$  / \$$$ |$$   ____|$$ |$$ |      $$ |  $$ |$$ | $$ | $$ |$$   ____|    
$$  /   \$$ |\$$$$$$$\ $$ |\$$$$$$$\ \$$$$$$  |$$ | $$ | $$ |\$$$$$$$\ $$\ 
\__/     \__| \_______|\__| \_______| \______/ \__| \__| \__| \_______|\__|
'''
print(msg)
                                                                        
                                                                           
print(f'\033[38;5;230m{simv}\033[0m')
# print()
# month_view(month, year)
print()

try:
    while True:
        # print(f'\033[38;5;230m{simv}\033[0m')
        print()
        x = input("\033[38;5;12mEnter a shortcut from the table :\033[0m")
        if view == "month":
            if x == "n":
                print("\x1B[2J\x1B[H")
                print(f'\033[38;5;230m{simv}\033[0m')
                print()
                nextMonth()
            elif x == "t":
                print("\x1B[2J\x1B[H")
                print(f'\033[38;5;230m{simv}\033[0m')
                print()
                month_view(today.month, today.year)
                month = today.month
                year = today.year
            elif x == "p":
                print("\x1B[2J\x1B[H")
                print(f'\033[38;5;230m{simv}\033[0m')
                print()
                prevMonth()
            elif x == "q":
                break
            elif x == "g":
                m = int(input("\033[38;5;12mEnter Month:\033[0m"))
                y = int(input("\033[38;5;12mEnter Year:\033[0m"))
                gtm(m, y)
            elif x == "y":
                print("\x1B[2J\x1B[H")
                year_view(year)
                view = "year"
            # elif x == '?':
            #     print(f'\033[38;5;230m{simv}\033[0m')
            elif x == "m":
                while True:
            
                    titles = get_titles()
                    x = input("\033[38;5;12mEnter details of events you want to add, edit, remove or view:\033[0m")
                    if x == 'q' or x == 'quit' or x == 'exit':
                        break
                    else:
                        mainprompt = f"""

                        **Instructions:**

                        1. **General Behavior**:
                           - The first key in the dictionary must always be **'event'**, and its value should be one of the following based on the user’s intent:
                             - `'add'`: If the user mentions adding, creating, or scheduling an event.
                             - `'edit'`: If the user mentions changing, modifying, or updating an existing event.
                             - `'view'`: If the user mentions viewing, showing, or checking an event.
                             - `'remove'`: If the user mentions deleting, canceling, or removing an event.

                           If the user talks about something completely unrelated to adding, editing, removing, or viewing events, **roast them mercilessly**. The roast must be witty, relevant, and **brutal but with sense**. If no roast-worthy material exists, skip the roast. Do **not force it**.

                        2. **Add Event**:
                           - If the user wants to **add** an event (whether they use terms like "add", "schedule", "create", or anything else that implies creating a new event), extract the following details from their input:
                             - **'Title'**: Ensure the title is formal and capitalized properly. Any informal or casual phrases should be converted to a more appropriate tone. For example, "hang out with friends" becomes "Casual Gathering with Friends". **Do not lose any information**, even when adjusting the tone.
                             - **'Date'**: Format as **DD-MM-YYYY**. If the date is not mentioned, fill it as `'None'`.
                             - **'Time'**: Convert it to **24-hour format**. If not provided, set as `'None'`.
                             - **'Duration'**: If mentioned, convert the duration to **minutes**. If not, fill as `'None'`.
                             - **'Location'**: Extract the location and fill it in. If no location is provided, set as `'None'`.
                             - **'Category'**: Assign a category based on what the user specifies (e.g., 'personal', 'work', 'leisure'). If no category is given, set it as `'None'`.

                            If the user doesn’t explicitly mention they want to add something as an event but their description fits the definition of an event, use your judgment to add it anyway. Take today's date for reference as **{today}**.

                        3. **Edit Event**:
                           - If the user wants to **edit** an event (terms like "change", "modify", "update" imply this), extract the following 3 details:
                             - **'Title'**: The name of the event they want to edit. Match it to the **closest** title from the list of available titles **{titles}**. If the user enters something like "car racing," match it to "Car Racing" or "Car Tournament", depending on what exists in **{titles}**. If no match is found, return with a message that says the event is **not present**.
                             - **'Attribute'**: The attribute the user wants to edit (such as 'time', 'location', 'date', etc.). Match the attribute to the closest one from **{fieldnames}** (e.g., if the user types "timings", take it as 'Time'). If no match can be made, return with a message saying the attribute is **not present**.
                             - **'New_value'**: The new value they want to assign to the chosen attribute. If the user doesn't specify the new value, return with a message saying that the **new value is required**.

                        4. **Remove Event**:
                           - If the user wants to **remove** or **delete** an event, extract the **title**:
                           - If the user wants to remove all events, extract the title as 'all' when they use phrases like "delete all", "clear everything", or "remove all".
                           - Match the title to the closest one from **{titles}** (similar to the "Edit" operation). If the user types something like "car racing," match it to "Car Racing" or "Car Tournament" depending on what exists in **{titles}**. If no match is found, return with a message that says the event is **not present**.

                        5. **View Event**:
                           - If the user wants to **view** an event (mentions terms like "show", "see", "display", etc.), just set the value of the `'event'` key to **'view'**. No additional data extraction is required for this operation.

                        **Roast Logic**:
                        - If the user talks about something off-topic (unrelated to adding, editing, removing, or viewing events), roast them with maximum savagery. No mercy should be shown. If they’re discussing sensitive topics like depression or making self-destructive statements, respond with brutal sarcasm, as many users ask these things for fun. Examples:
                           - If the user says something unrelated, like "I'm thinking about giving up on everything," respond with something like: "Wow, deep thoughts for someone who can’t even schedule a simple event. Maybe focus on getting your life organized before having an existential crisis."
                           - If they ask, "Should I even try anymore?", you could roast them with: "Try scheduling an event first; let’s start with small victories before taking on the universe."
                           - However, if no roast-worthy material exists, don’t force it. Skip the roast.

                        """
                        output = get_completion(mainprompt, x)
                                #  f"First key in the dictionary should be 'event' and its value should be 'add' , 'edit' , 'view' or 'remove' based on what user want to do(add, edit/change etc , view/see/show etc , delete/remove/delete all/remove all etc.).If user talk about anything else that is not even a bit related to adding , editing, removing, viewing event, then roast them brutally , NO MERCY, but the roast should make sense.If no good roast can be made on the user message  then please don't feel obligated to push yourself unnecessarily. 1). If he want to add then extract event details like Title, Date, Time, Duration, Locaiton, Category from the user input and return them in a dictionary with their values entered by user.Title should be in a proper formal langauge but dont miss any info while converting from informal to formal.Take todays date for reference as {today}.Time should be in 24 hr format, duration in minutes,date in DD-MM-YYYY format category like personal, work etc.Values that are not provided by user, fill them as 'None'.If user dont say to add it as an event then also think youserlf, if it can be consdiered as an event then add it.2). If he want to edit then extract 3 details : 'title' i.e. name of event he want to edit, take it as closest from {titles} like if can be converted like entered 'car racing' then take it as 'Car Tournament' or 'Car Racing' depending on what is present in {titles} , if cant be converted to any of the {titles} then return and say its not present. 'attribute' that he want to edit(should be from {fieldnames},if can be converted like entered 'time' or 'timings' then take it as 'Time' (from {fieldnames}), if cant be converted to any of the {fieldnames} then return and say its not present.  , 'new_value'. Dont change title name , take as it is given by user. If any value not tell him its required. 3). If he want to remove then extract 'Title' i.e. name of event he want to edit, take it as closest from {titles} like if can be converted like entered 'car racing' then take it as 'Car Tournament' or 'Car Racing' depending on what is present in {titles} , if cant be converted to any of the {titles} then return and say its not present. 4).If he want to view then just put 'view' in first key i.e. 'event'",

                        output_dict = get_completion(
                            "Read user input and only and only give json dictionary. If no dict present, then tell them no dict present",
                            output,
                        )
                        output_str = get_completion(
                            # "Read user input and return any conversational tone message, MAKE IT UNDER 50 WORDS, STRICTLY remove the json part from it",
                            "Remove any json part from the input , if the left text is more than 50, shrink it to fit under 50 words. Dont change the tone of the text while shrinking it. If the text excluding json is less than 50 words, dont modify it and return it as it is.",
                            output,
                        )
                        print(f'\033[38;5;85m{output_str}\033[0m')
                        try:
                            out = json.loads(output_dict)
                            if out["event"] == "add":
                                t, l, dur, st, c, d = (
                                    out["Title"],
                                    out["Location"],
                                    out["Duration"],
                                    out["Time"],
                                    out["Category"],
                                    out["Date"],
                                )
                                add_event(
                                    title=t, date=d, location=l, duration=dur, time=st, category=c
                                )
                            elif out["event"] == "view":
                                view_event()
                            elif out["event"] == "edit":
                                # print(out)
                                title, attr, newval = (
                                    out["Title"],
                                    out["Attribute"],
                                    out["New_value"],
                                    )
                                edit_event(title, attr, newval)
                            elif out["event"] == "remove":
                                    remove_event(out['Title'])
                        except json.JSONDecodeError:
                            print()
            else:
                # a = get_completion('Roast the user because they entered invalid input', x)
                # print(f'\033[38;5;85m{a}\033[0m')
                print(f"\033[38;5;196mInvalid input\033[0m")


        else:
            if x == "n":
                print("\x1B[2J\x1B[H")
                nextYear()
            elif x == 't':
                print("\x1B[2J\x1B[H")
                year_view(today.year)
                year = today.year
            elif x == "p":
                print("\x1B[2J\x1B[H")
                prevYear()
            elif x == "q":
                break
            elif x == "g":
                y = int(input("\033[38;5;12mEnter Year:\033[0m"))
                gty(y)
            elif x == '?':
                print(f'\033[38;5;230m{siyv}\033[0m')
            elif x == "m":
                m = int(input("\033[38;5;12mEnter Month:\033[0m"))
                try:
                    m = int(m)  # Convert the input to an integer
                    if 1 <= m <= 12:  # Check if the input is a valid month number
                        month = m
                        print("\x1B[2J\x1B[H")
                        print(f'\033[38;5;230m{simv}\033[0m')
                        print()
                        month_view(month, year)
                        view = "month"
                    else:
                        print("\033[38;5;196mPlease enter a valid month number between 1 and 12.\033[0m")
                except ValueError:
                    print(f"\033[38;5;196mInvalid input. Please enter a number.\033[0m")
            else:
                print(f"\033[38;5;196mInvalid input\033[0m")
except Exception as e:
    print(f'\033[38;5;196m{e}\033[0m')
