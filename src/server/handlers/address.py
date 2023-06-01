from struct import unpack_from


def handle_address_response(connection_socket, original_registration_number):
    status_code = 0

    read_bytes = 0

    buffer = connection_socket.recv(2)
    read_bytes += 2
    registration_number = unpack_from("H", buffer, 0)[0]

    buffer = connection_socket.recv(4)
    read_bytes += 4
    header_length = unpack_from("I", buffer, 0)[0]

    buffer = connection_socket.recv(4)
    read_bytes += 4
    postal_code, padding = unpack_from("HH", buffer, 0)

    print("Registration number:", registration_number)
    print("Header length:", header_length)
    print("Postal code:", postal_code)

    # We subtract 2, because server has read the message type (2 Bytes)
    unread_bytes = header_length - read_bytes - 2
    remaining_buffer = connection_socket.recv(unread_bytes)

    if original_registration_number != registration_number:
        status_code = 1
        return status_code, None

    full_address = [postal_code]

    offset = 0

    loop_counter = 2  # Used to construct status codes in [11, 17]
    both = False  # Used to indicate the absence of 2 values
    while offset < unread_bytes:
        value_length = unpack_from("H", remaining_buffer, offset)[0]
        offset += 2

        if value_length == 0:
            if status_code > 0:
                both = True
            status_code += loop_counter

        value = (
            unpack_from(str(value_length) + "s", remaining_buffer, offset)[0]
        ).decode("utf-8")
        offset += value_length

        print(value)
        full_address.append(value)

        padding_length = (2 - value_length) % 4
        offset += padding_length

        loop_counter += 1

    if both:
        status_code += 1
    if status_code > 0:
        status_code += 10
        return status_code, None

    return status_code, full_address
