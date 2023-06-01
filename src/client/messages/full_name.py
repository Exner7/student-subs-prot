from ctypes import create_string_buffer
from struct import pack_into


def construct_full_name_header(registration_number):
    message_type = 2  # 2 Bytes

    # message type occupies 2 Bytes
    # registration number occupies 2 Bytes
    # the header length itself occupies 4 Bytes
    header_length = 2 + 2 + 4

    items = []
    for item in ["first name", "last name", "father's name"]:
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
