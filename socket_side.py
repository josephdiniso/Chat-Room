import socket
import pickle
import threading
import sys
import json
import hashlib
import os

class hostServer():
    def __init__(self):
        self.threads = []
        self.clients = []
        self.addresses = {}
        #Creates TCP socket(IPv4)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Get server IP
        #returns the host name of the current system running server  
        host_name = socket.gethostname()
        #returns ip address of host
        self.server_IP_address = socket.gethostbyname(host_name)
        print("Server Ipv4: " + self.server_IP_address)
        #Establish port
        self.port = 5555
        #Designates ip as server ip address via bind
        self.s.bind((self.server_IP_address, self.port))
        print("socket binded to %s" %(self.port))
        #prepares socket for accepting connectiooons
        self.s.listen(100)
        print("socket is listening")
        #Recieve client data
        while True:
        # Establish connection with client.
            c, addr = self.s.accept()
            if(c not in self.clients):
                self.clients.append(c)
                self.temp = threading.Thread(target=self.securityCheck, args=(c,addr))
                self.temp.start()


    def securityCheck(self, c, addr):
        passCorrect = False
        #Allows three tries to connect with u & p before closing connection
        for i in range(0,3):
            if self.checkPass(c) == True:
                c.send(b'connect')
                passCorrect=True
                t = threading.Thread(target = self.read_loop, args=(c,addr))
                t.start()
                break
            else:
                c.send(b'Incorrect Password')
        # closes connection with client after 3 attempts
        if passCorrect==False:
            c.close()


    def read_loop(self, c, addr):
        while(1):
            data = c.recv(4096)
            if data:
                self.send_all(c,addr, data.decode('utf-8'))
            else:
                pass


    #Send data to clients
    def send_all(self, c,addr,msg):
        for client in self.clients:
            print('Trying to send')
            if(client!=c):
                try:
                    print(msg)
                    client.send(msg.encode('utf-8'))
                    print('Sent!')
                except:
                    client.close()
                    remove(client)
                    pass
        print('Sent to all clients')


    def remove(self, connection):
        if connection in self.clients: remove(self.clients)

    
    def checkPass(self, c):
        # Takes hashed json dictionary
        with open('users.txt') as json_file:
            data = json.load(json_file)
        # Sends confirmation for client to send username
        c.send(b'Enter username: ')
        user_name = c.recv(4096).decode('utf-8')
        # If username exists, server sends back salt and then receives hashed password attempt
        # Else returns 0
        if(user_name in data):
            c.send(data[user_name]['Pass Salt'].encode('latin-1'))
            pass_key = data[user_name]['Pass Hash']
            pass_hash = c.recv(4096)
            return pass_hash == pass_key.encode('latin-1')
        else:
            c.send(os.urandom(32))
            c.recv(4096)
            return False

host = hostServer()