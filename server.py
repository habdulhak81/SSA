import threading
import socket
from tabulate import tabulate
import pickle


class textcolor:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'


host = '127.0.0.1'
port = 59001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

IoT = [['kitchen', 'ON'],
       ['bath', 'OFF'],
       ['bedroom', 'ON'],
       ['hall', 'ON']]


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            data_arr = pickle.loads(message)
            IoT.append(data_arr)

            print(tabulate(IoT, headers=["Room", "Light"]))
            print('-----------------------------')
            print(textcolor.BLUE + 'Received by client', repr(data_arr) + textcolor.RESET)

        except:
            print(textcolor.FAIL +'Error here in server!' + textcolor.RESET)
            client.close()
            break


def receive():
    while True:
        print(textcolor.WARNING + 'Server is running and listening ...' + textcolor.RESET)
        client, address = server.accept()
        print(f'connection is established with {str(address)}')

        data_string = pickle.dumps(IoT)
        client.send(data_string)

        message = client.recv(1024)

        data_arr = pickle.loads(message)

        IoT.append(data_arr)

        print(tabulate(IoT, headers=["Room", "Light"]))
        print('----------------------')
        print(textcolor.BLUE + 'Received by Client', repr(data_arr) + textcolor.RESET)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



if __name__ == "__main__":
    receive()
