import threading
import socket
import pickle
from tabulate import tabulate

class textcolor:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'


alias = input(textcolor.BLUE + 'Who are you >>> ' + textcolor.RESET)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59001))

IoT =[]

def client_receive():
    while True:
        try:

            message = client.recv(1024)

            data_arr = pickle.loads(message)
            print(tabulate(data_arr, headers=["Room", "Light"]))

        except:
            print('Error here in client!')
            client.close()
            break


def client_send():
    while True:

        room = input(textcolor.BLUE + 'input room name >>' + textcolor.RESET)
        light = input(textcolor.BLUE + 'input light ON/OFF >>' +textcolor.RESET)
        if light in ('ON', 'on', 'OFF', 'off'):
            IoT = [room, light]
            data_string = pickle.dumps(IoT)
            client.send(data_string)
            print('-----------------------------------------------')
            print(textcolor.GREEN + 'Your inputs are successfully sent to the Server' + textcolor.RESET)
            print('-----------------------------------------------')
        else:
            print('-----------------------------------------------')
            print(textcolor.FAIL + 'The Server not accepted you inputs' + textcolor.RESET)
            print(textcolor.WARNING + 'you input wrong data, light should be On or Off' + textcolor.RESET)
            print('-----------------------------------------------')


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
