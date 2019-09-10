import socket
import abc

HOST = 'localhost'
PORT = 50007


class Device(object):
    def __init__(self, id, type, name, status='OK'):
        self.id = id
        self.type = type
        self.name = name
        self.status = status

    @abc.abstractmethod
    def get_data(self):
        return


class TempSensor(Device):
    def __init__(self, id, name, status='OK'):
        Device.__init__(self, id, 'temp', name, status)
        self.temp = 0
        self.humidity = 0.0

    def get_data(self):
        return self.temp, self.humidity


class Server(object):
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.actions = {
            'get_device_status': self.get_device_status,
            'set_device_status': self.set_device_status,
            'add_device': self.add_device,
            'remove_device': self.remove_device
        }
        self.devices = dict()

    def __del__(self):
        self.s.close()

    def disconnect(self):
        self.s.close()

    def loop(self):
        self.s.listen(1)
        conn, addr = self.s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode('utf-8')
                if command == 'stop':
                    print('Client disconnected')
                    break
                args = command.split(':')[1:]
                command = command.split(':')[0]
                f = self.actions.get(command)
                response = f(*args) if f is not None else 'unknown command'
                conn.sendall(response.encode('utf-8'))

    def get_device_status(self, id):
        device = self.devices.get(id)
        return device.status if device is not None else 'NOK: not found'

    def set_device_status(self, id, status):
        device = self.devices.get(id)
        if device is None:
            return 'NOK: not found'
        device.status = status
        return 'OK'

    def add_device(self, id, type, name):
        if type == 'temp':
            device = TempSensor(id, name)
            self.devices[id] = device
            return 'OK'
        return 'NOK: unknown device type'

    def remove_device(self, id):
        if self.devices.get(id) is None:
            return 'NOK: not found'
        del self.devices[id]
        return 'OK'
