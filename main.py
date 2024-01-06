#!/usr/bin/env python
import asyncio
import json
import socket
import struct

import requests
import websockets

from constant.mapping import MAPPINGS


async def telemetry_data_parser(response):
    """
    Parses the telemetry data from the socket data

    :param response:
    :return: telemetry data
    """
    result = {}

    for map_key, map_value in MAPPINGS['payload'].items():
        start_address = map_value['address']['start']
        end_address = map_value['address']['start'] + map_value['address']['len']
        value_type = map_value['type']

        byte_value = response[start_address:end_address]

        """ Parse by given byte type """
        if value_type == bytes:
            value = byte_value.hex()
        elif value_type == str:
            value = str(byte_value.decode('utf-8'))
        elif value_type == float:
            value = struct.unpack('>f', byte_value)[0]

            if value > 1e+10:
                value = -1
        elif value_type == int:
            value = int.from_bytes(byte_value, "big")

            if value > 1e+10:
                value = -1
        else:
            value = None

        result[map_key] = value

    return result


async def telemetry_service_client_factory(selected_rocket):
    """
    Create a new socket client for telemetry

    :param selected_rocket:
    :return: client
    """

    telemetry_host = 'host.docker.internal'  # selected_rocket['telemetry']['host']
    telemetry_port = selected_rocket['telemetry']['port']
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((telemetry_host, telemetry_port))

    return tcp_client


async def get_rocket_data(message):
    """
    Get rocket metadata from API

    :param message:
    :return: rocket data
    """
    r = requests.get(url="http://host.docker.internal:5000/rockets", headers={"X-API-Key": "API_KEY_1"})

    rockets_data = r.json()
    selected_rocket = None

    for rocket in rockets_data:

        if rocket['id'] == message:
            selected_rocket = rocket
            break

    return selected_rocket


async def handler(websocket):
    """
    Websocket handler

    :param websocket:
    :return:
    """
    while True:
        try:
            """ Get rocket id """
            message = await websocket.recv()

            """ Get rocket metadata """
            selected_rocket = await get_rocket_data(message)

            if not selected_rocket:
                continue

            """ Get telemetry socket client of rocket """
            tcp_client = await telemetry_service_client_factory(selected_rocket)

            while True:
                """ Get telemetry data"""
                telemetry_data_response = tcp_client.recv(1024)

                """ Parse telemetry data """
                result = await telemetry_data_parser(telemetry_data_response)

                """ Send formatted data to websocket """
                await websocket.send(json.dumps(result))

                """ Sleep 1 seconds """
                await asyncio.sleep(1)

        except websockets.ConnectionClosedOK:
            print("[-] Websocket connection closed")

            break
        except socket.error as err:
            print("[-] Could not connect to socket")
            print("[-] {}".format(err))
        except Exception as err:
            print("[-] Unknown error: {}".format(err))

            continue


async def main():
    async with websockets.serve(handler, "", 8765):
        await asyncio.Future()  # run forever
        print("Listening on port 8765")


if __name__ == "__main__":
    asyncio.run(main())
