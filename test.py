
import csv
from prettytable import PrettyTable

def view_event():
    E = PrettyTable()
    
    with open('events.csv', 'r') as f:
        l = list(csv.reader(f))  # Read the CSV file into a list of rows
        print(f"Read from CSV: {l}")  # Debug: print what is read from CSV

    if len(l) == 0:
        print('Nothing to display.')
        return
    
    # Get the header
    E.field_names = l[0]
    
    # Check for duplicates in header
    if len(E.field_names) != len(set(E.field_names)):
        print("Error: Duplicate field names found in the header.")
        return
    
    l = l[1:]  # Exclude the header row
    E.add_rows(l)
    
    # Print the formatted table
    print(E)

# Example call to view events
view_event()
