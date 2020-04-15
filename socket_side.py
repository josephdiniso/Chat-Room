import socket
import pickle
import threading
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Socket created")

port = 12345

s.bind(('', port))         
print("socket binded to %s" %(port)) 
  
 
s.listen(100)      
print("socket is listening")  

def read_loop(c, addr):
    while(1):
        data = c.recv(4096)
        if data:
            send_all(c,addr, data.decode('utf-8'))
        else:
            pass
def send_all(c,addr,msg):
    for client in clients:
        print('Trying to send')
        if(client!=c):
            try:
                msg = "<"+addresses[addr]+">"+msg
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
    print(clients)
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
