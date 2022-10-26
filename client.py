"""This code is client side which receive
table of data shows status of smart home light
and send commands to control the lights"""
import threading
import socket
import pickle
from tabulate import tabulate


class TextColor:
    """This class is defined colors"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'


alias = input(TextColor.BLUE + 'Who are you >>> ' + TextColor.RESET)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket which is IPv4 and TCP
client.connect(('127.0.0.1', 59001))    # Connect to the socket with specific IP and port


def client_receive():
    """Function to receive message from server"""
    while True:
        try:
            message = client.recv(1024)  # Variable to receive the data
            # from server through the socket
            data_arr = pickle.loads(message)  # Pickle library to deserialize the received data
            print(tabulate(data_arr, headers=["Room", "Light"]))  # Print the data in Table

        except ConnectionAbortedError:  # Exception in case loss connection
            print('Error here in client!')
            client.close()  # After print error message, then close the connection
            break


def client_send():
    """Function to send message to server """
    while True:

        room = input(TextColor.BLUE + 'input room name >>'
                     + TextColor.RESET)  # Variable to safe client input (room name)
        light = input(TextColor.BLUE + 'input light ON/OFF >>'
                      + TextColor.RESET)  # Variable to safe client input (ON/OFF)

        if light in ('ON', 'on', 'OFF', 'off'):  # Test user inputs if correct
            message = [room, light]  # variable to safe inputs as matrix
            data_string = pickle.dumps(message)  # Variable contain the data which will send
            # to server and Pickle here serialize the data before sending
            client.send(data_string)  # Send serialized data to server
            print('-----------------------------------------------')
            print(TextColor.GREEN + 'Your inputs are successfully '
                                    'sent to the Server' + TextColor.RESET)
            print('-----------------------------------------------')

        else:  # If client enter wrong inputs print error message
            print('-----------------------------------------------')
            print(TextColor.FAIL + 'The Server not accepted '
                                   'you inputs' + TextColor.RESET)
            print(TextColor.WARNING + 'you input wrong data, light '
                                      'should be On or Off' + TextColor.RESET)
            print('-----------------------------------------------')


receive_thread = threading.Thread(target=client_receive)  # Create a new thread for
# clients receive process
receive_thread.start()

send_thread = threading.Thread(target=client_send)  # Create a new thread for clients send process
send_thread.start()
