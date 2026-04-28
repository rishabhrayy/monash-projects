"""
This is a program that asks the user to input a string, 
then choose a keyboard, 
then plans the actions of Robbie the robot so that it can type this string on a keyboard.
It uses the concept of checking the length of all the outputs to check for the most optimal position
"""
# Asking user to provide a string which Robbie has to type:
robbie_string = input("Enter a string to type: ")

"""
Here I have used the same concept as the previous task.
Making 4 different functions for each of the keyboard configuration given to us.
"""

def config_0():
    keyboard0 = ["abcdefghijklm", 
            "nopqrstuvwxyz"]
    cur_row = 0 
    cur_col = 0

    robbie_movement = ""

    can_type = True

    for char in robbie_string:
        search_row = 0 
        found = False
        
        for row in keyboard0:
            if char in row:
                new_row = search_row
                new_col = row.index(char)
                found = True
                break
            search_row += 1

        if found:
            if cur_col < new_col:
                robbie_movement += 'r' * (new_col - cur_col)
            elif cur_col > new_col:
                robbie_movement += 'l' * (cur_col - new_col)
            
            if cur_row < new_row:
                robbie_movement += 'd' * (new_row - cur_row)
            elif cur_row > new_row:
                robbie_movement += 'u' * (cur_row - new_row)
            
            robbie_movement += 'p'
            
            cur_row = new_row
            cur_col = new_col
        else:
            can_type = False
            break

    if can_type:
        return robbie_movement
    else:
        return False

def config_1():
    keyboard = ["789",
            "456",
            "123",
            "0.-"]

    cur_row = 0 
    cur_col = 0

    robbie_movement = ""

    can_type = True

    for char in robbie_string:
        search_row = 0 
        found = False
        
        for row in keyboard:
            if char in row:
                new_row = search_row
                new_col = row.index(char)
                found = True
                break
            search_row += 1

        if found:
            if cur_col < new_col:
                robbie_movement += 'r' * (new_col - cur_col)
            elif cur_col > new_col:
                robbie_movement += 'l' * (cur_col - new_col)
            
            if cur_row < new_row:
                robbie_movement += 'd' * (new_row - cur_row)
            elif cur_row > new_row:
                robbie_movement += 'u' * (cur_row - new_row)
            
            robbie_movement += 'p'
            
            cur_row = new_row
            cur_col = new_col
        else:
            can_type = False
            break

    if can_type:
        return robbie_movement
    else:
        return False


def config_2():
    keyboard = ["chunk",
                "vibex",
                "gymps",
                "fjord",
                "waltz"]

    cur_row = 0 
    cur_col = 0

    robbie_movement = ""

    can_type = True

    for char in robbie_string:
        search_row = 0 
        found = False
        
        for row in keyboard:
            if char in row:
                new_row = search_row
                new_col = row.index(char)
                found = True
                break
            search_row += 1

        if found:
            if cur_col < new_col:
                robbie_movement += 'r' * (new_col - cur_col)
            elif cur_col > new_col:
                robbie_movement += 'l' * (cur_col - new_col)
            
            if cur_row < new_row:
                robbie_movement += 'd' * (new_row - cur_row)
            elif cur_row > new_row:
                robbie_movement += 'u' * (cur_row - new_row)
            
            robbie_movement += 'p'
            
            cur_row = new_row
            cur_col = new_col
        else:
            can_type = False
            break

    if can_type:
        return robbie_movement
    else:
        return False


def config_3():
    keyboard = ["bemix",
                "vozhd",
                "grypt",
                "clunk",
                "waqfs"]

    cur_row = 0 
    cur_col = 0

    robbie_movement = ""

    can_type = True

    for char in robbie_string:
        search_row = 0 
        found = False
        
        for row in keyboard:
            if char in row:
                new_row = search_row
                new_col = row.index(char)
                found = True
                break
            search_row += 1

        if found:
            if cur_col < new_col:
                robbie_movement += 'r' * (new_col - cur_col)
            elif cur_col > new_col:
                robbie_movement += 'l' * (cur_col - new_col)
            
            if cur_row < new_row:
                robbie_movement += 'd' * (new_row - cur_row)
            elif cur_row > new_row:
                robbie_movement += 'u' * (cur_row - new_row)
            
            robbie_movement += 'p'
            
            cur_row = new_row
            cur_col = new_col
        else:
            can_type = False
            break

    if can_type:
        return robbie_movement
    else:
        return False
    
"""
Now I have called and compared the outputs from each required function as per the input by user for Robbie to type:
"""
   

keyb0 = config_0()
keyb1 = config_1()
keyb2 = config_2()
keyb3 = config_3()

#If all keyboards return false input then send the error message
if (keyb0 == False and keyb1 == False and keyb2 == False and keyb3 == False):
    print("The string cannot be typed out.")
    #If keyb1 has an output we know that the input is numeric and we call that keyboard:
if keyb1:
    out1 = '''Configuration used:
-------
| 789 |
| 456 |
| 123 |
| 0.- |
-------
The robot must perform the following operations:'''
    print(out1)
    print(keyb1)
    exit()
#As identified in the question if there is a 'j' in the input then keyboard configuration 3 will not be called as it does not have character 'j'
elif 'j' in robbie_string:
    keyb0 = config_0()
    keyb2 = config_2()
    #comparing the value of both outputs of keyboard config 0 and config 2
    if len(keyb0) <= len(keyb2):
        out0 = '''Configuration used:
-----------------
| abcdefghijklm |
| nopqrstuvwxyz |
-----------------
The robot must perform the following operations:'''
        print(out0)
        print(keyb0)    

    else:
        out2 = '''Configuration used:
---------
| chunk |
| vibex |
| gymps |
| fjord |
| waltz |
---------
The robot must perform the following operations:'''
        print(out2)
        print(keyb2)
#As identified in the question if there is a 'q' in the input then keyboard configuration 2 will not be called as it does not have character 'q'
elif 'q' in robbie_string:
    keyb0 = config_0()
    keyb3 = config_2()
     #comparing the value of both outputs of keyboard config 0 and config 3
    if len(keyb0) <= len(keyb3):
        out0 = '''Configuration used:
-----------------
| abcdefghijklm |
| nopqrstuvwxyz |
-----------------
The robot must perform the following operations:'''
        print(out0)
        print(keyb0)    

    else:
        out3 = '''Configuration used:
---------
| bemix |
| vozhd |
| grypt |
| clunk |
| waqfs |
---------
The robot must perform the following operations:'''
        print(out3)
        print(keyb3)

#Checking for the rest of the cases when all configs are true
elif (keyb0 and keyb2 and keyb3):
    #Checking the lenght of all the outputs when condition is true:
    if len(keyb0) <= len(keyb2) and len(keyb0) <= len(keyb3):
        out0 = '''Configuration used:
-----------------
| abcdefghijklm |
| nopqrstuvwxyz |
-----------------
The robot must perform the following operations:'''
        print(out0)
        print(keyb0)    

    elif len(keyb2) <= len(keyb0) and len(keyb2) <= len(keyb3):
        out2 = '''Configuration used:
---------
| chunk |
| vibex |
| gymps |
| fjord |
| waltz |
---------
The robot must perform the following operations:'''
        print(out2)
        print(keyb2)

    elif len(keyb3) <= len(keyb0) and len(keyb3) <= len(keyb2):
        out3 = '''Configuration used:
---------
| bemix |
| vozhd |
| grypt |
| clunk |
| waqfs |
---------
The robot must perform the following operations:'''
        print(out3)
        print(keyb3)

else:
    out0 = '''Configuration used:
-----------------
| abcdefghijklm |
| nopqrstuvwxyz |
-----------------
The robot must perform the following operations:'''
    print(out0)
    print(keyb0)
