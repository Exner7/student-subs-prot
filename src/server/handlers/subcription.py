from struct import unpack_from

from utils.utils import is_registration_number_valid


def handle_subcription_request(connection_socket):
    """
    Handles a subscription request received over a connection socket.

    Parameters:
        connection_socket (socket):
        The connection socket to receive the request from.

    Returns:
        tuple:
        A tuple containing the status code and registration number
        extracted from the request.

            - status_code (int):
            The status code indicating the validity of the registration number.
            0 indicates a valid registration number,
            while 1 indicates an invalid one.

            - registration_number (int):
            The registration number extracted from the request.
    """

    status_code = 0

    buffer = connection_socket.recv(2)
    registration_number = unpack_from("H", buffer, 0)[0]

    if not is_registration_number_valid(registration_number):
        status_code = 1

    buffer = connection_socket.recv(4)
    header_length = unpack_from("I", buffer, 0)[0]

    print("Registration number:", registration_number)
    print("Header length:", header_length)

    return status_code, registration_number
