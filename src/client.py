import socket
import time

HOST = 'localhost'
PORT = 50007


class Client(object):
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def __del__(self):
        self.s.close()

    def disconnect(self):
        self.__send_command('stop')
        self.s.close()

    def __send_command(self, command):
        self.s.sendall(command.encode('utf-8'))
        response = self.s.recv(10 * 1024)
        return response.decode('utf-8')

    def get_device_status(self, id):
        return self.__send_command(f'get_device_status:{id}')

    def set_device_status(self, id, status='OK'):
        return self.__send_command(f'set_device_status:{id}:{status}')

    def add_device(self, id, type, name):
        return self.__send_command(f'add_device:{id}:{type}:{name}')

    def remove_device(self, id):
        return self.__send_command(f'remove_device:{id}')


if __name__ == '__main__':
    client = Client()
    for i in range(10):
        print(client.get_device_status('1234'))
        time.sleep(1)
