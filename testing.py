import csv
with open('events.csv', 'r') as file:
    reader = csv.reader(file)

    # Iterate through each row in the CSV
    for row in reader:
        print(row) 
