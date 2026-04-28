"""
A program that reads items and containers from files items.csv and containers.csv, 
and prints the list of items.
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


# Standard container class
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
        if self.remaining_capacity() >= item.weight:
            self.looted_items.append(item)
            self.current_weight += item.weight  # Update current weight with the item's weight
            return True
        return False

    def remaining_capacity(self):
        """
        Calculates the remaining capacity of the container.
        """
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


# Main function
def main():
    """
    Main function to execute the container and item management program.
    """
    items = read_items_from_csv('items.csv')
    containers = read_containers_from_csv('containers.csv')

    # Sort items and containers alphabetically by name
    items_sorted = sorted(items, key=lambda item: item.name)
    containers_sorted = sorted(containers, key=lambda container: container.name)

    total_items = len(items_sorted) + len(containers_sorted)
    print(f"Initialised {total_items} items including {len(containers_sorted)} containers.\n")

    print("Items:")
    for item in items_sorted:
        print(f"{item}")

    print("\nContainers:")
    for container in containers_sorted:
        print(f"{container}")
    print()

if __name__ == "__main__":
    main()

