# Import socket module 
import socket                
import pickle
import sys
import select
import threading
import os


class clientSocket():
    def __init__(self):
        # Create a socket object 
        self.s = socket.socket()       

        # Define the port on which you want to connect 
        self.port = 5555
        # connect to the server on local computer 
        self.server_ipv4 = input("Servers IP Address, or enter 0 to use default server:  ")        #'10.0.0.206'
        if(self.server_ipv4=='0'):
            self.server_ipv4 = '34.231.214.96'
            print("Server_ipv4: ",self.server_ipv4)

        #Define user
        self.userName = input('Enter your username: ')
        #connect to server ip address 
        self.s.connect((self.server_ipv4, self.port))
        self.s.send(self.userName.encode('utf-8'))
        threading.Thread(target=self.send_msg).start()
        threading.Thread(target=self.recv_msg).start()
        
    def __repr__(self):
        print("Username: {}, Host IP: {}, Host Port: {}".format(self.userName, self.server_ipv4, self.port))

    #Send message to server
    def send_msg(self):
        while(1):
            self.message = sys.stdin.readline() 
            self.message_send = "<{}>".format(self.userName)+self.message
            self.s.send(self.message_send.encode('utf-8')) 
            sys.stdout.write("<You> ") 
            sys.stdout.write(self.message) 
            sys.stdout.flush() 
        s.close()

    def recv_msg(self):
        while True:
            data = self.s.recv(4096)
            if data:
                print(data.decode('utf-8'))
            else:
                pass

client1 = clientSocket()
