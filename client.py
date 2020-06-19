# Import socket module 
import socket                
import pickle
import sys
import select
import threading
import os
import hashlib
from tkinter import * 



#Notes:
'''
Must remove threading and allow for tkinter to send text, receiving text may remain the same
'''
class clientSocket():
    def __init__(self, master):
        self.master = master
        top_frame = Frame(master)           #Frame for data
        #self.print_button = Button(text="Click to be greeted", command=self.printMessage)
        #self.print_button.pack(side=BOTTOM)
        #Creates message list variable
        self.msg_list = Listbox(height=15, width=50)
        #Creates scroll bar variable
        self.scrollbar = Scrollbar(master, command=self.msg_list.yview)
        self.scrollbar.grid(row = 0, column = 0)
        #self.scrollbar.pack(side=LEFT, fill=BOTH)
        #Allows message list to be scrolled
        self.msg_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.set(0.3,1)
        self.msg_list.grid(row = 0, column = 1)
        #self.msg_list.pack(side=RIGHT, expand=True)
        self.text_entry = Entry(master)
        self.text_entry.grid(row = 1, column = 1)
        #self.text_entry.pack(side=BOTTOM)
        self.send_button = Button(master, text="SEND")
        self.send_button.grid(row = 1, column = 2, padx = 1)
        #self.send_button.pack(side=BOTTOM)
        self.send_button.config(command=self.check_button())
        self.is_clicked=False
        self.master.mainloop()
        # Create a socket object 
        self.s = socket.socket() 
        # Define the port on which you want to connect 
        self.port = 5555
        #Loops for IP input until valid IP is received
        while(1):
            print("Servers IP Address, or enter 0 to use default server:" )
            while(self.is_clicked==False):
                pass
            self.server_ipv4 = self.text_entry.get()
            #self.server_ipv4 = input("Servers IP Address, or enter 0 to use default server:  ")
            if(self.server_ipv4=='0'):
                self.server_ipv4 = '34.231.214.96'
            print("Server_ipv4: ",self.server_ipv4)
            try:
                self.s.connect((self.server_ipv4, self.port))
                break
            except:
                print('Invalid IP Address')
        #Receives input from server to activate username send
        self.s.recv(4096)
        self.userName = input('Enter your username: ')
        self.s.send(self.userName.encode('utf-8'))
        # Receives password salt from server
        pass_salt = self.s.recv(4096)
        # Sends hashed password to server
        password = input('Enter your password: ')
        pass_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), pass_salt, 100000, dklen = 128)
        self.s.send(pass_hash)
        # Loops while sign in data is invalid
        while(1):
            if self.s.recv(4096).decode('utf-8') == 'connect':
                print('Connected!')
                break
            print('looping')
            self.s.recv(4096)
            self.userName = input('Enter your username: ')
            self.s.send(self.userName.encode('utf-8'))
            pass_salt = self.s.recv(4096)
            password = input('Enter your password: ')
            pass_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), pass_salt, 100000, dklen = 128)
            self.s.send(pass_hash)

        threading.Thread(target=self.send_msg).start()
        threading.Thread(target=self.recv_msg).start()
        
    def __repr__(self):
        print("Username: {}, Host IP: {}, Host Port: {}".format(self.userName, self.server_ipv4, self.port))
    def check_button(self):
        self.is_clicked=True
    #Send message to server
    def send_msg(self):
        while(1):
            self.message = sys.stdin.readline() 
            self.message = self.window.text_entry.get()
            self.message_send = "<{}>".format(self.userName)+self.message
            self.s.send(self.message_send.encode('utf-8')) 
            sys.stdout.write("<You> ") 
            sys.stdout.write(self.message) 
            #Inserts message to gui
            format_string = "<You> {}".format(self.message)
            self.window.msg_list.insert(END, format_string)
            sys.stdout.flush() 
        s.close()

    def recv_msg(self):
        while True:
            data = self.s.recv(4096)
            if data:
                format_string = data.decode('utf-8')
                self.window.msg_list.insert(END, format_string)
            else:
                pass

class chatInterface:
    def __init__(self, master):             #Occurs as soon as your create an object
        self.master = master
        top_frame = Frame(master)           #Frame for data
        self.print_button = Button(text="Click to be greeted", command=self.printMessage)
        #self.print_button.pack(side=BOTTOM)
        #Creates message list variable
        self.msg_list = Listbox(height=15, width=50)
        #Creates scroll bar variable
        self.scrollbar = Scrollbar(master, command=self.msg_list.yview)
        self.scrollbar.grid(row = 0, column = 0)
        #self.scrollbar.pack(side=LEFT, fill=BOTH)
        #Allows message list to be scrolled
        self.msg_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.set(0.3,1)
        self.msg_list.grid(row = 0, column = 1)
        #self.msg_list.pack(side=RIGHT, expand=True)
        self.text_entry = Entry(master)
        self.text_entry.grid(row = 1, column = 1)
        #self.text_entry.pack(side=BOTTOM)
        self.send_button = Button(master, text="SEND")
        self.send_button.grid(row = 1, column = 2, padx = 1)
        #self.send_button.pack(side=BOTTOM)


    def printMessage(self):
        print("Welcome")

#Create GUI object for chat room
window = Tk()                                             #Creates blank window
#client_interface = chatInterface(window)                          #Need an object to do stuff in class

#Keeps window continuously on screen, hence main loop for the GUI      

#window.mainloop() 
#Create clientSocket() objext client1
client1 = clientSocket(window)
  

                                 