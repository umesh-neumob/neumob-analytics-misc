import os
import mmap
import time
import socket, struct

ROMER_FILE = 'romer2.bin'


def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


# netblock_row_size = 24
# pops_per_row = 16
# bytes_per_pop = 2
# rtt_bytes_per_pop = 1

ip_addr = '69.181.141.212'

l = list()
with open(ROMER_FILE, 'rb') as f:
    f.seek(-16, os.SEEK_END)
    romer_footer = f.read(16)
    netblock_row_size = romer_footer[8]
    pops_per_row = romer_footer[9]
    bytes_per_pop = romer_footer[10]
    rtt_bytes_per_pop = romer_footer[11]
    total_bytes_per_pop = bytes_per_pop + rtt_bytes_per_pop
    row_len = pops_per_row * total_bytes_per_pop
    i = 0
    while i < pops_per_row:
        start_byte = i*total_bytes_per_pop
        end_byte = start_byte + bytes_per_pop
        end_byte_rtt = end_byte+rtt_bytes_per_pop
        l.append((start_byte, end_byte, end_byte_rtt))
        i += 1

def test1(ip):
    ip_num = ip2long(ip)
    ip_col = ip_num >> (32-netblock_row_size)
    row_offset = ip_col*row_len

    with open(ROMER_FILE, 'rb') as romer_file:
        romer_file.seek(row_offset)
        pop_details = romer_file.read(row_len)

    for (start_byte, end_byte, end_byte_rtt) in l:
        pop_id_packed = pop_details[start_byte:end_byte]
        pop_rtt_packed = pop_details[end_byte:end_byte_rtt]
        pop_id = int.from_bytes(pop_id_packed, byteorder='big')
        pop_rtt = int.from_bytes(pop_rtt_packed, byteorder='big')
        print('pop_id = %d pop_rtt = %d' % (pop_id, pop_rtt))


if __name__ == '__main__':
    reqStart = int(time.time() * 1000)
    for _ in range(1):
        test1(ip_addr)
    reqTaken = int(time.time() * 1000) - reqStart
    print("Time Taken : %d msec !" % reqTaken)

