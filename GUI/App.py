from tkinter.ttk import Frame
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time


class Car:
    def __init__(self, CarID, name, x, y, pic):
        self.CarID = CarID
        self.name = name
        self.x = x
        self.y = y
        self.pic = pic

# used to determine if a new car has been added
# key: Car ID, value: Car object
carDict = {}


# helper function for whatPos
def setPicCoord(c, pic, x, y):
    c.pic = pic
    c.x = x
    c.y = y


# updates the coordinates and picture of the Car object
# based on the direction it has moved.
def whatPos(c, x, y):
    if c.x < x and c.y < y:
        setPicCoord(c, c.name + "NE.png", x, y)
    elif c.x > x and c.y < y:
        setPicCoord(c, c.name + "NW.png", x, y)
    elif c.x < x and c.y > y:
        setPicCoord(c, c.name + "SE.png", x, y)
    elif c.x > x and c.y > y:
        setPicCoord(c, c.name + "SW.png", x, y)
    elif c.x < x and c.y == y:
        setPicCoord(c, c.name + "E.png", x, y)
    elif c.x > x and c.y == y:
        setPicCoord(c, c.name + "W.png", x, y)
    elif c.x == x and c.y < y:
        setPicCoord(c, c.name + "N.png", x, y)
    else:
        setPicCoord(c, c.name + "S.png", x, y)


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


root.mainloop()
