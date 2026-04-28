"""
A program that reads items and containers from files items.csv and containers.csv, 
and ask the user for a container to pick for the adventure.
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
        """
        self.name = name
        self.weight = weight

    def __str__(self):
        """
        Returns a string representation of the item.
        """
        return f"{self.name} (weight: {self.weight})"


# Class representing a standard container
class Container:
    """
    Represents a container with a name, empty weight, and weight capacity.
    """
    def __init__(self, name, empty_weight, weight_capacity):
        """
        Initializes a container.
        """
        self.name = name
        self.empty_weight = empty_weight
        self.weight_capacity = weight_capacity
        self.looted_items = []
        self.current_weight = empty_weight  # Starts with the container's empty weight

    def add_item(self, item):
        """
        Adds an item to the container if it can fit based on the remaining capacity.
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
        """
        # Calculate remaining capacity as total capacity minus current weight (excluding empty weight)
        return self.weight_capacity - (self.current_weight - self.empty_weight)

    def __str__(self):
        """
        Returns a string representation of the container and its looted items.
        """
        result = (f"{self.name} (total weight: {self.current_weight}, "
                  f"empty weight: {self.empty_weight}, "
                  f"capacity: {self.current_weight - self.empty_weight}/{self.weight_capacity})")
        if self.looted_items:
            for item in self.looted_items:
                result += f"\n   {item}"  # Indent the items properly
        return result


# Function to read items from a CSV file
def read_items_from_csv(file_path):
    """
    Reads items from a CSV file and returns a list of Item objects.
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
    """
    for container in containers:
        if container.name == name:
            return container
    return None


# Function to find an item by name
def find_item(items, name):
    """
    Finds and returns an item by name from a list of items.
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
    items = read_items_from_csv('items.csv')
    containers = read_containers_from_csv('containers.csv')

    selected_container = None

    # Ask for the container name
    print(f"Initialised {len(items) + len(containers)} items including {len(containers)} containers.\n")

    while selected_container is None:
        container_name = input("Enter the name of the container: ")
        selected_container = find_container(containers, container_name)
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

