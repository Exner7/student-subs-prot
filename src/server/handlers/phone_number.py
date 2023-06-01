from struct import unpack_from

from utils.utils import is_phone_number_valid


def handle_phone_number_response(connection_socket, original_registration_number):
    status_code = 0

    buffer = connection_socket.recv(2)
    registration_number = unpack_from("H", buffer, 0)[0]

    buffer = connection_socket.recv(4)
    header_length = unpack_from("I", buffer, 0)[0]

    print("Registration number:", registration_number)

    if original_registration_number != registration_number:
        status_code = 1
        return status_code, None

    buffer = connection_socket.recv(10)
    phone_number = (unpack_from("10s", buffer, 0)[0]).decode("utf-8")

    print("Phone number:", phone_number)

    connection_socket.recv(2)

    if not is_phone_number_valid(phone_number):
        status_code = 3

    return status_code, phone_number
