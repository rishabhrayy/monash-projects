"""
This program that asks the user to enter a username. 
A successful login occurs when the user enters one of the valid usernames.
"""

#list of correct usernames from the question
correct_username = ['Ava','Leo','Raj','Zoe','Max','Sam','Eli','Mia','Ian','Kim']

#function to check for the correct Username:
def user_login():
    #using while true condition to keep promting the user until a valid username is provided
    while True:
        input_username = input("Enter username: ")

        if input_username in correct_username :
            print("Login successful. Welcome", input_username,"!")
            break
        else:
            print("Login incorrect.")
#Calling the function:
user_login()
