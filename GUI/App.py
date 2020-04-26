from tkinter.ttk import Frame
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Car:
    def __init__(self, CarID, name, x, y, pic, i):
        self.CarID = CarID
        self.name = name
        self.x = x
        self.y = y
        self.pic = pic
        self.i = i

# used to determine if a new car has been added
# key: Car ID, value: Car object
carDict = {}


# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg.insert(tk.END, msg)
        except OSError:  # Possibly disconnected?
            break


# helper function for whatPos
def setPicCoord(c, pic, x, y):
    c.pic = pic
    c.x = x
    c.y = y
    c.i = ImageTk.PhotoImage(Image.open(c.name))


# updates the coordinates and picture of the Car object
# based on the direction it has moved.
def whatPos(c, x, y):
    if c.x < x and c.y < y:
        setPicCoord(c, "pic/" + c.name + "NE.png", x, y)
    elif c.x > x and c.y < y:
        setPicCoord(c, "pic/" + c.name + "NW.png", x, y)
    elif c.x < x and c.y > y:
        setPicCoord(c, "pic/" + c.name + "SE.png", x, y)
    elif c.x > x and c.y > y:
        setPicCoord(c, "pic/" + c.name + "SW.png", x, y)
    elif c.x < x and c.y == y:
        setPicCoord(c, "pic/" + c.name + "E.png", x, y)
    elif c.x > x and c.y == y:
        setPicCoord(c, "pic/" + c.name + "W.png", x, y)
    elif c.x == x and c.y < y:
        setPicCoord(c, "pic/" + c.name + "N.png", x, y)
    else:
        setPicCoord(c, "pic/" + c.name + "S.png", x, y)
    return c



root = tk.Tk()
root.title("Secure V2V Communication Simulator")
#root.state("zoomed")  # makes full screen

topFrame = Frame(root, width=1400, height=800)  # Added "container" Frame.
topFrame.pack(side=tk.LEFT)
# create the drawing canvas
canvas = tk.Canvas(topFrame, width=900, height=800, bg='#25343F')
canvas.pack()

# draw horizontal lines
x1 = 0
x2 = 900
for k in range(0, 800, 50):
    y1 = k
    y2 = k
    canvas.create_line(x1, y1, x2, y2, fill="#B8CAD6")
# draw vertical lines
y1 = 0
y2 = 800
for k in range(0, 900, 50):
    x1 = k
    x2 = k
    canvas.create_line(x1, y1, x2, y2, fill="#B8CAD6")


# adds output panel on right
textWidget = tk.Text(root, height=800, width=500, font=36)
textWidget.pack(side=tk.RIGHT)


# adds to new car to dictionary if not been seen before
# sends to whatPos function to update x, y and pic
# modelled after trace file in mycourses
def newPacket(carid, message, x, y):
    if carid in carDict:
        canvas.delete(carDict[carid].i)
        c = whatPos(carDict[carid], x, y)
        canvas.create_image(c.x, c.y, image=c.i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n")
    else:
        length = len(carDict) + 1
        name = "Car" + str(length)
        pic = name + "N.png"
        c = Car(carid, "pic/" + name + "N.png", x, y, pic, ImageTk.PhotoImage(Image.open("pic/" + name + "N.png")))
        carDict[carid] = c
        canvas.create_image(c.x, c.y, image=c.i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n")


newPacket(1, "hello", 50, 40)
newPacket(2, "hello2", 90, 100)

newPacket(1, "bye", 400, 500)
newPacket(2, "bye2", 350, 200)
HOST = '127.0.0.1'
PORT = 6666
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

root.mainloop()


# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
# while True:
#     data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
#     print("received message:", data)
#

