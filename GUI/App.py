from tkinter.ttk import Frame
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
from socket import AF_INET, socket, SOCK_STREAM
import threading
from threading import Thread
import math
import json

class Car:
	def __init__(self, CarID, name, x, y, pic, i, tag):
		self.CarID = CarID
		self.name = name
		self.x = x
		self.y = y
		self.pic = pic
		self.i = i
		self.tag = tag  # color for text
"""
Receive a JSON string 

	decodedData['x'] = BSMData[0]
	decodedData['y'] = BSMData[1]
	decodedData['heading'] = BSMData[2]
	decodedData['sig'] = isValidSig
	decodedData['recent'] = isRecent
	decodedData['receiver'] = False

def newPacket(carid, x, y, heading, isValid, isRecent, isReceiver)

"""
def receive():

	while True:
		try:
			msg = c.recv(BUFSIZ).decode()

			print("Message received: " + msg)
			
			# decode the JSON string
			data = json.loads(msg)
			
			print("JSON decoded message: ",end="")
			print(data)

			update = Thread(target=newPacket, args=(0, data['x'], data['y'], data['heading'], data['sig'], data['recent'], data['receiver'], data['elapsed'],))
			update.start()

			"""
			messageCounter += 1 

			if messageCounter % 2 == 0:
				data = msg.split(",")
				print(data)

				valid = True if data[3] == "True" else False
				update = None
				if len(data) > 5:
					isReceiver = True if data[5] == "True" else False
					update = Thread(target=newPacket, args=(0,data[2],valid,data[0],data[1],data[4],isReceiver,))
				else:
					update = Thread(target=newPacket, args=(0,data[2],valid,data[0],data[1],data[4],))
				update.start()
			"""
		except Exception as e:
			print("=====================================================================================")
			print("Error processing packet. Exception type:")
			print(type(e))
			print("")
			print("Error message:")
			print(e)
			print("End error message")
			print("=====================================================================================")

root = tk.Tk()
root.title("Secure V2V Communication Simulator")
topFrame = Frame(root, width=700, height=300)  # Added "container" Frame.
topFrame.pack(side=tk.TOP)
# create the drawing canvas
canvas = tk.Canvas(topFrame, width=800, height=600, bg='#7E7E7E')
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
textWidget = tk.Text(root, height=200, width=1000, font=36)
textWidget.pack(side=tk.BOTTOM)
textWidget.tag_configure("valid", foreground="green")
textWidget.tag_configure("attack", foreground="red")
textWidget.tag_configure("information", foreground="orange")

def newPacket(carid, x, y, heading, isValid, isRecent, isReceiver, elapsedTime):

	# cast coordinates to integers
	x = int(x)
	y = int(y)
	
	# load the appropriate image, depending on signature validation and whether the packet is local
	i = None
	if isReceiver:
		i = ImageTk.PhotoImage(Image.open("pic/receiver/" + heading + ".png"))
	else:
		if isValid:
			i = ImageTk.PhotoImage(Image.open("pic/" + heading + ".png"))
		else:
			i = ImageTk.PhotoImage(Image.open("pic/phantom/" + heading + ".png"))

	canvas.create_image(x, y, image=i, anchor=tk.CENTER, tags="car" + str(threading.currentThread().ident))
	
	# print results
	if not isReceiver:
		check = u'\u2713'
		rejected = u'\u2716'
		
		textWidget.insert(tk.END, "==========================================\n","black")
		if isValid:
			
			textWidget.insert(tk.END, check + "Message successfully authenticated\n","valid")
		else:
			textWidget.insert(tk.END, rejected + "Invalid signature!\n","attack")
		
		if isRecent:
			textWidget.insert(tk.END, check + "Message is recent: " + str(round(elapsedTime,2)) + " micoseconds elapsed since transmission\n","valid")
		else:	
			textWidget.insert(tk.END, rejected + "Message out-of-date: " + str(round(elapsedTime,2)) + " micoseconds elapsed since transmission\n","information")
		
		if not isValid and not isRecent:
			textWidget.insert(tk.END, rejected + "!!!--- Invalid signature AND message expired: replay attack likely! ---!!!\n","attack")
		
		textWidget.insert(tk.END, "Vehicle reports location at (" + str(x) + "," + str(y) + "), traveling " + heading + "\n", "black")

		textWidget.insert(tk.END, "==========================================\n","black")
		textWidget.see(tk.END)
	
	time.sleep(1)
	canvas.delete("car" + str(threading.currentThread().ident))

s = socket()
port = 6666
s.bind(('127.0.0.1',port))
s.listen(4)
c, addr = s.accept()

BUFSIZ = 200

receive_thread = Thread(target=receive)
receive_thread.start()

root.mainloop()


