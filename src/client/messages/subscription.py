from struct import pack_into
from ctypes import create_string_buffer

from utils.utils import is_registration_number_valid


def construct_subscription_header():
    message_type = 0

    registration_number = input("Please, enter registration number: ")
    while not is_registration_number_valid(registration_number):
        registration_number = input(
            "The registration number should be a 5-digit numeric. "
            + "Please, try again: "
        )
    registration_number = int(registration_number)

    header_length = 8

    header = create_string_buffer(header_length)

    pack_into("H", header, 0, message_type)
    pack_into("H", header, 2, registration_number)
    pack_into("I", header, 4, header_length)

    return registration_number, header
