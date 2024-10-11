# calendar 180
import os
import csv
import datetime
from prettytable import PrettyTable

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


shortcutsTable = PrettyTable(["Shortcuts", "Description"])

events_table_header_for_printing = PrettyTable(
    ["S.No.", "Event Name", "Event attributes"]
)

events_table_header_for_saving = [
    "Title",
    "Date",
    "Location",
    "Start Time",
    "End Time",
    "Duartion",
    "Category",
]
events_table_list_for_savings = []

shortcuts_in_monthview = [
    ["n", "Next"],
    ["p", "Previous"],
    ["g", "Go to a specific month"],
    ["y", "Change to Year View"],
    ["m", "Manage events"],
    ["q", "Exit"],
    ["?", "Show this table"],
]

shortcuts_in_eventview = [
    ["a", "Add an event"],
    ["r", "Remove an eventsvent "],
    ["v", "View all events"],
    ["e", "Edit an existing event"],
    # ["s" , "Save changes"],
    ["q", "Exit"],
    ["?", "Show this table"],
]
events_list = []
options = [
    "Date(d)",
    "Location(l)",
    "Category(eg. bday)(c)",
    "Start Time(st)",
    "End Time(et)",
    "Duration(dur)",
]

shortcuts_in_yearview = [
    ["n", "Next"],
    ["p", "Previous"],
    ["g", "Go to a specific year"],
    ["m", "Change to Month View"],
    ["q", "Exit"],
    ["?", "Show this table"],
]


class Event:
    def __init__(
        self, title
    ):  # , date=None, location = None,start_time = None, duration = None
        self.title = title
        self.date = None
        self.location = None
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.category = None
        self.addedOptions = []
        self.allOptions = [
            self.title,
            self.date,
            self.location,
            self.start_time,
            self.end_time,
            self.duration,
            self.category,
        ]

    def add(self, option, value):
        self.addedOptions.append(option)
        setattr(self, option, value)

    def remove(self, option):
        self.addedOptions.remove(option)

    def update(self, option, newval):
        setattr(self, option, newval)


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


def add_event():
    title = input("Enter event name: ")
    new_event = Event(title)
    events_list.append(new_event)

    options = {
        "d": ("Date", "Enter the date in DD-MM-YYYY format: ", "date", isDate),
        "l": ("Location", "Enter the location: ", "location", None),
        "c": ("Category", "Enter the category: ", "category", None),
        "st": (
            "Start Time",
            "Enter the time in 24 hrs HH:MM format: ",
            "start_time",
            isTime,
        ),
        "et": (
            "End Time",
            "Enter the time in 24 hrs HH:MM format: ",
            "end_time",
            isTime,
        ),
        "dur": ("Duration", "Enter duration in minutes: ", "duration", None),
    }

    while options:
        selected_option = input(
            f"Which option do you want to add? {', '.join([f'{key}: {value[0]}' for key, value in options.items()])} or type 'done' to finish: "
        )

        if selected_option == "done":
            break

        if selected_option in options:
            option_details = options[selected_option]
            value = input(option_details[1])

            # Validate the input if a validation function is provided
            if option_details[3] and not option_details[3](value):
                print(f"Invalid {option_details[0].lower()}.")
                continue

            new_event.add(option_details[2], value)
            print(f"{option_details[0]} has been added.")
            del options[selected_option]  # Remove added option from the list

        else:
            print("Invalid option. Please select a valid option.")

    print("Event added successfully!")


def remove_event():
    if len(events_list) == 0:
        print("No events to remove.")
        return
    for i in range(len(events_list)):
        print(f"{i + 1}. {events_list[i].title}")
    index = int(input("Select the event number to remove: ")) - 1
    if 0 <= index < len(events_list):
        events_list.pop(index)
        print("Event removed successfully!")
    else:
        print("Invalid event number.")


def edit_event():
    if not events_list:
        print("No events to edit.")
        return
    for i in range(len(events_list)):
        print(f"{i + 1}. {events_list[i].title}")
    index = int(input("Select the event number to edit: ")) - 1
    if 0 <= index < len(events_list):
        event = events_list[index]
        option = (
            input("What do you want to edit? (title, date, location, time, duration): ")
            .strip()
            .lower()
        )
        if option == "date":
            value = input("Enter new date in DD-MM-YYYY format: ")
            result = isDate(value)
            if result is None:
                print("Invalid date.")
                return
            event.update(field, value)

        elif option in events_list[i].options:
            value = input(f"Enter new value for {option}: ")
            event.update(option, value)
            print("Event updated successfully!")
        else:
            print("Invalid field.")
    else:
        print("Invalid event number.")


def view_events():

    if len(events_list) == 0:
        print("No event to display.")
        return

    for i in range(len(events_list)):
        print(f"{i + 1}. {events_list[i].title}")


def save_events():
    for i in events_list:
        events_table_list_for_savings.append(
            [
                getattr(i, attr) if getattr(i, attr) else "None"
                for attr in [
                    "title",
                    "date",
                    "location",
                    "start_time",
                    "end_time",
                    "duration",
                    "category",
                ]
            ]
        )
    if not os.path.exists("events.csv"):
        with open("events.csv", mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(events_table_header_for_saving)

            writer.writerows(events_table_list_for_savings)

    else:
        with open("events.csv", mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)

            writer.writerows(events_table_list_for_savings)


def cal_d(month, year):
    # Number of leap years from 1-(year/year+1)
    num_of_leaps = 0
    for i in range(1, year, 1):
        if is_leap(i):
            num_of_leaps += 1

    num_of_leaps_till_year = 0
    for i in range(1, year + 1, 1):
        if is_leap(i):
            num_of_leaps_till_year += 1

    # Calculating day
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


def reset_view(printed_lines):
    for _ in range(printed_lines):
        print("\033[A", end="")  # Move cursor up by one line
        print("\033[K", end="")  # Clear the current line


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

    # if not (month.isdigit() and year.isdigit()):
    # print("Inputs must be a number")
    # return
    # year, month = int(year), int(month)

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

    # if not (month.isdigit() and year.isdigit()):
    #    print("Inputs must be a number")
    #    return
    # year, month = int(year), int(month)

    # print('***************')
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
        # if d == 1:
        #     print()
        one_line(d, no_of_days)
        print()

    # print('***************')


today = datetime.date.today()
month = today.month
year = today.year
shortcutsTable.clear_rows()
shortcutsTable.add_rows(shortcuts_in_monthview)
print(shortcutsTable)
month_view(month, year)
view = "month"


# fd = sys.stdin.fileno()  # Get file descriptor for stdin
# old_settings = termios.tcgetattr(fd)  # Save current terminal settings

# try:
#    tty.setraw(fd)
# lines_after_calendar = 0
while True:

    x = input("Select a shortcut to continue(press ? for help):")

    # lines_after_calendar += 1

    if view == "month":
        if x == "n" or x == "^[[C":
            month += 1
            if month > 12:
                month = 1
                year += 1

            print("\x1B[2J\x1B[H")  # Clear screen and move cursor to top-left corner
            # reset_view(lines_after_calendar )
            # lines_after_calendar = 0
            month_view(month, year)
            # lines_after_calendar = 10

        elif x == "p" or x == "^[[D":
            month -= 1
            if month < 1:
                month = 12
                year -= 1

            print("\x1B[2J\x1B[H")  # Clear screen and move cursor to top-left corner
            # reset_view(lines_after_calendar )
            # lines_after_calendar = 0
            month_view(month, year)
            # lines_after_calendar = 10

            # print("\03s[11A\033[J")
            # month_view(month, year)
        elif x == "y":
            print("\x1B[2J\x1B[H")  # Clear screen and move cursor to top-left corner
            view = "year"
            year_view(year)

        elif x == "g":
            m = int(input("Enter month no.: "))
            y = int(input("Enter year no.: "))
            if 0 < m < 13 and y > 0:
                print("\x1B[2J\x1B[H")
                month = m
                year = y
                # reset_view(lines_after_calendar )
                # lines_after_calendar = 0
                month_view(month, year)
                # lines_after_calendar = 10

                # month_view(month , year)
            else:
                print("Month should be between 1 and 12")

        elif x == "m":
            shortcutsTable.clear_rows()
            shortcutsTable.add_rows(shortcuts_in_eventview)
            print(shortcutsTable)

            while True:

                x = input("Select a shortcut to continue(press ? for help):")
                if x == "a":
                    add_event()

                elif x == "r":
                    remove_event()

                elif x == "e":
                    edit_event()

                elif x == "v":
                    view_events()

                elif x == "?":
                    shortcutsTable.clear_rows()
                    shortcutsTable.add_rows(shortcuts_in_eventview)
                    print(shortcutsTable)

                elif x == "q":
                    save_events()
                    break

                else:
                    print("Invalid input.")

        elif x == "?":
            shortcutsTable.clear_rows()
            shortcutsTable.add_rows(shortcuts_in_monthview)
            print(shortcutsTable)

        elif x == "q":
            break
        else:
            print("Enter a valid choice")

    #        elif x == "\x1b[A":
    #            year -= 1
    #            print("\x1B[2J\x1B[H")
    #            # Clear screen and move cursor to top-left corner
    #            month_view(month, year)
    #
    #        elif x == "\x1b[B":
    #            year += 1
    #            print("\x1B[2J\x1B[H")
    #            # Clear screen and move cursor to top-left corner
    #            month_view(month, year)
    #
    #        elif x == "\x1b[C":
    #            month += 1
    #            if month == 13:
    #                month = 1
    #                year += 1
    #
    #        elif x == "\x1b[D":
    #            month -= 1
    #            if month == 0:
    #                month = 12
    #                year -= 1
    #            print("\x1B[2J\x1B[H")
    #            # Clear screen and move cursor to top-left corner
    #            month_view(month, year)
    else:  # Year view
        if x == "n":
            year += 1
            print("\x1B[2J\x1B[H")
            # Clear screen and move cursor to top-left corner
            year_view(year)

        elif x == "p":
            year -= 1
            print("\x1B[2J\x1B[H")
            # Clear screen and move cursor to top-left corner
            year_view(year)

        elif x == "m":
            view = "month"
            month = int(input("Enter month no.: "))
            print("\x1B[2J\x1B[H")
            # Clear screen and move cursor to top-left corner
            month_view(month, year)

        elif x == "h":
            print(table)

        elif x == "g":
            y = int(input("Enter year no.: "))
            if y > 0:
                print("\x1B[2J\x1B[H")
                year = y
                year_view(year)
            else:
                print("Year cannot be less than 1")

        elif x == "?":
            shortcutsTable.clear_rows()
            shortcutsTable.add_rows(shortcuts_in_yearview)
            print(shortcutsTable)

        elif x == "q":
            break
        else:

            print("enter a valid choice")


# finally:
#    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore original settings
