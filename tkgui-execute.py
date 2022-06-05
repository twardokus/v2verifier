import tkinter as tk
from v2verifier_python.TkGUI import TkGUI

if __name__ == "__main__":
    root = tk.Tk()
    gui = TkGUI(root)
    gui.run_gui_receiver()
    print("GUI Initialized...")
    root.mainloop()
