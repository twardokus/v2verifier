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

'''
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

'''


# helper function for whatPos
def setPicCoord(c, pic, x, y):
    print("Entered setPicCoord")
    carDict[c].pic = pic
    carDict[c].x = x
    carDict[c].y = y
    carDict[c].i = ImageTk.PhotoImage(Image.open(carDict[c].pic))


# updates the coordinates and picture of the Car object
# based on the direction it has moved.
def whatPos(c, x, y):
    print("Entered whatPos")
    if carDict[c].x < x and carDict[c].y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "NE.png", x, y)
    elif carDict[c].x > x and carDict[c].y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "NW.png", x, y)
    elif carDict[c].x < x and carDict[c].y > y:
        setPicCoord(c, "pic/" + carDict[c].name + "SE.png", x, y)
    elif carDict[c].x > x and carDict[c].y > y:
        setPicCoord(c, "pic/" + carDict[c].name + "SW.png", x, y)
    elif carDict[c].x < x and carDict[c].y == y:
        setPicCoord(c, "pic/" + carDict[c].name + "E.png", x, y)
    elif carDict[c].x > x and carDict[c].y == y:
        setPicCoord(c, "pic/" + carDict[c].name + "W.png", x, y)
    elif carDict[c].x == x and carDict[c].y < y:
        setPicCoord(c, "pic/" + carDict[c].name + "N.png", x, y)
    else:
        setPicCoord(c, carDict[c].name + "S.png", x, y)


root = tk.Tk()
root.title("Secure V2V Communication Simulator")
root.state("zoomed")  # makes full screen
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
    newx = int(x)
    newy = int(y)

#    print(str(x))
#    print(str(y))

    newx = (newx - 8500)/2
    newy = (newy - 8000)/2

    print("Entered newPacket")
    if carid in carDict:
        canvas.delete(carDict[carid].i)
        whatPos(carid, newx, newy)
        canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
        print("image: " + carDict[carid].name)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n")
        textWidget.see(tk.END)
    else:
        length = len(carDict) + 1
        name = "Car" + str(length)
        pic = name + "N.png"
        c = Car(carid, name, newx, newy, pic, ImageTk.PhotoImage(Image.open("pic/" + name + "N.png")))
        carDict[carid] = c
        canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
        textWidget.insert(tk.END, "Car:" + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n")
        textWidget.see(tk.END)

'''
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

newPacket(1, "hello", 9786, 8105)
newPacket(2, "hello", 10283, 8216)
newPacket(1, "hello", 9374, 9000)
newPacket(2, "hello", 8666, 8105)
root.mainloop()


