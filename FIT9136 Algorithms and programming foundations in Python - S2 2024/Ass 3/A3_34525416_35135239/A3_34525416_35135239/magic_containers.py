"""
This program manages a collection of containers and items, allowing 
the user to loot items and store them in various containers.
Containers can be standard, multi-compartment, or magic containers.
"""

import csv

# Class for a named and weighed item
class Item:
    """ 
    Depicts a thing with a weight and name.
    
    Qualities:
        name (str): The object's name.
        weight (int): The object's weight.
    """

    def __init__(self, name, weight):
        """ 
        Adds a name and weight to an item to initialize it.

        Arguments: 
            name (str): The item's name.
            weight (int): The object's weight.
        """
        self.name = name
        self.weight = weight

    def __str__(self):
        """ 
        Returns the item's string representation.

        Returns: str: A formatted string containing the item's name and weight.
        """
        return f"{self.name} (weight: {self.weight})"

# Standard container class
class Container:
    """ 
    Depicts a typical storage container with a weight and capacity restriction.
    
    Qualities:
        name (str): The container's name.
        empty_weight (int): The empty container's weight.
        Weight capacity (int): The utmost weight that the container is able to support.
        looted_items (list): the items that were stored in the container.
        current_weight (int): The container's weight as of right now.
    """

    def __init__(self, name, empty_weight, weight_capacity):
        """ 
        Sets up a container with a name, empty weight, and maximum weight.

        Args: 
            name (str): The container name.
            empty_weight (int): The empty container's weight.
            Weight capacity (int): The utmost weight that the container is able to support.
        """
        self.name = name
        self.empty_weight = empty_weight
        self.weight_capacity = weight_capacity
        self.looted_items = []
        self.current_weight = empty_weight  

    def add_item(self, item):
        """ 
        Attempts to fill the container with anything. determines if the item will fit based on the amount of space left.

        Args: item (Item): The object to be put in the container.

        Returns: bool: True in the event that the item was successfully added, False in all other cases.
        """
        if self.remaining_capacity() >= item.weight:
            self.looted_items.append(item)
            self.current_weight += item.weight  
            return True
        return False

    def remaining_capacity(self):
        """ 
        Determines the container's remaining capacity by weighing it at the moment.

        Returns: int: The container's remaining capacity 
        """
        return self.weight_capacity - (self.current_weight - self.empty_weight)

    def __str__(self):
        """ 
        Gives back a text representation of the looted objects and container.

        Returns: str: A formatted string containing the name, capacity, empty weight, 
        total weight, and items of the container.
        """
        result = (f"{self.name} (total weight: {self.current_weight}, "
                  f"empty weight: {self.empty_weight}, capacity: {self.current_weight - self.empty_weight}/{self.weight_capacity})")
        if self.looted_items:
            for item in self.looted_items:
                result += f"\n   {item}"  
        return result

# Multi-compartment container compartment class
class Compartment(Container):
    """ 
    Depicts a section inside a container with many sections.

    Takes over from the Container.
    """
    def __init__(self, name, empty_weight, weight_capacity):
        super().__init__(name, empty_weight, weight_capacity)

    def __str__(self):
        """ 
        Gives back a string representation of the plundered goods in the compartment.

        Returns: str: A formatted string containing the name, empty weight, capacity, 
        and contents of the compartment.
        """

        result = (f"{self.name} (total weight: {self.current_weight}, empty weight: {self.empty_weight}, "
                  f"capacity: {self.current_weight - self.empty_weight}/{self.weight_capacity})")
        for item in self.looted_items:
            result += f"\n      {item}"  
        return result

# Multi-compartment container class
class MultiCompartmentContainer(Container):
    """ 
    Depicts a container with several inside sections.

    Features: List of compartments within the container: compartments (list).
    """

    def __init__(self, name, compartments):
        """ 
        Sets the compartments of a multi-compartment container to their initial values.

        Args: 
            name (str): The container name.
            compartments (list): The container's list of compartments.
        """
        self.name = name
        self.compartments = compartments
        self.empty_weight = sum(compartment.empty_weight for compartment in compartments)
        self.weight_capacity = sum(compartment.weight_capacity for compartment in compartments)  # Sum of compartments' capacities
        self.current_weight = self.empty_weight

    def add_item(self, item):
        """ 
        Makes an effort to stuff anything into the first available compartment.

        Args: item (Item): The item that has to be added.

        Returns: bool: True in the event that the item was successfully added, 
        False in all other cases.
        """

        for compartment in self.compartments:
            if compartment.add_item(item):
                self.current_weight += item.weight
                return True
        return False

    def remaining_capacity(self):
        """ 
        Determines the amount of capacity left in each compartment.

        Returns: int: The total capacity left in each and every container.
        """
        return sum(compartment.remaining_capacity() for compartment in self.compartments)

    def __str__(self):
        """ 
        Displays the multi-compartment container and its compartments as a 
        string representation.

        Returns: str: A formatted string containing the name of the container, 
        its total weight, its empty weight, and its compartments.
        """
        result = (f"{self.name} (total weight: {self.current_weight}, "
                  f"empty weight: {self.empty_weight}, "
                  f"capacity: 0/0)")  
        for compartment in self.compartments:
            result += f"\n   {compartment}"  
        return result

# Magic container class
class MagicContainer(Container):
    """ 
    Depicts a magical container that doesn't gain weight when holding things.
    Comes from the Container by inheritance.
    """

    def __init__(self, name, empty_weight, weight_capacity):
        super().__init__(name, empty_weight, weight_capacity)  

    def add_item(self, item):
        """ Increases the capacity of the container without adding weight to it.

        Args: item (Item): The item that has to be added.

        Returns: bool: True in the event that the item was successfully added, 
        False in all other cases.
        """
        if self.remaining_capacity() >= item.weight:
            self.looted_items.append(item)
            return True  
        return False

    def add_container(self, container):
        """ 
        Inserts a new container into the magical container.

        Args: container (Container): The container to be added.

        Returns: bool: True in the event that the container was successfully added, 
        False in all other cases.
        """
        if self.remaining_capacity() >= container.current_weight:
            self.looted_items.append(container)
            return True
        return False

    def remaining_capacity(self):
        """ 
        Determines how much capacity is left depending on the things that are stored.

        Returns: int: The magic container's remaining capacity.
        """
        return self.weight_capacity - sum(item.weight for item in self.looted_items)

    def __str__(self):
        """
        Returns a string representation of the magic container and its looted items.

        Returns:
            str: A formatted string showing the container's name, empty weight, 
            capacity, and items.
        """
        result = (f"{self.name} (total weight: {self.empty_weight}, empty weight: {self.empty_weight}, "
                  f"capacity: {sum(item.weight for item in self.looted_items)}/{self.weight_capacity})")
        if self.looted_items:
            for item in self.looted_items:
                result += f"\n   {item}"  
        return result

# Function to read items from a CSV file
def read_items_from_csv(file_path):
    """
    Reads items from a CSV file and creates a list of Item objects.

    Args:
        file_path (str): The file path of the CSV file.

    Returns:
        list: A list of Item objects.
    """
    items = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            name, weight = row[0], row[1]
            try:
                items.append(Item(name, int(weight)))  
            except ValueError:
                print(f"Invalid weight '{weight}' for item '{name}'. Skipping.")
    return items

# Function to read standard containers from a CSV file
def read_containers_from_csv(file_path):
    """ 
    Builds a list of Container objects by reading containers from a CSV file.

    The arguments consist of the file path of the CSV file, file_path (str).

    List: An array of Container objects is returned.
    """
    containers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            name, empty_weight, weight_capacity = row[0], row[1], row[2]
            try:
                containers.append(Container(name, int(empty_weight), int(weight_capacity)))
            except ValueError:
                print(f"Invalid weights for container '{name}'. Skipping.")
    return containers

# Function to find a container by name
def find_container(containers, name):
    """
    Utilizes its name to locate a container

    Arguments: 
        containers (list): A list of objects that make up a container.
        name (str): The container's name that has to be located.

    Returns:
        Container: The found container, or None if not found.
    """
    for container in containers:
        if container.name.strip() == name.strip():
            return container
    return None

# Function to read multi-compartment containers from a CSV file
def read_multi_containers_from_csv(file_path, all_containers):
    """
    Reads multi-compartment containers from a CSV file and creates a list of MultiCompartmentContainer objects.

    Args:
        file_path (str): The file path of the CSV file.
        all_containers (list): List of all available containers for creating compartments.

    Returns:
        list: A list of MultiCompartmentContainer objects.
    """
    multi_containers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            name = row[0]  
            compartment_names = row[1:]  

            # Create compartments by finding corresponding containers from the full list
            compartments = []
            for compartment_name in compartment_names:
                compartment = find_container(all_containers, compartment_name.strip())
                if compartment:
                    compartments.append(Compartment(compartment.name, compartment.empty_weight, compartment.weight_capacity))

            multi_containers.append(MultiCompartmentContainer(name, compartments))

    return multi_containers

# Function to read magic containers from a CSV file
def read_magic_containers_from_csv(file_path, all_containers):
    """
    Reads magic containers from a CSV file and wraps them in a MagicContainer.

    Args:
        file_path (str): The file path of the CSV file.
        all_containers (list): List of all available containers.

    Returns:
        list: A list of MagicContainer objects.
    """
    magic_containers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            magic_container_name, base_container_name = row[0], row[1]
            # Find the base container and wrap it in a magic container
            base_container = find_container(all_containers, base_container_name)
            if base_container:
                # Magic containers should not increase weight when items are stored
                magic_container = MagicContainer(magic_container_name, base_container.empty_weight, base_container.weight_capacity)
                magic_containers.append(magic_container)
            else:
                print(f"Base container '{base_container_name}' not found for magic container '{magic_container_name}'.")
    return magic_containers


# Function to find an item by name
def find_item(items, name):
    """ Retrieves an item from a list by name.

    The arguments are: 
        items (list): A list of item objects.
        name (str): The object's name to be located.

    Returns: Item: The item that was located, or None in the event that it was not situated.
    """    
    for item in items:
        if item.name == name:
            return item
    return None

# Main function
def main():
    """ Primary function in charge of managing program flow.

    Reads items and containers from CSV files, presents a menu to 
    list looted objects in the chosen container, and lets the user choose which 
    container to use.
    """

    # Read items and containers from CSV files
    items = read_items_from_csv('items.csv')
    containers = read_containers_from_csv('containers.csv')
    multi_containers = read_multi_containers_from_csv('multi_containers.csv', containers)
    
    # Combine both single and multi-compartment containers
    all_containers = containers + multi_containers

    # Now read magic containers with all_containers passed as an argument
    magic_containers = read_magic_containers_from_csv('magic_containers.csv', all_containers)  
    
    # Add magic containers to all containers
    all_containers += magic_containers

    # Count the total items and containers
    total_items = len(items)
    total_containers = len(all_containers)

    print(f"Initialised {total_items + total_containers} items including {total_containers} containers.\n")

    selected_container = None

    # Ask for the container name
    while selected_container is None:
        container_name = input("Enter the name of the container: ")
        selected_container = find_container(all_containers, container_name)
        if selected_container is None:
            print(f'"{container_name}" not found. Try again.')

    # Menu logic
    while True:
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")
        choice = input()

        if choice == "1":
            item_name = input("Enter the name of the item: ")
            item = find_item(items, item_name)

            if item:
                if selected_container.add_item(item):
                    print(f'Success! Item "{item.name}" stored in container "{selected_container.name}".')
                else:
                    print(f'Failure! Item "{item.name}" NOT stored in container "{selected_container.name}".')
            else:
                print(f'Item "{item_name}" not found.')

        elif choice == "2":
            print(selected_container)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

