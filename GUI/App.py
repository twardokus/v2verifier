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

# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
def receive():
	"""Handles receiving of messages."""
	messageCounter = 1
	while True:
		try:
			msg = c.recv(BUFSIZ).decode()
			print(msg)
			messageCounter += 1 
			# Throw out invalid length messages - occasional result of TCP segments
			# being received too close together and thrown in same buffer
		   # if len(msg) > 25:
			#	continue
			if messageCounter % 2 == 0:
				data = msg.split(",")
				print(data)
				newPacket(0,data[2],True if data[3] == "True" else False,data[0],data[1])
		except Exception as e:
			print(type(e))
			print(e)

# helper function for whatPos
def setPicCoord(c, pic, x, y):
	carDict[c].pic = pic
	carDict[c].x = x
	carDict[c].y = y
	carDict[c].i = ImageTk.PhotoImage(Image.open(carDict[c].pic))


# updates the coordinates and picture of the Car object
# based on the direction it has moved.
def whatPos(c, x, y, heading, valid):
	if valid:
		setPicCoord(c, "pic/" + heading + ".png", x, y)
	else:
		setPicCoord(c, "pic/phantom/" + heading + ".png", x, y)


root = tk.Tk()
root.title("Secure V2V Communication Simulator")
#root.state("zoomed")  # makes full screen
topFrame = Frame(root, width=700, height=300)  # Added "container" Frame.
topFrame.pack(side=tk.LEFT)
# create the drawing canvas
#canvas = tk.Canvas(topFrame, width=800, height=800, bg='#25343F')
canvas = tk.Canvas(topFrame, width=800, height=800, bg='#7E7E7E')
canvas.pack()
canvas.pack()

# draw horizontal lines
x1 = 0
x2 = 800
for k in range(0, 800, 50):
	y1 = k
	y2 = k

	canvas.create_line(x1, y1, x2, y2, fill="#000000")

# draw vertical lines
y1 = 0
y2 = 800
for k in range(0, 800, 50):
	x1 = k
	x2 = k
	canvas.create_line(x1, y1, x2, y2, fill="#000000")


# adds output panel on right
textWidget = tk.Text(root, height=800, width=500, font=36)
textWidget.pack(side=tk.RIGHT)
textWidget.tag_configure("valid", foreground="green")
textWidget.tag_configure("invalid", foreground="red")

def isValid(valid, carid):
	check = u'\u2713'
	nope = u'\u2716'
	if valid:
		textWidget.insert(tk.END, "===================================\n","valid")
		textWidget.insert(tk.END, check + " Message from Car " + str(carid) + " has been successfully authenticated\n","valid")
	else:
		textWidget.insert(tk.END, "===================================\n","invalid")
		textWidget.insert(tk.END, nope + " Message from Car " + str(carid) + " is unsigned or incorrectly formatted. Ignoring message!\n","invalid")

# adds to new car to dictionary if not been seen before
# sends to whatPos function to update x, y and pic
# modelled after trace file in mycourses
def newPacket(carid, heading, valid, x, y):

	newx = x
	newy = y

	if carid in carDict:
		canvas.delete(carDict[carid].i)
		whatPos(carid, newx, newy, heading,valid)
		canvas.create_image(carDict[carid].x, carDict[carid].y, image=carDict[carid].i, anchor=tk.CENTER)
		isValid(valid, carid)
		textWidget.tag_configure(carDict[carid].tag, foreground=carDict[carid].tag)
		textWidget.insert(tk.END, "Car " + str(carid) + " is at location (" + str(newx) + "," + str(newy) + ")\n", carDict[carid].tag)
		textWidget.see(tk.END)
	else:
		print("Here")
		colortag = "red"
		length = 0
		
		name = "Car" + str(length)
		pic = "pic/" + heading + ".png"
		c = Car(carid, name, newx, newy, pic, ImageTk.PhotoImage(Image.open(pic)), colortag)
		carDict[carid] = c
		
		isValid(valid, carid)
		textWidget.tag_configure(carDict[carid].tag, foreground=carDict[carid].tag)
		textWidget.insert(tk.END, "Car " + str(carid) + " is at location (" + str(x) + "," + str(y) + ")\n", carDict[carid].tag)
		textWidget.see(tk.END)


s = socket()
port = 6666
s.bind(('127.0.0.1',port))
s.listen(4)
c, addr = s.accept()

BUFSIZ = 105

receive_thread = Thread(target=receive)
receive_thread.start()

root.mainloop()


