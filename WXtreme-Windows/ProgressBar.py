import tkinter as tk
from tkinter import ttk
import os

def ProgressBar(ThreadStatus):

    workingdir = os.getcwd()

    def tryClose():
        if ThreadStatus.is_set():
            root.destroy()
        root.after(100, tryClose)


    root = tk.Tk()
    root.geometry('300x80')
    root.title('Generating Graph...')
    root.iconbitmap(f'{workingdir}\\icon.ico')

    root.grid()

    # progressbar
    pb = ttk.Progressbar(
        root,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )
    # place the progressbar
    pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

    pb.start()

    tryClose()

    root.mainloop()
