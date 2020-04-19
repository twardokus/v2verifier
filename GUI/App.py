from tkinter.ttk import Frame
import tkinter as tk
from PIL import Image
import ImageTk
from PIL import ImageTk

# try:
#     # Python2
#     import Tkinter as tk
# except ImportError:
#     # Python3
#     #import tkinter as tk
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
img = ImageTk.PhotoImage(Image.open("./pic/Car1.png"))
#  load = Image.open("./pic/Car1.jpg")
canvas.create_image(50, 50, image=img, anchor=tk.CENTER)

Car2 = ImageTk.PhotoImage(Image.open("./pic/Car2.png"))
canvas.create_image(700, 450, image=Car2, anchor=tk.CENTER)

#adds output panel on right
textWidget = tk.Text(root, height=800, width=500)
textWidget.pack(side=tk.RIGHT)

textWidget.tag_configure("green", foreground="green")
textWidget.insert(tk.END, "Testing 123\n", "green")
textWidget.tag_configure("orange", foreground="orange")
textWidget.insert(tk.END, "Testing 123\n", "orange")


root.mainloop()
