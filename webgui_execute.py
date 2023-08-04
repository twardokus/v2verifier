import python_guis.WebGUI as webgui
import time
import threading

print("Launching V2Verifier receiver with WebGUI...")
gui = webgui.WebGUI()
gui.start_receiver()
gui.prep()
time.sleep(1)
print("WebGUI initialized...")
gui_thread = threading.Thread(target=gui.run)
gui_thread.start()
print("WebGUI launched successfully")
