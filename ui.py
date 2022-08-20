from cmath import log
from sys import maxsize
import tkinter as tk
from PIL import Image, ImageTk

# Global Variable Initialization
ROW_HEIGHT = 80
WIDTH = 852
HEIGHT = 480
BG_COLOUR = '#d6d6d6'

window = tk.Tk()
window.title('Student Housing Finder')

# Set up frames for UI
title_frame = tk.Frame(master=window, width=WIDTH, height=ROW_HEIGHT, bg=BG_COLOUR)
frame_L = tk.Frame(master=window, width=WIDTH//2, height=400, bg=BG_COLOUR)
frame_R = tk.Frame(master=window, width=WIDTH//2, height=400, bg=BG_COLOUR)

# Set up header for application
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_lbl = tk.Label(master=title_frame, image=logo)
logo_lbl.image = logo
logo_lbl.pack()

# Set grid locations of frames
title_frame.grid(row=0, columnspan=2, sticky='nsew')
frame_L.grid(row=1, column=0, sticky='nsew')
frame_R.grid(row=1, column=1, sticky='nsew')

# Set minimum size for window rows/coloumns
window.columnconfigure(0, minsize=WIDTH//2)
window.columnconfigure(1, minsize=WIDTH//2)
window.rowconfigure(0, minsize=ROW_HEIGHT)
window.rowconfigure(1, minsize=400)

# Set minimum sizes for left frame rows/columns
frame_L.columnconfigure(0, minsize=WIDTH//2)
frame_L.rowconfigure([0, 1, 3], minsize=100)
frame_L.rowconfigure(2, minsize=50)

# Create buttons & slider for left side of screen
start_btn = tk.Button(master=frame_L, text='Start Search')
auto_btn = tk.Button(master=frame_L, text='Auto Search')
time_sldr = tk.Scale(master=frame_L, from_=1, to=10, orient=tk.HORIZONTAL)
reset_btn = tk.Button(master=frame_L, text='Reset Filters')

# Position buttons & slider
start_btn.grid(column=0, row=0, sticky='nsew', padx=20, pady=20)
auto_btn.grid(column=0, row=1, sticky='nsew', padx=20, pady=20)
time_sldr.grid(column=0, row=2, sticky='nsew', padx=20, pady=20)
reset_btn.grid(column=0, row=3, sticky='nsew', padx=20, pady=20)

# Add status window to right of screen
status_lbl = tk.Label(master=frame_R, text='STATUS', bg=BG_COLOUR, fg='black')
status_text = tk.StringVar()
status_window = tk.Label(master=frame_R, textvariable=status_text, width=35, height=18, bg='white', fg='black')
status_text.set('Nothing\nNothing at all!')
status_lbl.pack(pady=20)
status_window.pack()

window.mainloop()