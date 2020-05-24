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


class GUI:
	

	def __init__(self, root):

		self.threadlock = threading.Lock()
		self.receivedPacketCount = 0
		self.processedPacketCount = 0
		self.authenticatedPacketCount = 0
		self.intactPacketCount = 0
		self.ontimePacketCount = 0

		self.root = root
		root.title("V2X Communications - Security Testbed")	

		self.root.grid_rowconfigure(1, weight=1)
		self.root.grid_columnconfigure(1, weight=1)

		CANVAS_HEIGHT = 600
		CANVAS_WIDTH = 800

		# create the drawing canvas
		self.canvas = tk.Canvas(root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg='#7E7E7E')

		# create textbox to display messages
		self.textWidget = tk.Text(root, height=300,font=36, bg="white", borderwidth=2)

		self.textWidget.tag_configure("valid", foreground="green")
		self.textWidget.tag_configure("attack", foreground="red")
		self.textWidget.tag_configure("information", foreground="orange")

		# create another textbox to display counters
		self.counters = tk.Text(root,font=36,bg="white",borderwidth=2)

		# draw horizontal lines on the canvas
		x1 = 0
		x2 = CANVAS_WIDTH
		for k in range(0, CANVAS_HEIGHT, 50):
			y1 = k
			y2 = k

			self.canvas.create_line(x1, y1, x2, y2, fill="#000000")

		# draw vertical lines
		y1 = 0
		y2 = CANVAS_HEIGHT
		for k in range(0, CANVAS_WIDTH, 50):
			x1 = k
			x2 = k
			self.canvas.create_line(x1, y1, x2, y2, fill="#000000")

		self.textWidget.grid(row=1,column=0,columnspan=2,)
		self.canvas.grid(row=0,column=0,sticky="nw")
		self.counters.grid(row=0,column=1,sticky="n")

		receive_thread = Thread(target=self.receive)
		receive_thread.start()

		#counter_thread = Thread(target=self.printCounters)
		#counter_thread.start()

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
	def receive(self):

		while True:
			try:
				msg = c.recv(BUFSIZ).decode()

				self.receivedPacketCount += 1

				# decode the JSON string
				data = json.loads(msg)

				self.intactPacketCount += 1

				#self.newPacket(0, data['x'], data['y'], data['heading'], data['sig'], data['recent'], data['receiver'], data['elapsed'])

				if data['sig']:
					self.authenticatedPacketCount += 1
				if data['recent']:
					self.ontimePacketCount += 1

				update = Thread(target=self.newPacket, args=(self.threadlock, 0, data['x'], data['y'], data['heading'], data['sig'], data['recent'], data['receiver'], data['elapsed'],))
				update.start()


			except json.decoder.JSONDecodeError as jsonError:
				print(msg)
				print("JSON decoding error - invalid data. Discarding.")
			except Exception as e:
				print("=====================================================================================")
				print("Error processing packet. Exception type:")
				print(type(e))
				print("")
				print("Error message:")
				print(e)
				print("End error message")
				print("=====================================================================================")


	def newPacket(self, lock, carid, x, y, heading, isValid, isRecent, isReceiver, elapsedTime):
		
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

		self.canvas.create_image(x, y, image=i, anchor=tk.CENTER, tags="car" + str(threading.currentThread().ident))
		
		with lock:
			# print results
			if not isReceiver:
				check = u'\u2713'
				rejected = u'\u2716'
				
				self.textWidget.insert(tk.END, "==========================================\n","black")
				if isValid:
					
					self.textWidget.insert(tk.END, check + "Message successfully authenticated\n","valid")
				else:
					self.textWidget.insert(tk.END, rejected + "Invalid signature!\n","attack")
				
				if isRecent:
					self.textWidget.insert(tk.END, check + "Message is recent: " + str(round(elapsedTime,2)) + " micoseconds elapsed since transmission\n","valid")
				else:	
					self.textWidget.insert(tk.END, rejected + "Message out-of-date: " + str(round(elapsedTime,2)) + " micoseconds elapsed since transmission\n","information")
				
				if not isValid and not isRecent:
					self.textWidget.insert(tk.END, rejected + "!!!--- Invalid signature AND message expired: replay attack likely! ---!!!\n","attack")
				
				self.textWidget.insert(tk.END, "Vehicle reports location at (" + str(x) + "," + str(y) + "), traveling " + heading + "\n", "black")

				self.textWidget.insert(tk.END, "==========================================\n","black")
				self.textWidget.see(tk.END)
		if isReceiver:
			time.sleep(0.1)
		else:		
			time.sleep(0.5)
		self.canvas.delete("car" + str(threading.currentThread().ident))
		self.processedPacketCount += 1

	def printCounters(self):
		while True:
			print(str(self.receivedPacketCount))
			print(str(self.processedPacketCount))
			print(str(self.authenticatedPacketCount))
			print(str(self.intactPacketCount))
			print(str(self.ontimePacketCount))
			time.sleep(2)

if __name__=="__main__":
	s = socket()
	port = 6666
	s.bind(('127.0.0.1',port))
	s.listen(4)
	c, addr = s.accept()

	BUFSIZ = 200

	root = tk.Tk()
	gui = GUI(root)
	root.mainloop()

	
