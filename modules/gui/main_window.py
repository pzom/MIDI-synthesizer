import tkinter as tk
from tkinter import ttk


def CreateMainWindow():

    root = tk.Tk()
    root.title("Hello World")
    root.geometry("400x200")
    root.config(bg="skyblue")
    AddFrame(root, 200, 100, 10, 10, tk.X, tk.TOP, bg="red")
    AddFrame(root, 9999, 9999, 10, 0, tk.Y, tk.BOTTOM, bg="yellow")
    root.mainloop()

def AddFrame(window, wd, ht, padx, pady, fill, side, bg):
    frame = tk.Frame(window, width=wd, height=ht, bg=bg)
    frame.pack(padx=padx, pady=pady, fill=fill,side=side )
    
