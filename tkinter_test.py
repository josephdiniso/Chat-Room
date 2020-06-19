from tkinter import *

master = Tk()


listbox = Listbox(master)
scrollbar = Scrollbar(listbox)
scrollbar.pack(side=LEFT, fill=Y)
listbox.pack()

listbox.insert(END, "a list entry")

listy = "hello my name is joseph and I really like to type into lists like these because I can type a lot of words"
listy = listy.split()
for item in listy:
    listbox.insert(END, item)

mainloop()