"""
This program that asks the user to enter a valid username and a valid password. 
A successful login occurs when the user enters one of the correct usernames and one of the correct passwords. 
If after 3 tries, the user did not provide a correct login, the program terminates.
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
        if (input_username in correct_username) and (input_password in correct_password) :
            print("Login successful. Welcome", input_username,"!")
            break
        else:
            #reducing the value of tries by 1 everytime an incorrect input is received
            tries-=1
            print("Login incorrect. Tries left:", tries)

# calling the function
user_login()
