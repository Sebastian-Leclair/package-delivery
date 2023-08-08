import datetime
import csv

from HashTable import HashTable
from Package import Package
from Truck import Truck

# The first step is to read the data from the csv files and store it for later use

# Read the Distances.csv file and store the information in the list distance_data
with open("Distances.csv") as distances:  # O(1) complexity
    distance_data = csv.reader(distances, delimiter=",")
    distance_data = list(distance_data)

# Read the Addresses.csv file and store the information in the list address_data
with open("Addresses.csv") as addresses:  # O(1) complexity
    address_data = csv.reader(addresses, delimiter=",")
    address_data = list(address_data)


# Load all the package data into the hash table
def load_package_data(file_name):  # O(n) complexity
    # Read the Packages.csv file
    with open(file_name) as packages:
        package_data = csv.reader(packages, delimiter=",")
        next(package_data)  # Skips the first row with titles of columns like "Package ID, Address, etc."
        for package in package_data:
            package_id = int(package[0])
            address = package[1]
            city = package[2]
            zip_code = package[3]
            deadline = package[4]
            weight = package[5]
            status = "At Hub"

            # Create package object
            package = Package(package_id, address, deadline, city, zip_code, weight, status)

            # Insert package object into hash table
            packages_hash_table.insert(package_id, package)


# The second step is to have functions that will get information from the csv files to use in your algorithm

# Return the distance between the inputted addresses
def distance_between_addresses(row, column):  # O(1) complexity
    distance = distance_data[row][column]
    if distance == "":  # If that row and column doesn't have a value then switch them
        distance = distance_data[column][row]

    return float(distance)


# Return the row of the inputted address from Addresses.csv
def get_address_row(address):  # O(n) complexity
    for row in address_data:
        if address in row[2]:
            return int(row[0])


# The third step is to instantiate the various objects that will be utilized throughout the program

# Create truck objects with manually loaded packages
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
               datetime.timedelta(hours=8))  # 8:00 AM is the earliest time that the truck can leave the hub
truck2 = Truck(16, 18, None, [3, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East",
               datetime.timedelta(hours=10, minutes=20))  # 10:20 AM is the earliest time that the truck can leave the hub
truck3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
               datetime.timedelta(hours=9, minutes=5))  # 9:05 AM is the earliest time that the truck can leave the hub

# Create the hash table that will store the package data
packages_hash_table = HashTable()

# Load all the package data into the hash table
load_package_data("Packages.csv")


# The fourth step is the nearest neighbor algorithm

# Each truck will deliver their packages using the nearest neighbor algorithm
def deliver_packages(truck):  # O(n^2) complexity
    # Track the packages that are still on the truck after each delivery with the remaining_packages list
    remaining_packages = []
    for package_id in truck.packages:
        package = packages_hash_table.search(package_id)
        remaining_packages.append(package)

    truck.packages.clear()  # Clear the list of packages on the truck so the nearest neighbor algorithm can fix the order

    # Nearest neighbor algorithm that will order the truck.packages list by packages with the nearest address
    while len(remaining_packages) > 0:  # O(n^2) complexity
        next_address_distance = 1000
        next_package = None

        # Loop through each package that remains on the truck to find the one with the nearest address
        for package in remaining_packages:
            if distance_between_addresses(get_address_row(truck.address), get_address_row(package.address)) <= next_address_distance:
                next_address_distance = distance_between_addresses(get_address_row(truck.address), get_address_row(package.address))
                next_package = package

        truck.packages.append(next_package)  # Adds the package with the nearest address to the truck.packages list
        remaining_packages.remove(next_package)  # Remove that package from the remaining_packages list
        truck.mileage += next_address_distance  # Add the mileage traveled to the total
        truck.address = next_package.address  # Update the truck's current address
        truck.time += datetime.timedelta(hours=next_address_distance / 18)  # Update the time of the truck after travelling
        next_package.delivery_time = truck.time  # Update the delivery time of the package
        next_package.departure_time = truck.depart_time  # Update the time the package left the hub


deliver_packages(truck1)  # Truck 1 delivers its packages
deliver_packages(truck2)  # Truck 2 delivers its packages
truck3.depart_time = min(truck1.time, truck2.time)  # Prevents Truck 3 from starting until either Truck 1 or Truck 2 is finished
deliver_packages(truck3)  # Truck 3 delivers its packages


# The fifth step is to implement a user interface that can get input from the user

# Provide a user interface through the console to interact with the program
class Main:  # O(n) complexity
    # Allow the user to select an option
    user_input = input(
        "1. Get all packages' information and total mileage \n"
        "2. Get a single package's information at a specific time \n"
        "3. Get all packages' information at a specific time \n"
        "4. Exit the program \n"
    )

    # Print all the package information contained within the hash table and the calculated total mileage
    if int(user_input) == 1:  # O(n) complexity
        print("Package ID, Address, City, Zip Code, Deadline, Weight (KILO), Status, Delivery Time")
        for package_id in range(1, 41):
            package = packages_hash_table.search(
                package_id)  # Searches to see if there is a package with the inputted Package ID in the hash table
            package.status = "Delivered"
            print(package.package_id, ",", package.address, ",", package.city, ",", package.zip_code, ",",
                  package.deadline, ",", package.weight, ",", package.status, ",", package.delivery_time)
        print("The total mileage for the route is:", truck1.mileage + truck2.mileage + truck3.mileage, "miles.")

    # Print the specified package information from the inputted Package ID and at the inputted time
    elif int(user_input) == 2:  # O(1) complexity
        user_time = input("Enter a time in the format of HH:MM:SS. \n")

        # Converts the inputted time into a format that is readable by the program
        (h, m, s) = user_time.split(":")
        converted_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        package_id = input("Enter a package id.")
        package = packages_hash_table.search(
            int(package_id))  # Searches to see if there is a package with the inputted Package ID in the hash table
        package.update_status(converted_time)  # Updates the status of the package based on the inputted time
        if package.status == "Delivered":
            print("Package ID, Address, City, Zip Code, Deadline, Weight (KILO), Status, Delivery Time")
            print(package.package_id, ",", package.address, ",", package.city, ",", package.zip_code, ",",
                  package.deadline, ",", package.weight, ",", package.status, ",", package.delivery_time)
        else:
            print("Package ID, Address, City, Zip Code, Deadline, Weight (KILO), Status")
            print(package.package_id, ",", package.address, ",", package.city, ",", package.zip_code, ",",
                  package.deadline, ",", package.weight, ",", package.status)

    # Prints all the packages' information at the inputted time
    elif int(user_input) == 3:  # O(n) complexity
        user_time = input("Enter a time in the format of HH:MM:SS. \n")

        # Converts the inputted time into a format that is readable by the program
        (h, m, s) = user_time.split(":")
        converted_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        print("Package ID, Address, City, Zip Code, Deadline, Weight (KILO), Status, Delivery Time")
        for package_id in range(1, 41):
            package = packages_hash_table.search(
                package_id)  # Searches to see if there is a package with the inputted Package ID in the hash table
            package.update_status(converted_time)  # Updates the status of the packages based on the inputted time
            if package.status == "Delivered":
                print(package.package_id, ",", package.address, ",", package.city, ",", package.zip_code, ",",
                      package.deadline, ",", package.weight, ",", package.status, ",", package.delivery_time)
            else:
                print(package.package_id, ",", package.address, ",", package.city, ",", package.zip_code, ",",
                      package.deadline, ",", package.weight, ",", package.status)

    # Exits the program
    elif int(user_input) == 4:  # O(1) complexity
        exit()
