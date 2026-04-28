"""
This is a program that asks the user to input a string, 
and then plans the actions of Robbie the robot so that it can type this string on a keyboard.
It uses the current location of robbie and the previous location to check the movement
"""
# Inputting the keyboard as provided in the question:
keyboard = ["abcdefghijklm", 
            "nopqrstuvwxyz"]

# Asking user to provide a string which Robbie has to type:
robbie_string = input("Enter a string to type: ")

# Using the current position of Robbie as (0, 0) which is for 'a'
cur_row = 0 
cur_col = 0

# Using a variable to track Robbie's movement from current position to new position
robbie_movement = ""

# Another variable to track if the string can be typed on the given keyboard in question
can_type = True

# Using a for loop to go through all the characters in the string input by the user
for char in robbie_string:
    # Initially looking for the character in the first row
    search_row = 0 
    # Using found variable as an indicator when the character is found on the keyboard
    found = False
    #using a nested for loop to check for the character in both rows:
    for row in keyboard:
        if char in row:
            # If the character is found, store the new index value of row and column
            new_row = search_row
            new_col = row.index(char)
            found = True
            break
        # Move to the next row if the character is not found in the current row
        else:
            search_row += 1

    # If the character was found, plan Robbie's movement
    if found == True:
        # Move horizontally first (first right then left)
        if cur_col < new_col:
            robbie_movement += 'r' * (new_col - cur_col)
        elif cur_col > new_col:
            robbie_movement += 'l' * (cur_col - new_col)
        
        # Move vertically next (first up and then down)
        if cur_row < new_row:
            robbie_movement += 'd' * (new_row - cur_row)
        elif cur_row > new_row:
            robbie_movement += 'u' * (cur_row - new_row)
        
        # Press the key whenever a key is found after going through if...elif condition
        robbie_movement += 'p'
        
        # Update Robbie's new position to the current position
        cur_row = new_row
        cur_col = new_col
    else:
        can_type = False
        break

# Final output based on whether the string can be fully typed or not
if can_type:
    print("The robot must perform the following operations:")
    print(robbie_movement)
else:
    print("The string cannot be typed out.")

