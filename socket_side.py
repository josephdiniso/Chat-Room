import socket
import pickle
import threading
import sys
import json
import hashlib

class hostServer():
    def __init__(self):
        self.threads = []
        self.clients = []
        self.addresses = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Creates TCP socket(IPv4)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Get server IP
        host_name = socket.gethostname()                        #returns the host name of the current system running server  
        self.server_IP_address = socket.gethostbyname(host_name)     #returns ip address of host
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
                clientName = c.recv(4096)
                self.clients.append(c)
                self.addresses[addr] = clientName.decode('utf-8')
                temp = threading.Thread(target=self.securityCheck, args=(c,addr))
                temp.start()
    def securityCheck(self, c, addr):
        # Receives original username from client
        user_orig = c.recv(4096)
        

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
    
    def checkPass(self, c, user_orig, first):
        c.send(b'Enter username: ')
        user_name = c.recv(4096).decode('utf-8')
        c.send(b'Enter password: ')
        pass_string = c.recv(4096).decode('utf-8')
        with open('users.txt') as json_file:
            data = json.load(json_file)
        if pass_string in data:
            pass_key = data[user_name]['Pass Hash']
        else:
            return False
        pass_salt = data[user_name]['Pass Salt']
        pass_hash = hashlib.pbkdf2_hmac('sha256', pass_string.encode('utf-8'), pass_salt.encode('latin-1'), 100000, dklen = 128)
        return pass_hash == pass_key.encode('latin-1')
host = hostServer()