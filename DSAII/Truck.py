# Create a truck object that will hold the packages
class Truck:  # O(1) complexity
    # Store the inputted truck information in the truck object
    def __init__(self, capacity, speed, load, packages, mileage, address, depart_time):  # O(1) complexity
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time
