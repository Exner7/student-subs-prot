from struct import unpack_from


def handle_information_request(connection_socket):
    message_data = connection_socket.recv(2)
    information_type = unpack_from("H", message_data, 0)[0]

    message_data = connection_socket.recv(4)

    return information_type
