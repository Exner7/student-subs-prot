import random
import random


class Collection:
    def __init__(self, items=None):
        # Initialize the collection with the provided items or an empty list
        if items is None:
            self.items = []
        else:
            self.items = list(items)

    def random_pop(self):
        if self.items:
            # Generate a random index within the range of the collection
            random_index = random.randint(0, len(self.items) - 1)
            # Remove and return the item at the random index
            return self.items.pop(random_index)
        else:
            # Return None if the collection is empty
            return None


def is_message_rejected(probability_of_rejection):
    return random.random() < probability_of_rejection


# The registration number should be a 5-digit numeric
def is_registration_number_valid(registration_number):
    registration_number = str(registration_number)
    return len(registration_number) == 5 and registration_number.isdigit()


# The phone number should be a 10-digit numeric,
# starting with a '2' or a '6'
def is_phone_number_valid(phone_number):
    return (
        len(phone_number) == 10
        and phone_number.isdigit()
        and (phone_number[0] == "2" or phone_number[0] == "6")
    )


# The postal code should be a 5-digit numeric
def is_postal_code_valid(postal_code):
    return len(postal_code) == 5 and postal_code.isdigit()


status = [
    "All went well, the connection is to be terminated.",
    "Error-01: Registration number is not consistent.",
    "Error-02: Unknown information type.",
    "Error-03: Phone number incorrect.",
    "Error-04: Full name not present.",
    "Error-05: Last name not present.",
    "Error-06: Father's name not present.",
    "Error-07: Both full and last name not present.",
    "Error-08: Both full and father's name not present.",
    "Error-09: Both last and father's name not present.",
    "Error-10: All names not present.",
    "Error-11: Postal code missing.",
    "Error-12: Postal address missing.",
    "Error-13: Postal city missing.",
    "Error-14: Postal code and address missing.",
    "Error-15: Postal code and city missing.",
    "Error-16: Postal address and postal city missing.",
    "Error-17: All fields from postal data are is missing.",
]
