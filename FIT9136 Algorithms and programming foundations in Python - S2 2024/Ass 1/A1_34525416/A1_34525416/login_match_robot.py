"""
Writing a program that asks the user to enter a valid login. 
A valid login is a pair of username/password, where each username has a single password associated to it. 
If, after 3 tries, the user did not provide a correct login, the program asks whether they are a robot. 
If they are not a robot, the user is allowed 3 more tries. 
If they are a robot, the program terminates.
"""

#list of correct usernames and passwords from the question
correct_username = ['Ava','Leo','Raj','Zoe','Max','Sam','Eli','Mia','Ian','Kim']
correct_password = ['12345','abcde','pass1','qwert','aaaaa','zzzzz','11111','apple','hello','admin']

#Function to check the username and password from the question against the input from user:
def user_login():
        #using the variable tries to run the code thrice for a correct input
        tries = 3
        while tries != 0:
           input_username = input("Enter username: ")
           input_password = input("Enter password: ")
           #checking the username and password against every single variation of username and password match
           if (input_username == correct_username[0]) and (input_password == correct_password[0]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[1]) and (input_password == correct_password[1]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[2]) and (input_password == correct_password[2]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[3]) and (input_password == correct_password[3]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[4]) and (input_password == correct_password[4]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[5]) and (input_password == correct_password[5]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[6]) and (input_password == correct_password[6]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[7]) and (input_password == correct_password[7]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[8]) and (input_password == correct_password[8]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           elif (input_username == correct_username[9]) and (input_password == correct_password[9]) :
               print("Login successful. Welcome", input_username,"!")
               exit()
           else:
               #reducing the value of tries by 1 everytime an incorrect input is received
               tries-=1
               print("Login incorrect. Tries left:", tries)
        #Calling the function for checking whether user is a robot     
        robo_check()
        exit()
"""
This function checks the user input on the question: Are you a robot (Y/n)? 
and based on the input it returns to the user login function, exits the code or asks the same question again.
"""
def robo_check():
    robo ="n" 
    while robo == "n":
        robo=input("Are you a robot (Y/n)? ")
        if (robo == "n"):    
            user_login()
        elif(robo =="Y" or robo==""):
            exit()
        else:
            robo_check()

#calling the function user_login()
user_login()
