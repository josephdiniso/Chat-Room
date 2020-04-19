import socket
import pickle
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Creates TCP socket(IPv4)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Get server IP
host_name = socket.gethostname()                        #returns the host name of the current system running server  
server_IP_address = socket.gethostbyname(host_name)     #returns ip address of host
print("Server Ipv4: " + server_IP_address)
#Establish port
port = 5555

#Designates ip as server ip address via bind
s.bind((server_IP_address, port))
print("socket binded to %s" %(port))
#prepares socket for accepting connectiooons
s.listen(100)
print("socket is listening")
#Recieve client data
def read_loop(c, addr):
    while(1):
        data = c.recv(4096)
        if data:
            send_all(c,addr, data.decode('utf-8'))
        else:
            pass

#Send data to clients
def send_all(c,addr,msg):
    for client in clients:
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

def remove(connection):
    if connection in clients: remove(clients)


threads = []
clients = []
addresses = {}
while True:
    # Establish connection with client.
    c, addr = s.accept()
    # print(clients)
    if(c not in clients):
        clientName = c.recv(4096)
        clients.append(c)
        addresses[addr] = clientName.decode('utf-8')
        t = threading.Thread(target=read_loop, args=(c,addr))
        threads.append(t)
        t.start()
    
c.close()
s.close()
sys.exit()
