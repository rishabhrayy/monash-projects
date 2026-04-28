from tabulate import tabulate
import csv

file_names = [
    "grades.csv",
    "class_students.csv",
    "rabbytes_club_students.csv",
    "rabbytes_data.csv"
]

user_tables = []
deleted_tables = []

def read_csv_file(file_name):
    #Reads a CSV file and outputs a list of rows as its contents.
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]
    return rows

# Load CSV files into user_tables
for file_name in file_names:
    user_tables.append(read_csv_file(file_name))

def list_tables():
    #Lists the tables along with the number of rows, columns, and indices.
    table_data = []
    for index, table in enumerate(user_tables):
        if table is not None:
            table_cols = len(table[0])
            table_rows = len(table)
            table_data.append([index, table_cols, table_rows])
    print(tabulate(table_data, headers=["Index", "Columns", "Rows"]))

def display_table():
    #asks the user to choose a table index, then shows the chosen table.
    while True:
            print("Choose a table index (to display):")
            table_index = int(input())
            if 0 <= table_index < len(user_tables) and user_tables[table_index] is not None:
                print(tabulate(user_tables[table_index], headers="firstrow"))
                break
            else:
                print("Incorrect table index. Try again.")

def duplicate_table():
    #asks the user to choose a table index and then makes a replica of the chosen table.
    while True:
            print("Choose a table index (to duplicate):")
            table_index = int(input())
            if 0 <= table_index < len(user_tables) and user_tables[table_index] is not None:
                # Deep copy of the table
                user_tables.append([row[:] for row in user_tables[table_index]])
                break
            else:
                print("Incorrect table index. Try again.")


def main_menu():
    #Processes user selections and presents a menu for interacting with CSV tables.
    while True:
        print("""==================================
Enter your choice:
1. List tables.
2. Display table.
3. Duplicate table.
0. Quit.
==================================""")
        user_choice = input()

        if user_choice == '1':
            list_tables()
        elif user_choice == '2':
            display_table()
        elif user_choice == '3':
            duplicate_table()
        elif user_choice == '0':
            exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
