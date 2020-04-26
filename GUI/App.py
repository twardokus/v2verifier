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

#  img = ImageTK.PhotoImage(Image.open("./pic/Car1.jpg"))
img = ImageTk.PhotoImage(Image.open("pic/Car1N.png"))
#  load = Image.open("./pic/Car1.jpg")
canvas.create_image(50, 50, image=img, anchor=tk.CENTER)

Car2 = ImageTk.PhotoImage(Image.open("pic/Car3NE.png"))
canvas.create_image(700, 450, image=Car2, anchor=tk.CENTER)

#adds output panel on right
textWidget = tk.Text(root, height=800, width=500, font=36)
textWidget.pack(side=tk.RIGHT)

textWidget.tag_configure("green", foreground="green")
textWidget.insert(tk.END, "Car:1 message has authenticated\n", "green")
textWidget.insert(tk.END, "Car:1 is located at (50,50)\n", "green")

textWidget.tag_configure("orange", foreground="purple")
textWidget.insert(tk.END, "Car:2 message has authenticated\n", "orange")
textWidget.insert(tk.END, "Car:2 is located at (700,450)\n", "orange")


# adds to new car to dictionary if not been seen before
# sends to whatPos function to update x, y and pic
# modelled after trace file in mycourses
def newPacket(carid, message, x, y):
    c = Car()
    if carid in carDict:
        canvas.delete(c.i)
        c = whatPos(carDict[carid], x, y)
        canvas.create_image(c.x, c.y, image=c.i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + carid + " is at location (" + x +"," + y + ")")
    else:
        length = len(carDict) + 1
        name = "Car" + str(length)
        pic = name + "N.png"
        c = Car(carid, "pic/" + name + "N.png", x, y, pic)
        c.i = ImageTk.PhotoImage(Image.open(c.name))
        canvas.create_image(c.x, c.y, image=c.i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + carid + " is at location (" + x + "," + y + ")")


HOST = input('Enter host: ')
PORT = input('Enter port: ')
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

#print ("test")

# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
# while True:
#     data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
#     print("received message:", data)
#

