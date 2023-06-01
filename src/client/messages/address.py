from ctypes import create_string_buffer
from struct import pack_into

from utils.utils import is_postal_code_valid


def construct_address_header(registration_number):
    message_type = 4  # 2 Bytes

    # message type occupies 2 Bytes
    # registration number occupies 2 Bytes
    # the header length itself occupies 4 Bytes
    header_length = 2 + 2 + 4

    postal_code = input("Please, enter postal code: ")
    while not is_postal_code_valid(postal_code):
        postal_code = input(
            "The postal code should be a 5-digit numeric. Please, try again: "
        )
    postal_code = int(postal_code)

    # Postal code, and postal code padding
    # occupy 2 Bytes each
    header_length += 2 + 2

    items = []
    for item in ["postal address", "postal city"]:
        value = input(f"Please, enter {item}: ")
        padding_length = (2 - len(value)) % 4
        items.append({"value": value, "padding_length": padding_length})

        # We add 2, because the item length itself occupies 2 Bytes
        header_length += 2 + len(value) + padding_length

    # Construct the header

    header = create_string_buffer(header_length)
    offset = 0

    pack_into("H", header, offset, message_type)
    offset += 2

    pack_into("H", header, offset, registration_number)
    offset += 2

    pack_into("I", header, offset, header_length)
    offset += 4

    pack_into("H", header, offset, postal_code)
    offset += 2

    pack_into("2x", header, offset)
    offset += 2

    for item in items:
        pack_into("H", header, offset, len(item["value"]))
        offset += 2

        pack_into(
            str(len(item["value"])) + "s", header, offset, bytes(item["value"], "utf-8")
        )
        offset += len(item["value"])

        if item["padding_length"] > 0:
            pack_into(str(item["padding_length"]) + "x", header, offset)
            offset += item["padding_length"]

    return header
