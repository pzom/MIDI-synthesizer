import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Hello World")
root.geometry("400x200")
label = ttk.Label(root, text="Hello World!", font=("Arial", 16))
label.pack(expand=True)
root.mainloop()


