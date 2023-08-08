# Create a package object that will hold each package's information
class Package:  # O(1) complexity
    # Store the inputted package information in the package object
    def __init__(self, package_id, address, deadline, city, zip_code, weight, status):  # O(1) complexity
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # Update the status of the package based on the user's inputted time
    def update_status(self, user_input_time):  # O(1) complexity
        if self.delivery_time < user_input_time:
            self.status = "Delivered"
        elif self.departure_time < user_input_time:
            self.status = "En route"
        else:
            self.status = "At Hub"
