import tkinter as tk
from PIL import Image, ImageTk
from test import Finder

# Global Variable Initialization
ROW_HEIGHT = 80
WIDTH = 852
HEIGHT = 480
BG_COLOUR = '#d6d6d6'
FONT = ('courier', 20)

city = 'mississauga / peel region'
max_price = 1500
pets = False
furnished = False
female_only = False
male_only = False
FINDER = Finder(city, max_price, pets, furnished, female_only, male_only)

def get_filters():
    frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT, bg=BG_COLOUR)
    window.columnconfigure(0, minsize=WIDTH)
    window.rowconfigure(0, minsize=HEIGHT)
    frame.grid(column=0, row=0)
    _max_price(frame)

def _max_price(frame):
    lbl = tk.Label(master=frame, text='What is the max price you will rent for?', bg=BG_COLOUR, fg='black', font=FONT)
    sldr = tk.Scale(master=frame, from_=0, to=5000, orient=tk.HORIZONTAL, bg=BG_COLOUR, fg='black')
    next_btn = tk.Button(master=frame, text='Next', font=FONT, command=lambda:_pets(frame))

    lbl.pack()
    sldr.pack()
    next_btn.pack()
    window.mainloop()

def _pets(frame):
    lbl = tk.Label(master=frame, text='Would you want pet friendly accomodations?', bg=BG_COLOUR, fg='black', font=FONT)
    sldr = tk.Scale(master=frame, from_=0, to=5000, orient=tk.HORIZONTAL, bg=BG_COLOUR, fg='black')
    next_btn = tk.Button(master=frame, text='Next', font=FONT)

    lbl.pack()
    sldr.pack()
    next_btn.pack()
    window.mainloop()

def main():
    # Set up frames for UI
    title_frame = tk.Frame(master=window, width=WIDTH, height=ROW_HEIGHT, bg=BG_COLOUR)
    frame_L = tk.Frame(master=window, width=WIDTH//2, height=400, bg=BG_COLOUR)
    frame_R = tk.Frame(master=window, width=WIDTH//2, height=400, bg=BG_COLOUR)

    # Set up header for application
    logo = Image.open('logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_lbl = tk.Label(master=title_frame, image=logo, bg=BG_COLOUR)
    logo_lbl.image = logo
    logo_lbl.grid(column=0, row=0, sticky='nsew')

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

    def search():
        num_results, name = FINDER.search()
        status_text.set(f'Found {num_results} results matching your filters!\nFind the listings in {name}')

    def get_minutes():
        time_sldr = tk.Scale(master=frame_L, from_=1, to=10, orient=tk.HORIZONTAL, bg=BG_COLOUR, fg='black')
        time_sldr.grid(column=0, row=2, sticky='nsew', padx=20, pady=5)
        status_text.set('Please use the slider to select how often you\nwould like the Auto Search to be performed\n(in minutes), Then press Auto Search again to\nbegin the process')

    # Create buttons & slider for left side of screen
    start_btn = tk.Button(master=frame_L, text='Start Search', font=FONT, command=search)
    auto_btn = tk.Button(master=frame_L, text='Auto Search', font=FONT, command=get_minutes)
    reset_btn = tk.Button(master=frame_L, text='Reset Filters', font=FONT)

    # Position buttons & slider
    start_btn.grid(column=0, row=0, sticky='nsew', padx=20, pady=20)
    auto_btn.grid(column=0, row=1, sticky='nsew', padx=20, pady=20)
    reset_btn.grid(column=0, row=3, sticky='nsew', padx=20, pady=20)

    # Add status window to right of screen
    status_lbl = tk.Label(master=frame_R, text='STATUS', bg=BG_COLOUR, fg='black', font=FONT)
    status_text = tk.StringVar()
    status_window = tk.Label(master=frame_R, textvariable=status_text, width=35, height=17, bg='white', fg='black')
    status_text.set('Waiting for selection...')
    status_lbl.pack(pady=10)
    status_window.pack()


window = tk.Tk()
window.title('Student Housing Finder')
get_filters()
main()