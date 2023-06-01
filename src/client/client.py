from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack

from utils.utils import *

from messages.subscription import construct_subscription_header
from messages.full_name import construct_full_name_header
from messages.phone_number import construct_phone_number_header
from messages.address import construct_address_header
from messages.termination import construct_termination_header

from handlers.information import handle_information_request
from handlers.termination import handle_termination


# Information type corresponds to indeces
header_constructors = [
    construct_full_name_header,
    construct_phone_number_header,
    construct_address_header,
]

server_address = "127.0.0.1"
server_port = 54321

with socket(AF_INET, SOCK_STREAM) as connection_socket:
    connection_socket.connect((server_address, server_port))

    # Interact with the server...

    # Send subscription requests to the server
    registration_number, message_to_send = construct_subscription_header()
    connection_socket.sendall(message_to_send)

    close_connection_flag = False

    while not close_connection_flag:
        # Receive message from the server

        # Process message

        # Receive first 2 Bytes containing message type
        buffer = connection_socket.recv(2)
        message_type = unpack("H", buffer)[0]

        print("Message Type:", message_type)

        # Depending on the message type,
        # call appropriate handler method

        match message_type:
            case 1:  # Information request
                information_type = handle_information_request(connection_socket)
                match information_type:
                    case 0 | 1 | 2:
                        message_to_send = header_constructors[information_type](
                            registration_number
                        )
                        connection_socket.sendall(message_to_send)

                    case 3:  # Simulated error, resend request
                        connection_socket.sendall(message_to_send)
                        print("Simulated error, resend request")

                    case _:  # Unknown information type, error #02
                        close_connection_flag = True
                        message_to_send = construct_termination_header(5, 2)
                        connection_socket.sendall(message_to_send)
                        print(status[2])

            case 5:  # Termination message by the server
                close_connection_flag = True
                notification_type = handle_termination(connection_socket)
                print(status[notification_type])

            case _:  # Unknown message type
                # Treated similarly to unknown information type, error #02,
                # as this case is not specified in the draft's section 4.6
                close_connection_flag = True
                message_to_send = construct_termination_header(5, 2)
                connection_socket.sendall(message_to_send)
                print("Unknown message type")
