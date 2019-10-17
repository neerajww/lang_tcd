import socket
import time
import sys


def isOffline():
    if len(sys.argv) > 1:
        if any(x == 'offline' for x in sys.argv[1:]):
        # if sys.argv[1] == 'offline':
            return True
    return False


class Sender:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        if not isOffline():
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket.connect((self.ip, self.port))
    
    def send(self, trigger):
        try:
            with open('timing.txt', 'a+') as file:
                file.write('{0} {1}\n'.format(trigger, time.time()))
            str = '#Din:%s\n' % trigger
            # print(str)
            strb = bytes(str, 'utf-8')
            if not isOffline():
                self.my_socket.sendall(strb)
        except:
            print('Sending {0} failed.'.format(trigger))

    def sendTrigger(self, prompt, section):
        dictn = {'start': '00', 'listen': '01', 'rest': '02', 'keypress': '03', 'end': '99'}
        trigger = '{0:03d}'.format(prompt) + dictn[section]
        # print(trigger)
        self.send(trigger)
