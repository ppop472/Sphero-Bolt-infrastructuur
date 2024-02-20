import tkinter as tk
import threading
import os

def open_controllertest():
    threading.Thread(target=run_script, args=("controller.py",)).start()

def open_interface():
    threading.Thread(target=run_script, args=("interface.py",)).start()

def run_script(script_name):
    os.system(f"python {script_name}")

root = tk.Tk()
root.title("Open and Close Python Scripts")

controllertest_button = tk.Button(root, text="Open controllertest.py", command=open_controllertest)
controllertest_button.pack(pady=10)

interface_button = tk.Button(root, text="Open interface.py", command=open_interface)
interface_button.pack(pady=10)

root.mainloop()
