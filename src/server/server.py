from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack

from messages.termination import construct_termination_header
from messages.information import construct_information_header

from handlers.subcription import handle_subcription_request
from handlers.full_name import handle_full_name_response
from handlers.phone_number import handle_phone_number_response
from handlers.address import handle_address_response
from handlers.termination import handle_termination

from utils.utils import *


# Server setup

server_address = "127.0.0.1"
server_port = 54321

probability_of_rejection = 0.35

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((server_address, server_port))
    server_socket.listen()

    print("The server is now listening for incoming connections")

    close_server_flag = False

    while not close_server_flag:
        connection_socket, (client_address, client_port) = server_socket.accept()

        close_connection_flag = False

        information_types = Collection([0, 1, 2])
        information_handlers = [
            [handle_full_name_response, None],  # Full-name handler, full-name value
            [handle_phone_number_response, None],
            [handle_address_response, None],
        ]

        # Interact with the client...

        status_code = 0
        is_first_message = False

        # Server-client interaction loop
        while not close_connection_flag:
            # Receive message from the client...

            if not is_first_message and is_message_rejected(probability_of_rejection):
                # `1` is the message type for an information request, and
                # `3` is the notification type for a simulated error or resend information request
                connection_socket.sendall(construct_information_header(1, 3))
                print("Simulated error, resend request")

            else:
                # Process message...

                # Receive first 2 Bytes containing message type
                message = connection_socket.recv(2)
                message_type = unpack("H", message)[0]

                print("Message Type:", message_type)

                # Depending on the message type,
                # call appropriate handler function

                match message_type:
                    case 0:
                        is_first_message = True
                        status_code, registration_number = handle_subcription_request(
                            connection_socket
                        )
                    # message types `2`, `3`, and `4`
                    # correspond to information messages
                    case 2 | 3 | 4:
                        (
                            status_code,
                            information_handlers[message_type - 2][1],
                        ) = information_handlers[message_type - 2][0](
                            connection_socket, registration_number
                        )

                    case 5:  # Termination message by the client
                        close_connection_flag = True
                        notification_type = handle_termination(connection_socket)
                        print(status[notification_type])

                    case _:  # Unknown message type
                        # Treated similarly to unknown information type, error #02,
                        # as this case is not specified in the draft's section 4.6
                        close_connection_flag = True
                        connection_socket.sendall(construct_termination_header(5, 2))
                        print("Unknown message type")

                if status_code or (not information_types.items):
                    close_connection_flag = True
                    connection_socket.sendall(
                        construct_termination_header(5, status_code)
                    )
                    print(status[status_code])

                    if not status_code:
                        registration_print_out = "Student registered as:\n"
                        for handler in information_handlers:
                            registration_print_out += "\t" + str(handler[1]) + "\n"

                        print(registration_print_out)

                else:
                    # `1` is the message type for an information request
                    information_request = construct_information_header(
                        1, information_types.random_pop()
                    )

                    connection_socket.sendall(information_request)
