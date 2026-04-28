import keyword

def get_input():
    #Gathers several lines of user input to create a Python application.
    #requests that the user type each line of code individually. 
    #The user types 'end' to conclude the input collection.
    #gives back a list of strings, each of which corresponds to a line from the input program.
    
    print("Enter the Python program to analyze, line by line. Enter 'end' to finish.")
    user_input_program = []
    
    while True:
        program_lines = input()
        if program_lines.lower() == 'end':
            break
        user_input_program.append(program_lines)

    return user_input_program

def print_program(user_input_program):
    #From a collection of strings, prints every line of a Python program.

    print("Program:")
    for line in user_input_program:
        print(line)

def list_variables(user_input_program):
    #pulls the variable names out of a list of Python code lines and prints them.
    python_keywords = set(keyword.kwlist)
    variables = set()
    
    for line in user_input_program:
        words = line.split()       
        for word in words:
            clean_word = word.strip("()[]{}.,:;+-*/=<>!&|^~%@#")            
            if clean_word and clean_word[0].isalpha() and clean_word not in python_keywords:
                variables.add(clean_word)
    
    sorted_variables = sorted(variables)   
    print("Variables:")
    for var in sorted_variables:
        print(var)

def main_menu():
    #Shows a menu that allows the user to interact with a Python program.
    #gives the user the option to print the 
    #complete program or a list of the variable names that were taken out of it. 
    #Until the user selects to close it, the menu will remain visible.

    entered_program = get_input()
    while True:
        print("""==================================
Enter your choice:
1. Print program.
2. List.
0. Quit.
==================================""")
        menu_choice = int(input())
    
        if menu_choice == 1:
            print_program(entered_program)
        elif menu_choice == 2:
            list_variables(entered_program)
        elif menu_choice == 0:
            exit()


main_menu()
