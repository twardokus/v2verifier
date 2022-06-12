#  Copyright (c) 2022. Geoff Twardokus
#  Reuse permitted under the MIT License as specified in the LICENSE file within this project.

import tkinter as tk
from python_guis.TkGUI import TkGUI

if __name__ == "__main__":
    root = tk.Tk()
    gui = TkGUI(root)
    gui.run_gui_receiver()
    print("GUI Initialized...")
    root.mainloop()
