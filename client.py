# Import socket module 
import socket                
import pickle
import sys
import select
import threading

# Create a socket object 
s = socket.socket()       

# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
server_ipv4 = input("Servers IP Address:  ")        #'10.0.0.206'
userName = input('Enter your username: ')           #Define user
s.connect((server_ipv4, port))                     #connect to server ip address 
s.send(userName.encode('utf-8'))

#Send message to server
def send_msg(s):
    while(1):
        message = sys.stdin.readline() 
        s.send(message.encode('utf-8')) 
        sys.stdout.write("<You> ") 
        sys.stdout.write(message) 
        sys.stdout.flush() 
    s.close()

def recv_msg(s):
    while True:
        data = s.recv(4096)
        if data:
            print(data.decode('utf-8'))
        else:
            pass

threading.Thread(target=send_msg, args=(s,)).start()
threading.Thread(target=recv_msg, args=(s,)).start()
