# Create a hash table object that will store all the packages
class HashTable:  # O(n) complexity
    # Create the hash table, using a list, to hold each package object
    def __init__(self, size=200):  # O(n) complexity
        self.list = []
        for i in range(size):
            self.list.append([])

    # Add a new package object to the hash table with the Package ID as the key
    def insert(self, key, value):  # O(n) complexity
        # Built-in Python hash function used on key to get the index of the hash table to store the package object in
        index = hash(key) % len(self.list)

        if self.list[index] is None:  # If a package object with that Package ID is not in the hash table yet then add it
            self.list[index] = list([[key, value]])
            return True
        else:  # If a package object with that Package ID is already in the hash table then update it
            for pair in self.list[index]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.list[index].append([key, value])
            return True

    # Find a package object within the hash table based on the inputted Package ID as the key
    def search(self, key):  # O(n) complexity
        index = hash(key) % len(self.list)
        if self.list[index] is not None:  # Check to see if that Package ID is in the hash table
            for pair in self.list[index]:
                if pair[0] == key:
                    return pair[1]
        return None  # If that package ID is not in the hash table then return none

    # Print everything contained in the hash table
    def print(self):  # O(n) complexity
        for item in self.list:
            if item is not None:
                print(str(item))
