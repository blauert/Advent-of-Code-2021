# https://adventofcode.com/2021/day/16

with open('real_input.txt') as file:
    real_string = file.read()

with open('test_input.txt') as file:
    test_strings = [line.strip() for line in file.readlines()]

#string = test_strings[14]  # Part 1: 0-6, Part 2: 7-14
#print(f"Hex: {string}")

string = real_string

packet = 0
packet_len = len(string) * 4
gnirts = string[::-1]
for i in range(len(string)):
    packet += int(gnirts[i], 16) << i * 4


def get_version(packet, packet_len):
    version_mask = int('111', 2) << packet_len - 3
    version = (packet & version_mask) >> packet_len - 3
    packet_len -= 3
    return version, packet_len


def get_type(packet, packet_len):
    type_mask = int('111', 2) << packet_len - 3
    type_id = (packet & type_mask) >> packet_len - 3
    packet_len -= 3
    return type_id, packet_len


def get_literal(packet, packet_len):
    literal = 0
    prefix = 1
    while prefix == 1:
        prefix_mask = 1 << packet_len - 1
        prefix = (packet & prefix_mask) >> packet_len - 1
        num_mask = int('1111', 2) << packet_len - 5
        num = (packet & num_mask) >> packet_len - 5
        literal = (literal << 4) + num
        packet_len -= 5
    return literal, packet_len


def get_length_type(packet, packet_len):
    length_type_mask = 1 << packet_len - 1
    length_type_id = (packet & length_type_mask) >> packet_len - 1
    packet_len -= 1
    return length_type_id, packet_len


def decode_packet(packet, packet_len):

    global version_numbers  # Part 1
    version, packet_len = get_version(packet, packet_len)
    version_numbers += version
    
    type_id, packet_len = get_type(packet, packet_len)

    # Literal value packet (Type 4)
    if type_id == 4:  
        value, packet_len = get_literal(packet, packet_len)

    # Operator packet (Types 0-3, 5-7)
    else:
        subp_values = []

        length_type_id, packet_len = get_length_type(packet, packet_len)

        if length_type_id == 0:
            # Next 15 bits = total length of following subpackets
            subp_mask = int('111111111111111', 2) << packet_len - 15
            subp_len = (packet & subp_mask) >> packet_len - 15
            packet_len -= 15
            end_len = packet_len - subp_len
            while packet_len > end_len:
                packet_len, value = decode_packet(packet, packet_len)
                subp_values.append(value)

        elif length_type_id == 1:
            # Next 11 bits = number of subpackets
            subp_mask = int('11111111111', 2) << packet_len - 11
            no_subp = (packet & subp_mask) >> packet_len - 11
            packet_len -= 11
            for i in range(no_subp):
                packet_len, value = decode_packet(packet, packet_len)
                subp_values.append(value)

        # Evaluate expression on sub-packet values
        if type_id == 0:  # sum
            value = sum(subp_values)
        elif type_id == 1:  # product
            value = 1
            for i in subp_values:
                value *= i
        elif type_id == 2:  # minimum
            value = min(subp_values)
        elif type_id == 3:  # maximum
            value = max(subp_values)
        elif type_id == 5:  # greater than
            if subp_values[0] > subp_values[1]:
                value = 1
            else:
                value = 0
        elif type_id == 6:  # less than
            if subp_values[0] < subp_values[1]:
                value = 1
            else:
                value = 0
        elif type_id == 7:  # equal to
            if subp_values[0] == subp_values[1]:
                value = 1
            else:
                value = 0

    return packet_len, value


# Part 1
version_numbers = 0
p_len, value = decode_packet(packet, packet_len)
print(f"Part 1: Sum of version numbers: {version_numbers}")

# Part 2
print(f"Part: BITS transmission: {value}")
