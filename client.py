# Import socket module 
import socket                
import pickle
import sys
import select
import threading
import os

#Import tkinter class
from tkinter import *           



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




class chatInterface:

    def __init__(self, master):             #Occurs as soon as your create an object
        top_frame = Frame(master)           #Frame for data
        self.room_title = Label(text="Welcome to JB's Chat Room!", bg="gray")   
        self.room_title.pack(side=TOP, fill=X)

        self.print_button = Button(text="Click to be greeted", command=self.printMessage)
        self.print_button.pack(side=BOTTOM)


    def printMessage(self):
        print("Welcome")


#Create GUI object for chat room
window = Tk()                                             #Creates blank window
client_interface = chatInterface(window)                          #Need an object to do stuff in class


#Create clientSocket() objext client1
client1 = clientSocket()

#Keeps window continuously on screen, hence main loop for the GUI 
window.mainloop()                                         