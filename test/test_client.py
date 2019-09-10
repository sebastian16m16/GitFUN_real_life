import unittest
import threading
from src.client import *
from src.server import *


def start_server():
    server = Server('localhost', 50007)
    server.loop()


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = threading.Thread(target=start_server)
        cls.t.start()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = Client('localhost', 50007)
        self.client.add_device(id='1234', type='temp', name='parcela00')

    def tearDown(self):
        self.client.remove_device(id='1234')

    def test_get_device_status(self):
        status = self.client.get_device_status(id='1234')
        self.assertEqual(status, 'OK')

    def test_device_not_found(self):
        status = self.client.get_device_status(id='dsfjshf')
        self.assertNotEqual(status, 'OK')

    def test_remove_device(self):
        status = self.client.remove_device(id='1234')
        self.assertEqual(status, 'OK')
        status = self.client.get_device_status(id='1234')
        self.assertEqual(status.lower(), 'nok: device not found')

    def test_add_device(self):
        id = '1235'
        status = self.client.add_device(id, type='temp', name='parcela01')
        self.assertEqual(status, 'OK')
        status = self.client.get_device_status(id)
        self.assertEqual(status, 'OK')

    def test_add_invalid_device(self):
        id = '1236'
        status = self.client.add_device(id, 'cucubau', 'parcela02')
        self.assertEqual(status, 'NOK: unknown device type')
        status = self.client.get_device_status(id)
        self.assertEqual(status, 'NOK: not found')


if __name__ == '__main__':
    unittest.main()
