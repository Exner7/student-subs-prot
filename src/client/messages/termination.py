from struct import pack_into
from ctypes import create_string_buffer


def construct_termination_header(message_type, notification_type):
    message_type = 5

    header_length = 8

    header = create_string_buffer(header_length)

    pack_into("H", header, 0, message_type)
    pack_into("H", header, 2, notification_type)
    pack_into("I", header, 4, header_length)

    return header
