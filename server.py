import time
from Devices import Lamp
import socket
from threading import Thread
import sys

class Logger(object):
    def __init__(self, filename="default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(time.strftime('\n[%y-%m-%d %H:%M:%S] ') + message)
        self.log.flush()

    def flush(self):
        self.log.flush()

    def __del__(self):
        self.log.close()

sys.stdout = Logger('/home/pi/Home_Automation/server.log')

class Server:
    devices = {}
    port = 1313

    def __init__(self):
        self.devices['lamp'] = {}
        self.devices['lamp']['myRoom'] = Lamp('myRoom')
        print(self.devices['lamp']['myRoom'])

        self.skt = socket.socket()
        self.skt.bind(('192.168.1.150', self.port))
        self.skt.listen(5)

    def executeRequest(self, request):
        request = request.replace('\r', '')
        request = request.replace('\n', '')
        request = request.split(',')
        do = getattr(self.devices[request[0]][request[1]], request[2])
        return do()

    def handleRequest(self, clientSocket, addr):
        print('Connection from {}'.format(addr))
        msg = clientSocket.recv(1024)
        print('Received msg {} from {}'.format(msg, addr))
        result = self.executeRequest(msg.decode())
        clientSocket.sendall(str(result).encode())
        clientSocket.close()


    def run(self):
        while True:
            try:
                print('Waiting for connection...')
                c, addr = self.skt.accept()
                Thread(target=self.handleRequest, args=(c, addr)).start()
            except KeyboardInterrupt:
                print('Exitting...')
                self.skt.close()
                exit()
            except Exception as e:
                print(e)

if __name__ == '__main__':
    srv = Server()
    srv.run()
