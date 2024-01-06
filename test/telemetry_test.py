import socket
import unittest


class TelemetryTest(unittest.TestCase):

    def test_connection(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)

        client.connect(('localhost', 5000))

        response = client.recv(36)

        client.close()

    def test_data_size(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(('localhost', 4000))

        response = client.recv(36)

        client.close()

        self.assertEqual(len(response), 36)


if __name__ == '__main__':
    unittest.main()
