import socket
import struct
from datetime import datetime
from time import sleep

from constant.mapping import MAPPINGS

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('localhost', 4000))
except Exception:
    print("[-] Could not connect to socket")
    exit(0)


def value_parser(byte_value, value_type):
    if value_type == bytes:
        value = byte_value.hex()
    elif value_type == str:
        value = str(byte_value.decode('utf-8'))
    elif value_type == float:
        value = struct.unpack('>f', byte_value)[0]
    elif value_type == int:
        value = int.from_bytes(byte_value, "big")
    else:
        value = None

    return value


while True:
    # receive the response data (4096 is recommended buffer size)
    response = client.recv(1024)

    response_size = len(response)
    response_time = datetime.now().isoformat()

    print("=" * 150)

    print("{:<20}{:<100}".format("Time", response_time))
    print("{:<20}{:<100}".format("Response", response.hex(':', 1)))
    print("{:<20}{:<100}".format("Size", response_size))
    print()

    if response_size != 36:
        print("[-] Wrong response size")

        continue

    for map_item, map_value in MAPPINGS.items():
        endstring = ''

        for map_subitem, map_subvalue in map_value.items():
            start_address = map_subvalue['address']['start']
            end_address = map_subvalue['address']['start'] + map_subvalue['address']['len']
            value_type = map_subvalue['type']

            byte_value = response[start_address:end_address]

            value = value_parser(byte_value, value_type)

            endstring += "{:<25}".format("{} ({})".format(map_subitem, value))

        print("{:<20}{:<100}".format(map_item.title(), endstring))

    print("=" * 150)

    sleep(0.1)
