# using the Tkinter canvas to
# draw a line from coordinates x1,y1 to x2,y2
# create_line(x1, y1, x2, y2, width=1, fill="black")
from tkinter.ttk import Frame

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
root = tk.Tk()
root.title("Secure V2V Communication Simulator")
root.state("zoomed")  # makes full screen

topFrame = Frame(root, width=1400, height=800)  # Added "container" Frame.
topFrame.pack(side=tk.LEFT)  # side=RIGHT, fill=X, expand=1, anchor=N)
# create the drawing canvas
#canvas = tk.Canvas(root, width=900, height=800, bg='#25343F')
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

textWidget = tk.Text(root, height=800, width=500)
textWidget.pack(side=tk.RIGHT)
textWidget.insert(tk.END, "Testing 123")


root.mainloop()
