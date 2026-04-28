"""
A program that reads items and containers from files items.csv and containers.csv, 
and ask the user for a container to pick for the adventure. 
Also multi_containers.csv, now provides the description of containers that have multiple compartments, 
each behaving like an independent container. 
"""

import csv

# Class representing an item with a name and weight
class Item:
    """
    Represents an item with a name and weight.
    """
    def __init__(self, name, weight):
        """
        Initializes an item with a name and weight.
        name: The name of the item.
        weight: The weight of the item.
        """
        self.name = name
        self.weight = weight

    def __str__(self):
        """
        Returns a string representation of the item.
        Returns a string displaying the item's name and weight.
        """
        return f"{self.name} (weight: {self.weight})"


# Standard container class
class Container:
    """
    Represents a container with a name, empty weight, and weight capacity.
    """
    def __init__(self, name, empty_weight, weight_capacity):
        """
        Initializes a container.
        name: The name of the container.
        empty_weight: The empty weight of the container.
        weight_capacity: The total weight capacity of the container.
        """
        self.name = name
        self.empty_weight = empty_weight
        self.weight_capacity = weight_capacity
        self.looted_items = []
        self.current_weight = empty_weight  # Starts with the container's empty weight

    def add_item(self, item):
        """
        Adds an item to the container if it can fit based on the remaining capacity.
        item: The item to be added.
        Returns True if the item was added, False otherwise.
        """
        # Check if the item can fit based on the remaining capacity
        if self.remaining_capacity() >= item.weight:
            self.looted_items.append(item)
            self.current_weight += item.weight  # Update current weight with the item's weight
            return True
        return False

    def remaining_capacity(self):
        """
        Calculates the remaining capacity of the container.
        Returns the remaining capacity of the container.
        """
        # Calculate remaining capacity as total capacity minus current weight (excluding empty weight)
        return self.weight_capacity - (self.current_weight - self.empty_weight)

    def __str__(self):
        """
        Returns a string representation of the container and its looted items.
        Returns a string displaying the container's details and its items.
        """
        result = (f"{self.name} (total weight: {self.current_weight}, "
                  f"empty weight: {self.empty_weight}, "
                  f"capacity: {self.current_weight - self.empty_weight}/{self.weight_capacity})")
        if self.looted_items:
            for item in self.looted_items:
                result += f"\n   {item}"  # Indent the items properly
        return result


# Compartment class for multi-compartment containers
class Compartment(Container):
    """
    Represents a compartment that inherits from the Container class.
    """
    def __init__(self, name, empty_weight, weight_capacity):
        """
        Initializes a compartment.
        name: The name of the compartment.
        empty_weight: The empty weight of the compartment.
        weight_capacity: The total weight capacity of the compartment.
        """
        super().__init__(name, empty_weight, weight_capacity)

    def __str__(self):
        """
        Returns a string representation of the compartment.
        Returns a string displaying the compartment's details and its items.
        """
        result = (f"{self.name} (total weight: {self.current_weight}, "
                  f"empty weight: {self.empty_weight}, "
                  f"capacity: {self.current_weight - self.empty_weight}/{self.weight_capacity})")
        for item in self.looted_items:
            result += f"\n      {item}"  # Indent the items further for compartments
        return result


# Multi-compartment container class
class MultiCompartmentContainer(Container):
    """
    Represents a container with multiple compartments.
    """
    def __init__(self, name, compartments):
        """
        Initializes a multi-compartment container.
        name: The name of the multi-compartment container.
        compartments: A list of compartments that make up the container.
        """
        self.name = name
        self.compartments = compartments
        # Calculate empty weight as the sum of all compartments' empty weights
        self.empty_weight = sum(compartment.empty_weight for compartment in compartments)
        # Calculate total weight capacity as the sum of all compartments' capacities
        self.weight_capacity = sum(compartment.weight_capacity for compartment in compartments)
        self.current_weight = self.empty_weight

    def add_item(self, item):
        """
        Adds an item to the first compartment with enough capacity.
        item: The item to be added.
        Returns True if the item was added, False otherwise.
        """
        for compartment in self.compartments:
            # Attempt to add the item to each compartment
            if compartment.add_item(item):
                self.current_weight += item.weight  # Update the total weight of the multi-compartment container
                return True
        return False

    def remaining_capacity(self):
        """
        Calculates the remaining capacity of the entire multi-compartment container.
        Returns the total remaining capacity of all compartments.
        """
        # Total remaining capacity is the sum of all compartments' remaining capacities
        return sum(compartment.remaining_capacity() for compartment in self.compartments)

    def __str__(self):
        """
        Returns a string representation of the multi-compartment container.
        Returns a string displaying the container's details and its compartments.
        """
        result = (f"{self.name} (total weight: {self.current_weight}, "
                  f"empty weight: {self.empty_weight}, "
                  f"capacity: 0/0)")
        for compartment in self.compartments:
            result += f"\n   {compartment}"  # Indented for compartments
        return result


# Function to read items from a CSV file
def read_items_from_csv(file_path):
    """
    Reads items from a CSV file and returns a list of Item objects.
    file_path: The path to the CSV file containing item data.
    Returns a list of Item objects.
    """
    items = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            name, weight = row[0], row[1]
            try:
                items.append(Item(name, int(weight)))  # Convert weight to integer and create Item object
            except ValueError:
                print(f"Invalid weight '{weight}' for item '{name}'. Skipping.")
    return items


# Function to read standard containers from a CSV file
def read_containers_from_csv(file_path):
    """
    Reads standard containers from a CSV file and returns a list of Container objects.
    file_path: The path to the CSV file containing container data.
    Returns a list of Container objects.
    """
    containers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            name, empty_weight, weight_capacity = row[0], row[1], row[2]
            try:
                containers.append(Container(name, int(empty_weight), int(weight_capacity)))  # Create Container object
            except ValueError:
                print(f"Invalid weights for container '{name}'. Skipping.")
    return containers


# Function to find a container by name
def find_container(containers, name):
    """
    Finds and returns a container by name from a list of containers.
    containers: A list of Container objects.
    name: The name of the container to find.
    Returns the Container object with the matching name, or None if not found.
    """
    for container in containers:
        if container.name.strip() == name.strip():
            return container
    return None


# Function to read multi-compartment containers from a CSV file
def read_multi_containers_from_csv(file_path, all_containers):
    """
    Reads multi-compartment containers from a CSV file.
    file_path: The path to the CSV file containing multi-container data.
    all_containers: A list of all containers to find the compartments from.
    Returns a list of MultiCompartmentContainer objects.
    """
    multi_containers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            name = row[0]  # Multi-compartment container name
            compartment_names = row[1:]  # Names of compartments in this container

            compartments = []
            for compartment_name in compartment_names:
                compartment = find_container(all_containers, compartment_name.strip())
                if compartment:
                    compartments.append(Compartment(compartment.name, compartment.empty_weight, compartment.weight_capacity))

            multi_containers.append(MultiCompartmentContainer(name, compartments))

    return multi_containers


# Function to find an item by name
def find_item(items, name):
    """
    Finds and returns an item by name from a list of items.
    items: A list of Item objects.
    name: The name of the item to find.
    Returns the Item object with the matching name, or None if not found.
    """
    for item in items:
        if item.name == name:
            return item
    return None


# Main function
def main():
    """
    Main function to execute the container and item management program.
    """
    # Read items and containers from CSV files
    items = read_items_from_csv('items.csv')
    containers = read_containers_from_csv('containers.csv')
    multi_containers = read_multi_containers_from_csv('multi_containers.csv', containers)

    # Combine both single and multi-compartment containers
    all_containers = containers + multi_containers

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

    # Menu logic for user interaction
    while True:
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")

        choice = input().strip()

        if choice == "1":
            while True:
                item_name = input("Enter the name of the item: ")
                item = find_item(items, item_name)

                if item is None:
                    print(f'"{item_name}" not found. Try again.')
                else:
                    # Attempt to add the item to the selected container
                    if selected_container.add_item(item):
                        print(f'Success! Item "{item_name}" stored in container "{selected_container.name}".')
                    else:
                        print(f'Failure! Item "{item_name}" NOT stored in container "{selected_container.name}".')
                    break

        elif choice == "2":
            # Print details of looted items in the selected container
            print(f"{selected_container}")

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

