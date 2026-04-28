rabbit = {}
parent = {}
kitten = {}

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
    #The user is asked to input a rabbit's name and update its age in a predefined 'rabbit' database, 
    #if found, the user is notified and prompted.

    while True:
        name = input("Input the rabbit's name:\n")
        if name in rabbit:
            rab_age = input(f"Input {name}'s age:\n")
            rabbit[name] = rab_age
            break
        else:
            print("That name is not in the database.\n")

def list_rabbits():
    #The function presume the 'rabbit' dictionary is predefined, 
    #iterates through the dictionary displaying the name and age of each rabbit, and returns None.
    print("Rabbytes:")
    for name, age in rabbit.items():
        print(f"{name} ({age})")

def create_parent():
    
    #'parent' and 'rabbit' databases are expanded to include a parent rabbit and its kitten.
    #Asks the user to provide the name of their kitten and parent. adds the parent and its kitten to the 
    #dictionary definition of "parent." 
    #Verifies that both names have the age "Unknown" in the "rabbit" database. 
    #Refreshes the dictionary entry for "kitten" to link the kitten to its parent. 
    #Assumes that the dictionaries for "parent," "rabbit," and "kitten" are preset and returns None.
    
    while True:
        par_name = input("Input the parent's name:\n")
        if par_name not in parent:
            parent[par_name] = []
        kitten_name = input("Input the kitten's name:\n")
        parent[par_name].append(kitten_name)

        if par_name not in rabbit:
            rabbit[par_name] = "Unknown"
        if kitten_name not in rabbit:
            rabbit[kitten_name] = "Unknown"
        if kitten_name not in kitten:
            kitten[kitten_name] = []
        kitten[kitten_name].append(par_name)
        break

def list_family():
    
    #lists the parents and kittens in the family of a given rabbit that has been found in the database.
    #asks the user to name a rabbit and shows the rabbit's parents and kittens. 
    #The user is prompted once more if the name cannot be located in the "rabbit" database. 
    #assumes that the dictionaries for "parent," "kitten," and "rabbit" are preset and returns None.
    
    while True:
        rab_name = input("Input the rabbit's name:\n")
        if rab_name not in rabbit:
            print("That name is not in the database.")
            continue

        print(f"Parents of {rab_name}:")
        if rab_name in kitten:
            for parent_name in sorted(kitten[rab_name]):
                print(parent_name)

        print(f"Kittens of {rab_name}:")
        if rab_name in parent:
            for kitten_name in sorted(parent[rab_name]):
                print(kitten_name)
        break

def find_cousins():
    
    #Searches the database for a given rabbit's cousins and displays them.
    #asks the user to name a rabbit and uses the relationship between 
    #the rabbit's parents and grandparents to determine its cousins. 
    #The user is prompted again if the name cannot be located in the "rabbit" database. 
    #assumes that the dictionaries for "parent," "kitten," and "rabbit" are preset.

    #Returns: None 
    
    while True:
        rab_name = input("Input the rabbit's name:\n")
        if rab_name not in rabbit:
            print("That name is not in the database.")
            continue

        print(f"Cousins of {rab_name}:")
        cousins = []  
        if rab_name in kitten:
            parents = kitten[rab_name]  

            for parent_name in parents:
                if parent_name in kitten:
                    grandparents = kitten[parent_name]  
                    for grandparent in grandparents:
                        if grandparent in parent:
                            siblings = parent[grandparent]  

                            for sibling in siblings:
                                if sibling != parent_name: 
                                    if sibling in parent:
                                        for cousin in parent[sibling]:
                                            if cousin != rab_name and cousin not in cousins: 
                                                cousins.append(cousin)

        
        if cousins:
            for cousin_name in cousins:
                print(cousin_name)
        break


def main_menu():
    
    #Shows the main menu, accepts user input, and runs commands on the 'rabbit' database.
    #A rabbit can be created, its age can be entered, it can list all rabbits, 
    #it can establish a parental relationship, it can list its immediate family, 
    #it can locate its cousins, or it can be quit. 
    #calls the relevant function in accordance with the user's selection and keeps going until 
    #the user decides to stop.

    #Returns: None
    
    while True:
        print("""==================================
Enter your choice:
1. Create a Rabbit.
2. Input Age of a Rabbit.
3. List Rabbytes.
4. Create a Parental Relationship.
5. List Direct Family of a Rabbit.
6. Find Cousins of a Rabbit.
0. Quit.
==================================""")
        user_input = input()

        if user_input == '1':
            create_rabbit()
        elif user_input == '2':
            input_rabbit_age()
        elif user_input == '3':
            list_rabbits()
        elif user_input == '4':
            create_parent()
        elif user_input == '5':
            list_family()
        elif user_input == '6':
            find_cousins()    
        elif user_input == '0':
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()
