from struct import unpack_from


def handle_termination(connection_socket):
    buffer = connection_socket.recv(2)
    notification_type = unpack_from("H", buffer, 0)[0]

    buffer = connection_socket.recv(4)

    return notification_type