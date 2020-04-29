from tkinter.ttk import Frame
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import math

class Car:
    def __init__(self, CarID, name, x, y, pic, i, tag):
        self.CarID = CarID
        self.name = name
        self.x = x
        self.y = y
        self.pic = pic
        self.i = i
        self.tag = tag  # color for text

# used to determine if a new car has been added
# key: Car ID, value: Car object
carDict = {}
colors = ["green", "orange", "purple", "blue", "black", "red"]

<<<<<<< HEAD
'''
=======

>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
def receive():
    """Handles receiving of messages."""
    messageCounter = 1
    while True:
        try:
            msg = c.recv(BUFSIZ).decode()
            messageCounter += 1 
            # Throw out invalid length messages - occasional result of TCP segments
            # being received too close together and thrown in same buffer
           # if len(msg) > 25:
            #    continue
            if messageCounter % 2 == 0:
                data = msg.split(",")
                newPacket(int(data[0]),True if data[3] == "True" else False,data[1],data[2])
        except Exception as e:
            print(type(e))
            print(e)
<<<<<<< HEAD
'''
=======

>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc

# helper function for whatPos
def setPicCoord(c, pic, x, y):
    carDict[c].pic = pic
    carDict[c].x = x
    carDict[c].y = y
    carDict[c].i = ImageTk.PhotoImage(Image.open(carDict[c].pic))


# updates the coordinates and picture of the Car object
# based on the direction it has moved.
def whatPos(c, x, y):
    if carDict[c].x < x and carDict[c].y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "NW.png", x, y)
    elif carDict[c].x > x and carDict[c].y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "NE.png", x, y)
    elif carDict[c].x < x and carDict[c].y > y:
        setPicCoord(c, "pic/" + carDict[c].name + "SW.png", x, y)
    elif carDict[c].x > x and carDict[c].y > y:
        setPicCoord(c, "pic/" + carDict[c].name + "SE.png", x, y)
    elif carDict[c].x < x and carDict[c].y == y:
        setPicCoord(c, "pic/" + carDict[c].name + "W.png", x, y)
    elif carDict[c].x > x and carDict[c].y == y:
        setPicCoord(c, "pic/" + carDict[c].name + "E.png", x, y)
    elif carDict[c].x == x and carDict[c].y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "S.png", x, y)
    else:
        setPicCoord(c, "pic/" + carDict[c].name + "N.png", x, y)


root = tk.Tk()
root.title("Secure V2V Communication Simulator")
#root.state("zoomed")  # makes full screen
topFrame = Frame(root, width=700, height=300)  # Added "container" Frame.
topFrame.pack(side=tk.LEFT)
# create the drawing canvas
canvas = tk.Canvas(topFrame, width=800, height=800, bg='#25343F')
canvas.pack()

# draw horizontal lines
x1 = 0
x2 = 800
for k in range(0, 800, 50):
    y1 = k
    y2 = k
    canvas.create_line(x1, y1, x2, y2, fill="#B8CAD6")

# draw vertical lines
y1 = 0
y2 = 800
for k in range(0, 800, 50):
    x1 = k
    x2 = k
    canvas.create_line(x1, y1, x2, y2, fill="#B8CAD6")


# adds output panel on right
textWidget = tk.Text(root, height=800, width=500, font=36)
textWidget.pack(side=tk.RIGHT)
<<<<<<< HEAD
textWidget.tag_configure("valid", foreground="green")
textWidget.tag_configure("invalid", foreground="red")
=======
>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc

def isValid(valid, carid):
    check = u'\u2713'
    nope = u'\u2716'
    if valid:
        textWidget.insert(tk.END, check + " Message from Car:" + str(carid) + " has been successfully authenticated\n",
<<<<<<< HEAD
                          "valid")
    else:
        textWidget.insert(tk.END, nope + " Message from Car:" + str(carid) + " has failed authentication\n",
                          "invalid")
=======
                          carDict[carid].tag)
    else:
        textWidget.insert(tk.END, nope + " Message from Car:" + str(carid) + " has failed authentication\n",
                          carDict[carid].tag)
>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc


# adds to new car to dictionary if not been seen before
# sends to whatPos function to update x, y and pic
# modelled after trace file in mycourses
def newPacket(carid, valid, x, y):

    """
    newx = int(x)
    newy = int(y)

    newx = (newx - 8500)/2
    newy = (newy - 8000)/2
    """

    newx = abs(int(x)) -150
    newy = int(y) - 3561
    newx = newx * 2
    newy = newy * 2
    #print ("x: " + str(newx))
    #print ("y: " + str(newy))
    #print ("Valid? " + str(valid))
    #print("Entered newPacket")
    if carid in carDict:
        if valid:
            canvas.delete(carDict[carid].i)
            whatPos(carid, newx, newy)
            canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
            print("image: " + carDict[carid].name)
        isValid(valid, carid)
        textWidget.tag_configure(carDict[carid].tag, foreground=carDict[carid].tag)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(newx) + "," + str(newy) + ")\n", carDict[carid].tag)
        textWidget.see(tk.END)
    else:
<<<<<<< HEAD
        colortag = colors[len(carDict)+2]
        length = len(carDict) + 3
=======
        colortag = colors[len(carDict)]
        length = len(carDict) + 1
>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc
        name = "Car" + str(length)
        pic = name + "N.png"
        c = Car(carid, name, newx, newy, pic, ImageTk.PhotoImage(Image.open("pic/" + name + "N.png")), colortag)
        carDict[carid] = c
<<<<<<< HEAD
        canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
=======
        #canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc
        isValid(valid, carid)
        textWidget.tag_configure(carDict[carid].tag, foreground=carDict[carid].tag)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n", carDict[carid].tag)
        textWidget.see(tk.END)

<<<<<<< HEAD
'''
=======

>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc
s = socket()
port = 6666
s.bind(('127.0.0.1',port))
s.listen(4)
c, addr = s.accept()


"""


HOST = '127.0.0.1'
PORT = 6666
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
"""
BUFSIZ = 105
"""
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
"""

receive_thread = Thread(target=receive)
receive_thread.start()

'''
newPacket(1, True, -293, 3779)
newPacket(2, False, -285, 3638)
newPacket(1, False, -293, 3776)
newPacket(2, True, -283, 3642)
<<<<<<< HEAD

=======
'''
>>>>>>> 045b2f4693dc9913f0eed4a1def3794c10bd7ccc
root.mainloop()


