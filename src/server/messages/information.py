from struct import pack_into
from ctypes import create_string_buffer


def construct_information_header(message_type, information_type):
    header_length = 8

    header = create_string_buffer(header_length)

    pack_into("H", header, 0, message_type)
    pack_into("H", header, 2, information_type)
    pack_into("I", header, 4, header_length)

    return header
