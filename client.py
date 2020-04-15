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
userName = input('Enter your username: ')
s.connect(('127.0.0.1', port)) 
s.send(userName.encode('utf-8'))
def send_msg(s):
    while(1):
        message = sys.stdin.readline() 
        s.send(message.encode('utf-8')) 
        sys.stdout.write("<You>") 
        sys.stdout.write(message) 
        sys.stdout.flush() 

def recv_msg(s):
    while True:
        data = s.recv(4096)
        if data:
            print(data.decode('utf-8'))
        else:
            pass

threading.Thread(target=send_msg, args=(s,)).start()
threading.Thread(target=recv_msg, args=(s,)).start()