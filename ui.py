from calendar import c
import fractions
from re import T
import tkinter as tk
from typing_extensions import IntVar
from PIL import Image, ImageTk
from test import Finder
from os.path import exists

# Global Variable Initialization
ROW_HEIGHT = 80
WIDTH = 852
HEIGHT = 480
Q_XPAD = 10
RADIO_PAD = 30
BG_COLOUR = '#d6d6d6'
FONT = ('courier', 20)
FONT_B = ('courier', 20, 'bold')
FONT_S = ('courier', 15)

class Controller():
    """ The Controller Class
    
        This class is responsible for controlling which frames of the GUI are
        being displayed at the current time.

        === Public Attributes ===
        frames:
             A dictionary containing each class with keys representing the 
             different main frames of the GUI, the values of these keys
             being an object that contains all of the elements of this
             main frame
    """
    frames: dict
    finder: Finder

    def __init__(self) -> None:
        """ Initialize the frames dictionary containing the objects of each
        of the main frames, then call self.show_frame() to display the first
        page
        """
        self.frames = {}
        self.finder = None

        for page in (Filters, MainApp):
            self.frames[page] = page(self)

        if self.check_filters():
            self.finder = self.create_finder()
            self.show_frame(MainApp)
        else:
            self.show_frame(Filters)

    def check_filters(self) -> bool:
        """ Checks if filters have already been specified in a file named
        filters.txt, returns true if they have, and false otherwise
        """
        return exists('Program Files/filters.txt')

    def show_frame(self, type):
        """ Show the main frame corresponding to <type>"""
        frame = self.frames[type].main_frame
        frame.tkraise()

    def create_finder(self) -> Finder:
        with open('Program Files/filters.txt', 'r') as f:
            filters = f.readlines()
        
        filter_dict = self._read_filters(filters)

        city = 'mississauga / peel region'
        max_price = filter_dict['max price']
        pets = filter_dict['pets']
        furnished = filter_dict['furnished']
        female_only = filter_dict['female-only']
        male_only = filter_dict['male-only']

        return Finder(city, max_price, pets, furnished, female_only, male_only)
    
    def _read_filters(self, filters) -> dict:
        filter_dict = {}

        for i in range(len(filters)):
            filters[i] = filters[i].replace('\n', '')

            if i == 0:
                if filters[i] == '1':
                    filter_dict['pets'] = True
                else:
                    filter_dict['pets'] = False
            elif i == 1:
                if filters[i] == '1':
                    filter_dict['furnished'] = True
                else:
                    filter_dict['furnished'] = False
            elif i == 2:
                filter_dict['max price'] = int(filters[i])
            elif i == 3:
                if filters[i] == '1':
                    filter_dict['female-only'] = True
                else:
                    filter_dict['female-only'] = False
            elif i == 4:
                if filters[i] == '1':
                    filter_dict['male-only'] = True
                else:
                    filter_dict['male-only'] = False

        return filter_dict


class Filters():
    def __init__(self, controller) -> None:
        self.controller = controller
        self.main_frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT, bg=BG_COLOUR)
        self.main_frame.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew')

        t_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=50, bg=BG_COLOUR)
        t_frame.grid(column=0, row=0, columnspan=2, sticky='nsew')
        t_frame.columnconfigure([0, 1], minsize=WIDTH//2)
        t_frame.rowconfigure([0, 1, 2], minsize=80//3)
        filter_txt = tk.Label(master=t_frame, text='Select the filters you would like to use in your search below:', font=FONT_B, bg=BG_COLOUR, fg='black')
        filter_txt.grid(column=0, row=0, columnspan=2, rowspan=3)

        r_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=400, bg=BG_COLOUR)
        r_frame.grid(column=0, row=1, columnspan=2, sticky='nsew')
        r_frame.columnconfigure([0, 1, 2, 3], minsize=WIDTH//4)
        r_frame.rowconfigure([2, 5], minsize=40)

        self.pet_var = tk.IntVar()
        lbl_pet = tk.Label(master=r_frame, text='Would you want pet friendly accomodations?', bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_pet_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey', variable=self.pet_var, value=1)
        radio_pet_n = tk.Radiobutton(master=r_frame, text='No', bg='grey', variable=self.pet_var, value=2)
        
        lbl_pet.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD, pady=10)
        radio_pet_y.grid(row=1, column=0, sticky='nsew', padx=RADIO_PAD, pady=5)
        radio_pet_n.grid(row=1, column=1, sticky='nsew', padx=RADIO_PAD, pady=5)
        
        self.furn_var = tk.IntVar()
        lbl_furn = tk.Label(master=r_frame, text='Would you want furnished accomodations?', bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_furn_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey', variable=self.furn_var, value=1)
        radio_furn_n = tk.Radiobutton(master=r_frame, text='No', bg='grey', variable=self.furn_var, value=2)
        
        lbl_furn.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD, pady=10)
        radio_furn_y.grid(row=4, column=0, sticky='nsew', padx=RADIO_PAD, pady=5)
        radio_furn_n.grid(row=4, column=1, sticky='nsew', padx=RADIO_PAD, pady=5)

        lbl_price = tk.Label(master=r_frame, text='What is the maximum price you will rent for?', bg=BG_COLOUR, fg='black', font=FONT_S)
        self.sldr_price = tk.Scale(master=r_frame, from_=0, to=5000, orient=tk.HORIZONTAL, bg=BG_COLOUR, fg='black', label='Select price in CAD', tickinterval=1000)

        lbl_price.grid(row=6, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD, pady=10)
        self.sldr_price.grid(row=7, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD, pady=5)

        self.female_var = tk.IntVar()
        lbl_female = tk.Label(master=r_frame, text='Would female-only accomodations work for you?', bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_female_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey', variable=self.female_var, value=1)
        radio_female_n = tk.Radiobutton(master=r_frame, text='No', bg='grey', variable=self.female_var, value=2)
        
        lbl_female.grid(row=0, column=2, columnspan=2, sticky='nsew', padx=Q_XPAD, pady=10)
        radio_female_y.grid(row=1, column=2, sticky='nsew', padx=RADIO_PAD, pady=5)
        radio_female_n.grid(row=1, column=3, sticky='nsew', padx=RADIO_PAD, pady=5)

        self.male_var = tk.IntVar()
        lbl_male = tk.Label(master=r_frame, text='Would male-only accomodations work for you?', bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_male_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey', variable=self.male_var, value=1)
        radio_male_n = tk.Radiobutton(master=r_frame, text='No', bg='grey', variable=self.male_var, value=2)
        
        lbl_male.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=Q_XPAD, pady=10)
        radio_male_y.grid(row=4, column=2, sticky='nsew', padx=RADIO_PAD, pady=5)
        radio_male_n.grid(row=4, column=3, sticky='nsew', padx=RADIO_PAD, pady=5)

        confirm_btn = tk.Button(master=r_frame, text='Confirm Filters', fg='white', font=FONT, highlightbackground='#0e7d00',
        command = self._check_filters)
        confirm_btn.grid(column=2, columnspan=2, row=6, sticky='ew', padx=100)

        self.error_text = tk.StringVar()
        error_lbl = tk.Label(master=r_frame, textvariable=self.error_text, fg='red', font=FONT_S, bg=BG_COLOUR)
        error_lbl.grid(column=2, columnspan=2, row=7, sticky='nsew')


    def _check_filters(self):
        values = (self.pet_var, self.furn_var, self.sldr_price, self.female_var, self.male_var)
        valid_filters = True
        for value in values:
            if value.get() == 0:
                valid_filters = False
                self.error_text.set('Please make sure all questions are\nanswered and max price is not $0')

        if valid_filters:
            self._write_filters(values)
            self._reset_filters(values)
            self.controller.finder = self.controller.create_finder()
            self.controller.show_frame(MainApp)

    def _write_filters(self, values):
        with open('Program Files/filters.txt', 'w') as f:
            for value in values:
                f.write(f'{value.get()}\n')

    def _reset_filters(self, values):
        self.error_text.set('')
        for value in values:
            value.set(0)

class MainApp():
    def __init__(self, controller) -> None:
        self.controller = controller
        self.main_frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT, bg=BG_COLOUR)
        self.main_frame.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew')

        # Set up frames for UI
        title_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=ROW_HEIGHT, bg=BG_COLOUR)
        frame_L = tk.Frame(master=self.main_frame, width=WIDTH//2, height=400, bg=BG_COLOUR)
        frame_R = tk.Frame(master=self.main_frame, width=WIDTH//2, height=400, bg=BG_COLOUR)

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

        # Set minimum sizes for left frame rows/columns
        frame_L.columnconfigure(0, minsize=WIDTH//2)
        frame_L.rowconfigure([0, 1, 3], minsize=100)
        frame_L.rowconfigure(2, minsize=50)

        self.frames = (title_frame, frame_L, frame_R)

        def get_minutes():
            time_sldr = tk.Scale(master=frame_L, from_=1, to=10, orient=tk.HORIZONTAL, bg=BG_COLOUR, fg='black')
            time_sldr.grid(column=0, row=2, sticky='nsew', padx=20, pady=5)
            self.status_text.set('Please use the slider to select how often you\nwould like the Auto Search to be performed\n(in minutes), Then press Auto Search again to\nbegin the process')

        # Create buttons & slider for left side of screen
        start_btn = tk.Button(master=frame_L, text='Start Search', font=FONT, command=self.search)
        auto_btn = tk.Button(master=frame_L, text='Auto Search', font=FONT, command=get_minutes)
        reset_btn = tk.Button(master=frame_L, text='Reset Filters', font=FONT, command = lambda : controller.show_frame(Filters))

        # Position buttons & slider
        start_btn.grid(column=0, row=0, sticky='nsew', padx=20, pady=20)
        auto_btn.grid(column=0, row=1, sticky='nsew', padx=20, pady=20)
        reset_btn.grid(column=0, row=3, sticky='nsew', padx=20, pady=20)

        # Add status window to right of screen
        status_lbl = tk.Label(master=frame_R, text='STATUS', bg=BG_COLOUR, fg='black', font=FONT)
        self.status_text = tk.StringVar()
        status_window = tk.Label(master=frame_R, textvariable=self.status_text, width=35, height=17, bg='white', fg='black')
        self.status_text.set('Waiting for selection...')
        status_lbl.pack(pady=10)
        status_window.pack()

    def search(self):
        num_results, name = self.controller.finder.search()
        if num_results == 0:
            self.status_text.set(f'Found {num_results} results matching your filters.\nNo new file was created in the Results folder.')
        else:
            self.status_text.set(f'Found {num_results} results matching your filters!\nFind the listings in the Results folder within a\nfile titled: {name}')

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Student Housing Finder')

    window.columnconfigure([0, 1], minsize=WIDTH//2)
    window.rowconfigure(0, minsize=ROW_HEIGHT)
    window.rowconfigure(1, minsize=400)

    app = Controller()

    window.mainloop()