from sys import maxsize
import tkinter as tk
from PIL import Image, ImageTk

ROW_HEIGHT = 80
WIDTH = 852
HEIGHT = 480

window = tk.Tk()
window.title('Student Housing Finder')

title_frame = tk.Frame(master=window, width=WIDTH, height=ROW_HEIGHT, bg='red')
frame_L = tk.Frame(master=window, width=WIDTH//2, height=400, bg='yellow')
frame_R = tk.Frame(master=window, width=WIDTH//2, height=400, bg='blue')
title_frame.grid(row=0, columnspan=2)
frame_L.grid(row=1, column=0, sticky='nsew')
frame_R.grid(row=1, column=1, sticky='nsew')
window.columnconfigure(0, minsize=WIDTH//2)
window.columnconfigure(1, minsize=WIDTH//2)
window.rowconfigure(0, minsize=ROW_HEIGHT)
window.rowconfigure(1, minsize=400)

frame_L.columnconfigure(0, minsize=WIDTH//2)
frame_L.rowconfigure([0, 1], minsize=200)

start_btn = tk.Button(master=frame_L, text='Start Search')
auto_btn = tk.Button(master=frame_L, text='Auto Search')
start_btn.grid(column=0, row=0, sticky='nsew', padx=40, pady=40)
auto_btn.grid(column=0, row=1, sticky='nsew', padx=40, pady=40)

window.mainloop()