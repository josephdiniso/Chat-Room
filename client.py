# Import socket module 
import socket                
import pickle
import sys
import select
import threading

# Create a socket object 
s = socket.socket()       

# Define the port on which you want to connect 
port = 5555
# connect to the server on local computer 
server_ipv4 = input("Servers IP Address, or enter 0 to use default server:  ")        #'10.0.0.206'
if(server_ipv4=='0'):
    server_ipv4 = '34.231.214.96'

#Define user
userName = input('Enter your username: ')
#connect to server ip address 
s.connect((server_ipv4, port))
s.send(userName.encode('utf-8'))

#Send message to server
def send_msg(s):
    while(1):
        message = sys.stdin.readline() 
        message_send = "<{}>".format(userName)+message
        s.send(message_send.encode('utf-8')) 
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
