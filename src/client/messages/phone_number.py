from struct import pack_into
from ctypes import create_string_buffer

from utils.utils import is_phone_number_valid


def construct_phone_number_header(registration_number):
    message_type = 3

    phone_number = input("Please, enter phone number: ")
    while not is_phone_number_valid(phone_number):
        phone_number = input(
            "The phone number should be a 10-digit numeric, "
            + "starting with a '2' or a '6'. "
            + "Please, try again: "
        )

    header_length = 20

    header = create_string_buffer(header_length)
    offset = 0

    pack_into("H", header, offset, message_type)
    offset += 2

    pack_into("H", header, offset, registration_number)
    offset += 2

    pack_into("I", header, offset, header_length)
    offset += 4

    pack_into("10s", header, offset, bytes(phone_number, "utf-8"))
    offset += 10

    pack_into("2x", header, offset)
    offset += 2

    return header
