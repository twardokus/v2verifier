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
#            print("Entered receive block")
            msg = c.recv(BUFSIZ).decode()
            # msg "0,9999,9999"
            # msg "0,9999,99990,9999,9999"
            # msg "0,10000,10000"
            if len(msg) > 15:
                continue
            #print(msg)
            #print("Received data")
            data = msg.split(",")
            #print(data[1])
            #print(data[2])
            newPacket(int(data[0]),"",data[1],data[2])
#textWidget.insert(tk.END, msg)
#            print("Exiting try block")
        except Exception as e:
            print(type(e))

#        except OSError:  # Possibly disconnected?
#            print("Hit EXCEPT block - possible OSError")
#        finally:
#            print("Error!! in finally block of receive()")
#            exit(1)


# helper function for whatPos
def setPicCoord(c, pic, x, y):
    print("Entered setPicCoord")
    carDict[c].pic = pic
    carDict[c].x = x
    carDict[c].y = y
    carDict[c].i = ImageTk.PhotoImage(Image.open(c.name))


# updates the coordinates and picture of the Car object
# based on the direction it has moved.
def whatPos(c, x, y):
    print("Entered whatPos")
    if c.x < x and c.y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "NE.png", x, y)
    elif c.x > x and c.y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "NW.png", x, y)
    elif c.x < x and c.y > y:
        setPicCoord(c, "pic/" + carDict[c].name + "SE.png", x, y)
    elif c.x > x and c.y > y:
        setPicCoord(c, "pic/" + carDict[c].name + "SW.png", x, y)
    elif c.x < x and c.y == y:
        setPicCoord(c, "pic/" + carDict[c].name + "E.png", x, y)
    elif c.x > x and c.y == y:
        setPicCoord(c, "pic/" + carDict[c].name + "W.png", x, y)
    elif c.x == x and c.y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "N.png", x, y)
    else:
        setPicCoord(c, "pic/" + carDict[c].name + "S.png", x, y)


root = tk.Tk()
root.title("Secure V2V Communication Simulator")
#root.state("zoomed")  # makes full screen
print("Line 75")
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
textWidget.yview_pickplace("end")
textWidget.pack(side=tk.RIGHT)


# adds to new car to dictionary if not been seen before
# sends to whatPos function to update x, y and pic
# modelled after trace file in mycourses
def newPacket(carid, message, x, y):
    
    print("x and y into newPacket")
    print(x)
    print(y)
    print("==============")

    x = int(x)
    y = int(y)

#    print(str(x))
#    print(str(y))

    x = (x - 8500)/2
    y = (y - 8000)/2

    print(str(x))
    print(str(y))

    print("Entered newPacket")
    if carid in carDict:
        canvas.delete(carDict[carid].i)
        whatPos(carid, x, y)
        canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n")
    else:
        length = len(carDict) + 1
        name = "Car" + str(length)
        pic = name + "N.png"
        c = Car(carid, "pic/" + name + "N.png", x, y, pic, ImageTk.PhotoImage(Image.open("pic/" + name + "N.png")))
        carDict[carid] = c
        canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n")

s = socket()
port = 6666
s.bind(('127.0.0.1',port))
s.listen(4)
c, addr = s.accept()


"""
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
"""
BUFSIZ = 105
"""
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
"""

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

