import keyword
import re

def print_program(program):
    #Outputs every line in the provided Python program.
    print("Program:")
    for line in program:
        print(line)

def list_variables(program):
    #Pulls variable names out of the specified Python program and prints them.
    variables = set()
    keywords = keyword.kwlist

    pattern = re.compile(r'\b[a-zA-Z_]\w*\b')

    for line in program:
        words = pattern.findall(line)
        for word in words:
            if word.isidentifier() and word not in keywords:
                variables.add(word)

    sorted_variables = sorted(variables)
    print("Variables:")
    for var in sorted_variables:
        print(var)
    return sorted_variables

def format_variables_to_snake_case(var_name):
    #Changes the value of a supplied variable name to snake case.
    #Uses the regex substitute library to format the variable 

    return re.sub(r'(?<!^)(?=[A-Z])', '_', var_name).lower()

def replace_variable_in_program(program, old_var, new_var):
    #Updates program variables by adding new variable names when existing ones are found.
    #Uses the regex compile library to format the variable and append it to the new program list
    new_program = []
    pattern = re.compile(rf'\b{re.escape(old_var)}\b')
    for line in program:
        new_program.append(pattern.sub(new_var, line))
    return new_program

def main():
    #The primary purpose is to communicate with the user and carry out 
    #actions on a Python program.
    #builds a program using user input and gives the user the ability to 
    #list variables, format variables to snake_case, replace variables, and print the program.

    program = []
    print("Enter the Python program to analyze, line by line. Enter 'end' to finish.")
    while True:
        line = input()
        if line == 'end':
            break
        program.append(line)
    
    while True:
        print("==================================")
        print("Enter your choice:")
        print("1. Print program.")
        print("2. List.")
        print("3. Format.")
        print("0. Quit.")
        print("==================================")
        
        choice = input()
        if choice == '1':
            print_program(program)
        elif choice == '2':
            variables = list_variables(program)
        elif choice == '3':
            variables = set()
            keywords = keyword.kwlist

            # Regular expression to match valid variable names        
            pattern = re.compile(r'\b[a-zA-Z_]\w*\b')
            
            # This loop is used to extract variables from the program
            for line in program:
                words = pattern.findall(line)
                for word in words:
                    if word.isidentifier() and word not in keywords:
                        variables.add(word)
            # If no variables are found, prompt the user and continue  
            if not variables:
                print("No variables found to format.")
                continue
            # Loop to prompt the user to pick a variable to format
            while True:
                print("Pick a variable:")  
                var_choice = input()
                if var_choice in variables:
                    new_var = format_variables_to_snake_case(var_choice)
                    program = replace_variable_in_program(program, var_choice, new_var)
                    break
                else:
                    print("This is not a variable name.")


        elif choice == '0':
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 0.")

if __name__ == "__main__":
    main()

