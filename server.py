"""This code is server side to demonstrate
the communication between two devices by sending
 data shows the status of smart home lights"""
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


HOST = '127.0.0.1'     # define the host IP address
PORT = 59001           # define the port number
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket which is IPv4 and TCP
server.bind((HOST, PORT))
server.listen()

# Initializing the content of IoT to be sent to client
IoT = [['kitchen', 'ON'],
       ['bath', 'OFF'],
       ['bedroom', 'ON'],
       ['hall', 'ON']]


def handle_client(client):
    """Function to handle client connection"""
    while True:
        try:
            message = client.recv(1024)  # Variable to receive the data
            # from client through the socket
            data_arr = pickle.loads(message)  # Pickle library to deserialize the received data
            IoT.append(data_arr)  # To add a new data to the initial data

            print(tabulate(IoT, headers=["Room", "Light"]))  # Print the all data in Table
            print('-----------------------------')
            print(TextColor.BLUE + 'Received by client',
                  repr(data_arr) + TextColor.RESET)  # Print the received data in Blue color

        except ConnectionAbortedError:  # Exception in case loss connection with the client
            print(TextColor.FAIL + 'Error here in server!' + TextColor.RESET)
            client.close()  # After print error message, then close the connection
            break


def receive():
    """Function to receive message from client"""
    while True:
        print(TextColor.WARNING + 'Server is running and listening ...'
              + TextColor.RESET)  # Show message that server is work and waiting for clients
        client, address = server.accept()  # Accept client connetion
        print(f'connection is established with {str(address)}')  # Print message with the IP and
        # port of connected client

        data_string = pickle.dumps(IoT)  # Variable contain the data which will send to client and
        # Pickle here serialize the data before sending
        client.send(data_string)  # Send serialized data to client

        message = client.recv(1024)

        data_arr = pickle.loads(message)
        IoT.append(data_arr)

        print(tabulate(IoT, headers=["Room", "Light"]))
        print('----------------------')
        print(TextColor.BLUE + 'Received by Client',
              repr(data_arr) + TextColor.RESET)

        thread = threading.Thread(target=handle_client, args=(client,))  # Create a new thread
        # for every client to speed the processing
        thread.start()


if __name__ == "__main__":
    receive()  # This function will be executed after start the application
