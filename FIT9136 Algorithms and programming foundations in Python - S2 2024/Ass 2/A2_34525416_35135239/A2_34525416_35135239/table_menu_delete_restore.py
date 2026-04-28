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

# Load tables from CSV files
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
                # Deep copy the table
                user_tables.append([row[:] for row in user_tables[table_index]])
                break
            else:
                print("Incorrect table index. Try again.")

def create_table():
    #Selects particular columns from an existing table to create a new table.

    while True:
            print("Choose a table index (to create from):")
            table_index = int(input())
            if 0 <= table_index < len(user_tables) and user_tables[table_index] is not None:
                print("Enter the comma-separated indices of the columns to keep:")
                column_index = input()
                column_indices = [int(index.strip()) for index in column_index.split(',')]
                
                original_table = user_tables[table_index]
                new_table = []
                for row in original_table:
                    new_row = []
                    for i in column_indices:
                        new_row.append(row[i])
                    new_table.append(new_row)
                user_tables.append(new_table)
                break
            else:
                print("Incorrect table index. Try again.")
                continue

def delete_table():
    #Deletes a table by making its user_tables entry equal to None.

    while True:
            print("Choose a table index (for table deletion):")
            table_index = int(input())
            if 0 <= table_index < len(user_tables)and user_tables[table_index] is not None:
                deleted_tables.append((table_index, user_tables[table_index]))
                user_tables[table_index] = None
                break
            else:
                print("Incorrect table index. Try again.")
                continue

def delete_column():
    #Deletes a column from a selected table based on the column 
    #index provided by the user.
 
     while True:
            print("Choose a table index (for column deletion):")
            table_index = int(input())
            if 0 <= table_index < len(user_tables) and user_tables[table_index] is not None:     
                print("Enter the index of the column to delete:")
                col_index = int(input())
                if 0 <= col_index < len(user_tables[table_index][0]):
                    for row in user_tables[table_index]:
                        del row[col_index]
                break
            else:
                print("Incorrect table index. Try again.")
                continue

def restore_table():
    #Restores a deleted table from the list of deleted tables.

    while True:
            print("Choose a table index (for restoration):")
            table_index = int(input())
            if 0 <= table_index < len(user_tables):
                for index, table in deleted_tables:
                        if index == table_index:
                            user_tables[table_index] = table
                            deleted_tables.remove((index, table))
                break
            else:
                print("Incorrect table index. Try again.")
                continue

def main_menu():
    #Displays a menu for interacting with CSV tables and processes user choices.

    while True:
        print("""==================================
Enter your choice:
1. List tables.
2. Display table.
3. Duplicate table.
4. Create table.
5. Delete table.
6. Delete column.
7. Restore table.
0. Quit.
==================================""")
        user_choice = input()

        if user_choice == '1':
            list_tables()
        elif user_choice == '2':
            display_table()
        elif user_choice == '3':
            duplicate_table()
        elif user_choice == '4':
            create_table()
        elif user_choice == '5':
            delete_table()
        elif user_choice == '6':
            delete_column()
        elif user_choice == '7':
            restore_table()
        elif user_choice == '0':
            exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
