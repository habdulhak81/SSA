import threading
import socket
import pickle
from tabulate import tabulate

alias = input('Who are you >>> ')
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

        room = input('input room name >>')
        light = input('input light ON/OFF >>')
        IoT =[room, light]
        data_string = pickle.dumps(IoT)
        client.send(data_string)



receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()



