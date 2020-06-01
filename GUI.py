from tkinter.ttk import *
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
import threading
from threading import Thread
import json
from socket import socket
import yaml

class GUI:

	def __init__(self, root):

		self.threadlock = threading.Lock()
		
		with open("init.yml", "r") as confFile:
			self.config = yaml.load(confFile,Loader=yaml.FullLoader)
		self.numVehicles = self.config["remoteConfig"]["numberOfVehicles"] + 1

		self.receivedPacketCount = 0
		self.processedPacketCount = 0
		self.authenticatedPacketCount = 0
		self.intactPacketCount = 0
		self.ontimePacketCount = 0

		self.receivedPacketCountText = tk.StringVar()
		self.processedPacketCountText = tk.StringVar()
		self.authenticatedPacketCountText = tk.StringVar()
		self.intactPacketCountText = tk.StringVar()
		self.ontimePacketCountText = tk.StringVar()
		self.receivedPacketCountValueText = tk.StringVar()
		self.processedPacketCountValueText = tk.StringVar()
		self.authenticatedPacketCountValueText = tk.StringVar()
		self.intactPacketCountValueText = tk.StringVar()
		self.ontimePacketCountValueText = tk.StringVar()
		self.receivedPacketCountPercentageText = tk.StringVar()
		self.processedPacketCountPercentageText = tk.StringVar()
		self.authenticatedPacketCountPercentageText = tk.StringVar()
		self.intactPacketCountPercentageText = tk.StringVar()
		self.ontimePacketCountPercentageText = tk.StringVar()
		self.vehicleZeroLocationText = tk.StringVar()
		self.vehicleOneLocationText = tk.StringVar()
		self.vehicleTwoLocationText = tk.StringVar()
		self.vehicleThreeLocationText = tk.StringVar()
		self.vehicleFourLocationText = tk.StringVar()
		self.vehicleFiveLocationText = tk.StringVar()
		self.vehicleSixLocationText = tk.StringVar()
		self.vehicleSevenLocationText = tk.StringVar()
		self.vehicleEightLocationText = tk.StringVar()
		self.vehicleNineLocationText = tk.StringVar()
		self.vehicleZeroSpeedText  = tk.StringVar()
		self.vehicleOneSpeedText  = tk.StringVar()
		self.vehicleTwoSpeedText = tk.StringVar()
		self.vehicleThreeSpeedText = tk.StringVar()
		self.vehicleFourSpeedText = tk.StringVar()
		self.vehicleFiveSpeedText = tk.StringVar()
		self.vehicleSixSpeedText = tk.StringVar()
		self.vehicleSevenSpeedText = tk.StringVar()
		self.vehicleEightSpeedText = tk.StringVar()
		self.vehicleNineSpeedText = tk.StringVar()
		self.receiverLocationText = tk.StringVar()
		self.receiverSpeedText = tk.StringVar()
		
		self.root = root
		root.title("V2X Communications - Security Testbed")	

		self.root.grid_rowconfigure(1, weight=1)
		self.root.grid_columnconfigure(1, weight=1)

		CANVAS_HEIGHT = 600
		CANVAS_WIDTH = 800

		# create the drawing canvas
		#self.canvas = tk.Canvas(root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg='#247000')
		self.canvas = tk.Canvas(root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)

		# create textbox to display messages
		self.textWidget = tk.Text(root, height=300,font=36, bg="white", borderwidth=2)

		self.textWidget.tag_configure("valid", foreground="green")
		self.textWidget.tag_configure("attack", foreground="red")
		self.textWidget.tag_configure("information", foreground="orange")

		background = ImageTk.PhotoImage(Image.open("pic/background.jpg"))
		self.backgroundImage = background
		self.canvas.create_image(400, 300, image=self.backgroundImage, anchor=tk.CENTER)

		self.topRight = Frame(root)

		# build the counter window
		self.counters = LabelFrame(self.topRight, text="Packet Statistics")
		self.buildStatisticsLabelFrame()
		
		# build the legend frame
		self.legend = LabelFrame(self.topRight, text="Legend")
		self.buildLegendFrame()

		# build the report frame
		self.report = LabelFrame(self.topRight, text="Vehicle Information")
		self.buildReportFrame()

		# Place core elements on canvas
		self.textWidget.grid(row=1,column=0,columnspan=2,)
		self.canvas.grid(row=0,column=0,sticky="nw")
		self.topRight.grid(row=0,column=1,sticky="new")
		
		# Place subframes inside top right frame
		#self.topRight.grid.rowconfigure(0,weight=1)
		self.topRight.grid_columnconfigure(0,weight=1)
		self.counters.grid(row=0,column=0,sticky="new")
		self.legend.grid(row=1,column=0,sticky="ew")
		self.report.grid(row=2,column=0,sticky="ew")

	
	def runGUIReceiver(self):
		# Start the GUI service on port 6666
		self.s = socket()
		port = 6666
		self.s.bind(('127.0.0.1',port))
		print("Calling receive()")
		
		labelThread = Thread(target=self.updateStatisticsLabels)
		labelThread.start()
		
		self.receiver = Thread(target=self.receive, args=(self.s,))
		self.receiver.start()
		
	def receive(self, s):
		
		s.listen(4)
		c = s.accept()[0]

		BUFSIZ = 200
		
		while True:
			try:
				msg = c.recv(BUFSIZ).decode()
				# decode the JSON string
				data = json.loads(msg)

				self.receivedPacketCount += 1

				self.intactPacketCount += 1

				if data['sig']:
					self.authenticatedPacketCount += 1
				if data['recent']:
					self.ontimePacketCount += 1

				self.updateVehicleInfoLabels(data["id"],"(" + data["x"] + "," + data["y"] + ")", data["speed"])
				update = Thread(target=self.newPacket, args=(self.threadlock, data["id"], data['x'], data['y'], data['heading'], data['sig'], data['recent'], data['receiver'], data['elapsed'],))
				update.start()

			except json.decoder.JSONDecodeError:
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
		x = float(x)
		y = float(y)
		
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
				
				print("time:\t" + str(elapsedTime))
				if isRecent:
					if elapsedTime > 0:
						self.textWidget.insert(tk.END, check + "Message is recent: " + str(round(elapsedTime,2)) + " milliseconds elapsed since transmission\n","valid")
					else:
						self.textWidget.insert(tk.END, check + "Message is recent: 0 milliseconds elapsed since transmission\n","valid")
						#self.textWidget.insert(tk.END, "Message has future timestamp - check clock synchronization!\n", "information")
				else:
					self.textWidget.insert(tk.END, rejected + "Message out-of-date: " + str(round(elapsedTime,2)) + " milliseconds elapsed since transmission\n","information")
				
				if not isValid and not isRecent:
					self.textWidget.insert(tk.END, rejected + "!!!--- Invalid signature AND message expired: replay attack likely! ---!!!\n","attack")
				
				self.textWidget.insert(tk.END, "Vehicle reports location at (" + str(x) + "," + str(y) + "), traveling " + self.headingToDirection(heading) + "\n", "black")

				self.textWidget.insert(tk.END, "==========================================\n","black")
				self.textWidget.see(tk.END)
		time.sleep(0.1)

		self.canvas.delete("car" + str(threading.currentThread().ident))
		self.processedPacketCount += 1

	def updateStatisticsLabels(self):
		while True:
			if self.receivedPacketCount == 0:
				continue
			self.receivedPacketCountText.set("Received:")
			self.processedPacketCountText.set("Processed:")
			self.authenticatedPacketCountText.set("Authentic:")
			self.intactPacketCountText.set("Intact:")
			self.ontimePacketCountText.set("On time:")

			self.receivedPacketCountValueText.set(str(self.receivedPacketCount))
			self.processedPacketCountValueText.set(str(self.processedPacketCount))
			self.authenticatedPacketCountValueText.set(str(self.authenticatedPacketCount))
			self.intactPacketCountValueText.set(str(self.intactPacketCount))
			self.ontimePacketCountValueText.set(str(self.ontimePacketCount))
			
			self.receivedPacketCountPercentageText.set(str(round((self.receivedPacketCount/self.receivedPacketCount)*100,2)) + "%")
			self.processedPacketCountPercentageText.set(str(round((self.processedPacketCount/self.receivedPacketCount)*100,2)) + "%")
			self.authenticatedPacketCountPercentageText.set(str(round((self.authenticatedPacketCount/self.receivedPacketCount)*100,2)) + "%")
			self.intactPacketCountPercentageText.set(str(round((self.intactPacketCount/self.receivedPacketCount)*100,2)) + "%")
			self.ontimePacketCountPercentageText.set(str(round((self.ontimePacketCount/self.receivedPacketCount)*100,2)) + "%")

			time.sleep(0.1)

	def buildStatisticsLabelFrame(self):
		self.receivedPacketCountLabel = Label(self.counters, textvariable=self.receivedPacketCountText)	
		self.processedPacketCountLabel = Label(self.counters, textvariable=self.processedPacketCountText)	
		self.authenticatedPacketCountLabel = Label(self.counters, textvariable=self.authenticatedPacketCountText)	
		self.intactPacketCountLabel = Label(self.counters, textvariable=self.intactPacketCountText)	
		self.ontimePacketCountLabel = Label(self.counters, textvariable=self.ontimePacketCountText)

		self.receivedPacketCountValue = Label(self.counters, textvariable=self.receivedPacketCountValueText)	
		self.processedPacketCountValue = Label(self.counters, textvariable=self.processedPacketCountValueText)	
		self.authenticatedPacketCountValue = Label(self.counters, textvariable=self.authenticatedPacketCountValueText)	
		self.intactPacketCountValue = Label(self.counters, textvariable=self.intactPacketCountValueText)	
		self.ontimePacketCountValue = Label(self.counters, textvariable=self.ontimePacketCountValueText)

		self.receivedPacketCountPercentage = Label(self.counters, textvariable=self.receivedPacketCountPercentageText)	
		self.processedPacketCountPercentage = Label(self.counters, textvariable=self.processedPacketCountPercentageText)	
		self.authenticatedPacketCountPercentage = Label(self.counters, textvariable=self.authenticatedPacketCountPercentageText)	
		self.intactPacketCountPercentage = Label(self.counters, textvariable=self.intactPacketCountPercentageText)	
		self.ontimePacketCountPercentage = Label(self.counters, textvariable=self.ontimePacketCountPercentageText)

		self.receivedPacketCountLabel.grid(row=0, column=0)
		self.processedPacketCountLabel.grid(row=1, column=0)
		self.authenticatedPacketCountLabel.grid(row=2, column=0)
		self.intactPacketCountLabel.grid(row=3, column=0)
		self.ontimePacketCountLabel.grid(row=4, column=0)

		self.receivedPacketCountValue.grid(row=0, column=1, padx=(10,10))
		self.processedPacketCountValue.grid(row=1, column=1, padx=(10,10))
		self.authenticatedPacketCountValue.grid(row=2, column=1, padx=(10,10))
		self.intactPacketCountValue.grid(row=3, column=1, padx=(10,10))
		self.ontimePacketCountValue.grid(row=4, column=1, padx=(10,10))

		self.receivedPacketCountPercentage.grid(row=0, column=2)
		self.processedPacketCountPercentage.grid(row=1, column=2)
		self.authenticatedPacketCountPercentage.grid(row=2, column=2)
		self.intactPacketCountPercentage.grid(row=3, column=2)
		self.ontimePacketCountPercentage.grid(row=4, column=2)
	
	def printCounters(self):
		while True:
			print(str(self.receivedPacketCount))
			print(str(self.processedPacketCount))
			print(str(self.authenticatedPacketCount))
			print(str(self.intactPacketCount))
			print(str(self.ontimePacketCount))
			time.sleep(2)

	def headingToDirection(self, heading):
		if heading == "E":
			return "east"
		elif heading == "NE":
			return "northeast"
		elif heading == "N":
			return "north"
		elif heading == "NW":
			return "northwest"
		elif heading == "W":
			return "west"
		elif heading == "SW":
			return "southwest"
		elif heading == "S":
			return "south"
		elif heading == "SE":
			return "southeast"

	def buildLegendFrame(self):
		self.receiverRowLabel = Label(self.legend, text="  is the receiving vehicle")
		self.otherRowLabel = Label(self.legend, text = "  are vehicles sendings BSMs")
		
		self.receiverImg = ImageTk.PhotoImage(Image.open("pic/receiver/E.png"))
		self.otherImg = ImageTk.PhotoImage(Image.open("pic/E.png"))
		
		self.receiverImage = Label(self.legend, image=self.receiverImg)
		self.otherImage = Label(self.legend, image=self.otherImg)
		
		self.receiverImage.grid(row=0,column=0)
		self.otherImage.grid(row=1,column=0)
		self.receiverRowLabel.grid(row=0,column=1,sticky="w")
		self.otherRowLabel.grid(row=1,column=1,sticky="w")

	def buildReportFrame(self):
		self.totalVehiclesLabel = Label(self.report, text="Total vehicles: " + str(self.numVehicles))

		self.vehicleZeroID = Label(self.report, text="0")
		self.vehicleOneID = Label(self.report, text="1")
		self.vehicleTwoID = Label(self.report, text="2")
		self.vehicleThreeID = Label(self.report, text="3")
		self.vehicleFourID = Label(self.report, text="4")
		self.vehicleFiveID = Label(self.report, text="5")
		self.vehicleSixID = Label(self.report, text="6")
		self.vehicleSevenID = Label(self.report, text="7")
		self.vehicleEightID = Label(self.report, text="8")
		self.vehicleNineID = Label(self.report, text="9")
		self.receiverID = Label(self.report, text="Rcvr.")

		self.vehicleZeroLocation = Label(self.report, textvariable=self.vehicleZeroLocationText)
		self.vehicleOneLocation = Label(self.report, textvariable=self.vehicleOneLocationText)
		self.vehicleTwoLocation = Label(self.report, textvariable=self.vehicleTwoLocationText)
		self.vehicleThreeLocation = Label(self.report, textvariable=self.vehicleThreeLocationText)
		self.vehicleFourLocation = Label(self.report, textvariable=self.vehicleFourLocationText)
		self.vehicleFiveLocation = Label(self.report, textvariable=self.vehicleFiveLocationText)
		self.vehicleSixLocation = Label(self.report, textvariable=self.vehicleSixLocationText)
		self.vehicleSevenLocation = Label(self.report, textvariable=self.vehicleSevenLocationText)
		self.vehicleEightLocation = Label(self.report, textvariable=self.vehicleEightLocationText)
		self.vehicleNineLocation = Label(self.report, textvariable=self.vehicleNineLocationText)
		self.receiverLocation = Label(self.report, textvariable=self.receiverLocationText)
		
		self.vehicleZeroSpeed = Label(self.report, textvariable=self.vehicleZeroSpeedText)
		self.vehicleOneSpeed = Label(self.report, textvariable=self.vehicleOneSpeedText)
		self.vehicleTwoSpeed = Label(self.report, textvariable=self.vehicleTwoSpeedText)
		self.vehicleThreeSpeed = Label(self.report, textvariable=self.vehicleThreeSpeedText)
		self.vehicleFourSpeed = Label(self.report, textvariable=self.vehicleFourSpeedText)
		self.vehicleFiveSpeed = Label(self.report, textvariable=self.vehicleFiveSpeedText)
		self.vehicleSixSpeed = Label(self.report, textvariable=self.vehicleSixSpeedText)
		self.vehicleSevenSpeed = Label(self.report, textvariable=self.vehicleSevenSpeedText)
		self.vehicleEightSpeed = Label(self.report, textvariable=self.vehicleEightSpeedText)
		self.vehicleNineSpeed = Label(self.report, textvariable=self.vehicleNineSpeedText)
		self.receiverSpeed = Label(self.report, textvariable=self.receiverSpeedText)
		
		self.totalVehiclesLabel.grid(row=0,column=1)
		
		self.idLabel = Label(self.report, text="Vehicle ID")
		self.locLabel = Label(self.report, text="Location")
		self.speedLabel = Label(self.report, text="Speed (km/hr)")
		
		self.idLabel.grid(row=1,column=0)
		self.locLabel.grid(row=1,column=1, padx=(10,10))
		self.speedLabel.grid(row=1,column=2)
		
		self.vehicleZeroID.grid(row=2,column=0)
		self.vehicleOneID.grid(row=3,column=0)
		self.vehicleTwoID.grid(row=4,column=0)
		self.vehicleThreeID.grid(row=5,column=0)
		self.vehicleFourID.grid(row=6,column=0)
		self.vehicleFiveID.grid(row=7,column=0)
		self.vehicleSixID.grid(row=8,column=0)
		self.vehicleSevenID.grid(row=9,column=0)
		self.vehicleEightID.grid(row=10,column=0)
		self.vehicleNineID.grid(row=11,column=0)
		self.receiverID.grid(row=12,column=0)

		self.vehicleZeroLocation.grid(row=2,column=1, padx=(10,10))
		self.vehicleOneLocation.grid(row=3,column=1, padx=(10,10))
		self.vehicleTwoLocation.grid(row=4,column=1, padx=(10,10))
		self.vehicleThreeLocation.grid(row=5,column=1, padx=(10,10))
		self.vehicleFourLocation.grid(row=6,column=1, padx=(10,10))
		self.vehicleFiveLocation.grid(row=7,column=1, padx=(10,10))
		self.vehicleSixLocation.grid(row=8,column=1, padx=(10,10))
		self.vehicleSevenLocation.grid(row=9,column=1, padx=(10,10))
		self.vehicleEightLocation.grid(row=10,column=1, padx=(10,10))
		self.vehicleNineLocation.grid(row=11,column=1, padx=(10,10))
		self.receiverLocation.grid(row=12,column=1, padx=(10,10))
		
		self.vehicleZeroSpeed.grid(row=2,column=2)
		self.vehicleOneSpeed.grid(row=3,column=2)
		self.vehicleTwoSpeed.grid(row=4,column=2)
		self.vehicleThreeSpeed.grid(row=5,column=2)
		self.vehicleFourSpeed.grid(row=6,column=2)
		self.vehicleFiveSpeed.grid(row=7,column=2)
		self.vehicleSixSpeed.grid(row=8,column=2)
		self.vehicleSevenSpeed.grid(row=9,column=2)
		self.vehicleEightSpeed.grid(row=10,column=2)
		self.vehicleNineSpeed.grid(row=11,column=2)
		self.receiverSpeed.grid(row=12,column=2)
		
	def updateVehicleInfoLabels(self, vehicleID, location, speed):
		vehicleID = int(vehicleID)
		if vehicleID == 0:
			self.vehicleZeroLocationText.set(location)
			self.vehicleZeroSpeedText.set(str(speed))
		elif vehicleID == 1:
			self.vehicleOneLocationText.set(location)
			self.vehicleOneSpeedText.set(str(speed))
		elif vehicleID == 2:
			self.vehicleTwoLocationText.set(location)
			self.vehicleTwoSpeedText.set(str(speed))
		elif vehicleID == 3:
			self.vehicleThreeLocationText.set(location)
			self.vehicleThreeSpeedText.set(str(speed))
		elif vehicleID == 4:
			self.vehicleFourLocationText.set(location)
			self.vehicleFourSpeedText.set(str(speed))
		elif vehicleID == 5:
			self.vehicleFiveLocationText.set(location)
			self.vehicleFiveSpeedText.set(str(speed))
		elif vehicleID == 6:
			self.vehicleSixLocationText.set(location)
			self.vehicleSixSpeedText.set(str(speed))
		elif vehicleID == 7:
			self.vehicleSevenLocationText.set(location)
			self.vehicleSevenSpeedText.set(str(speed))
		elif vehicleID == 8:
			self.vehicleEightLocationText.set(location)
			self.vehicleEightSpeedText.set(str(speed))
		elif vehicleID == 9:
			self.vehicleNineLocationText.set(location)
			self.vehicleNineSpeedText.set(str(speed))
		elif vehicleID == 99:
			self.receiverLocationText.set(location)
			self.receiverSpeedText.set(str(speed))
