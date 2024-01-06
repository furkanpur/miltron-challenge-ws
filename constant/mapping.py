MAPPINGS = {
    "header": {
        "start_byte": {
            "address": {
                "start": 0x00,
                "len": 1
            },
            "type": bytes,
            "description": "Packet start byte"
        },
        "id": {
            "address": {
                "start": 0x01,
                "len": 10
            },
            "type": str,
            "description": "Rocket telemetry system ID. This will be the same value as Rocket ID."
        },
        "packet_number": {
            "address": {
                "start": 0x0B,
                "len": 1
            },
            "type": bytes,
            "description": "Packet number. Will be reset every 256 frame."
        },
        "packet_size": {
            "address": {
                "start": 0x0C,
                "len": 1
            },
            "type": bytes,
            "description": "Packet size"
        },
    },
    "payload": {
        "altitude": {
            "address": {
                "start": 0x0D,
                "len": 4
            },
            "type": float,
            "description": "Altitude as metre - m"
        },
        "speed": {
            "address": {
                "start": 0x11,
                "len": 4
            },
            "type": float,
            "description": "Speed as metre per second m/s"
        },
        "acceleration": {
            "address": {
                "start": 0x15,
                "len": 4
            },
            "type": float,
            "description": "Acceleration as metre per second per second m/s^2"
        },
        "thrust": {
            "address": {
                "start": 0x19,
                "len": 4
            },
            "type": float,
            "description": "Thrust as Newton - N"
        },
        "temperature": {
            "address": {
                "start": 0x1D,
                "len": 4
            },
            "type": float,
            "description": "Temperature as degree Celsius"
        }
    },
    "footer": {
        "crc16": {
            "address": {
                "start": 0x021,
                "len": 2
            },
            "type": int,
            "description": "CRC16/BUYPASS value. Calculated from header and payload combined."
        },
        "delimiter": {
            "address": {
                "start": 0x23,
                "len": 1
            },
            "type": bytes,
            "description": "Delimiter"
        }
    }
}
