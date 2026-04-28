rabbit = {} 
def create_rabbit():
    #Asks the application user for rabbit name and then add that to only 'rabbit' db. 
    #The function will return a warning to the user that this name is already used and ask for another one. 
    #After typing one unique naming, it adds this name in dictionary rabbit like Key=>Value "Unknown". 
    #The iterations of this process carries on until a unique name is given. 
    #The assumes rabbit is a built-in dictionary 
        while True:
            name = input("Input the new rabbit's name:\n")
            if name in rabbit:
                print("That name is already in the database.")
            else:
                rabbit[name] = "Unknown"  
                break

def input_rabbit_age():
    #The user is asked to input a rabbit's name and update its age in a predefined 'rabbit' dictionary, 
    #if found, the user is notified and asked to enter age.
    
        while True:
            name = input("Input the rabbit's name:\n")
            if name in rabbit:
                rab_age = input(f"Input {name}'s age:\n")
                rabbit[name] = rab_age
                break
            else:
                print("That name is not in the database.")
                
def list_rabbits():
    #The function iterates through the dictionary displaying the name and age of each rabbit.
        print("Rabbytes:")
        for name, age in rabbit.items():
            print(f"{name} ({age})")

def main_menu():
    #shows the main menu and allows the user to enter commands to manipulate the 'rabbit' database.
    #You can create a rabbit, enter a rabbit's age, see a list of all the rabbits, or exit the menu.
    #based on user input, calls the relevant function and continues until the user decides to stop.

        while True:
            print("""==================================
Enter your choice:
1. Create a Rabbit.
2. Input Age of a Rabbit.
3. List Rabbytes.
0. Quit.
==================================""")
            user_input = input()

            if user_input == '1':
                create_rabbit()
            elif user_input == '2':
                input_rabbit_age()
            elif user_input == '3':
                list_rabbits()
            elif user_input == '0':
                break
            else:
                print("Invalid choice. Please try again.")

main_menu()
