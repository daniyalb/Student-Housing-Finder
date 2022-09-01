import tkinter as tk
from PIL import Image, ImageTk
from finder import Finder
from os.path import exists

# Global Variable Initialization
ROW_HEIGHT = 80
WIDTH = 852
HEIGHT = 480
Q_XPAD = 10
RADIO_PAD = 30
BG_COLOUR = '#d6d6d6'
GREEN = '#0e7d00'
RED = '#c41000'
FONT = ('courier', 20)
FONT_B = ('courier', 20, 'bold')
FONT_S = ('courier', 15)


def check_filters() -> bool:
    """ Checks if filters have already been specified in a file named
    filters.txt, returns true if they have, and false otherwise
    """
    return exists('Program Files/filters.txt')


def read_filters(filters: list) -> dict:
    """ Iterate through <filters> and assign the value of these filters in
    the filter_dict, the keys being the name of the filter, then return this
    dictionary
    """
    filter_dict = {}

    for i in range(len(filters)):
        filters[i] = filters[i].replace('\n', '')

    if filters[0] == '1':
        filter_dict['pets'] = True
    else:
        filter_dict['pets'] = False

    if filters[1] == '1':
        filter_dict['furnished'] = True
    else:
        filter_dict['furnished'] = False

    filter_dict['max price'] = int(filters[2])

    if filters[3] == '1':
        filter_dict['female-only'] = True
    else:
        filter_dict['female-only'] = False

    if filters[4] == '1':
        filter_dict['male-only'] = True
    else:
        filter_dict['male-only'] = False

    filter_dict['city'] = filters[5]

    return filter_dict


class Controller:
    """ The Controller Class

        This class is responsible for controlling which frames of the GUI are
        being displayed at the current time, checking for and reading the
        filters, and creating a Finder object

        === Public Attributes ===
        frames:
             A dictionary containing each class with keys representing the
             different main frames of the GUI, the values of these keys
             being an object that contains all the elements of this
             main frame
        finder:
            A Finder object which searches through kijiji listings and
            determines if they match the filters passed into it as attributes,
            writes these results to a txt file
    """
    frames: dict
    finder: Finder

    def __init__(self) -> None:
        """ Initialize the frames dictionary containing the objects of each
        of the main frames, check for filters and call a method to create a
        Finder object, and display the appropriate page based on the existence
        of filters
        """
        self.frames = {}

        for page in (Filters, MainApp):
            self.frames[page] = page(self)

        if check_filters():
            self.create_finder()
            self.show_frame(MainApp)
        else:
            self.show_frame(Filters)

    def show_frame(self, f_type) -> None:
        """ Show the main frame corresponding to <f_type>
        """
        frame = self.frames[f_type].main_frame
        frame.tkraise()

    def create_finder(self) -> None:
        """ Create a Finder object by reading the filters in filters.txt,
        calling a function to create a dictionary of these filters, then
        passing these filters as attributes to create a Finder object
        """
        with open('Program Files/filters.txt', 'r') as f:
            filters = f.readlines()

        filter_dict = read_filters(filters)

        city = filter_dict['city']
        max_price = filter_dict['max price']
        pets = filter_dict['pets']
        furnished = filter_dict['furnished']
        female_only = filter_dict['female-only']
        male_only = filter_dict['male-only']

        self.finder = Finder(city, max_price, pets, furnished, female_only,
                             male_only)


class Filters:
    """ The Filters class for this program.

        This class displays the options for the user to select their search
        filters, confirms if these filters are valid, writes these filters to
        a txt file, and can reset the filters by erasing the contents of the
        file.

        === Public Attributes ===
        controller:
            a
        main_frame:
            a
        pet_var:
            a
        furn_var:
            a
        sldr_price:
            a
        female_var:
            a
        male_var:
            a
        cityVar:
            a
        error_text:
            a
    """

    def __init__(self, controller) -> None:
        self.controller = controller
        self.main_frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT,
                                   bg=BG_COLOUR)
        self.main_frame.grid(column=0, row=0, columnspan=2, rowspan=2,
                             sticky='nsew')

        t_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=50,
                           bg=BG_COLOUR)
        t_frame.grid(column=0, row=0, columnspan=2, sticky='nsew')
        t_frame.columnconfigure(0, minsize=WIDTH//2)
        t_frame.columnconfigure(1, minsize=WIDTH//2)
        t_frame.rowconfigure(0, minsize=80//3)
        t_frame.rowconfigure(1, minsize=80//3)
        t_frame.rowconfigure(2, minsize=80//3)
        filter_txt = tk.Label(master=t_frame, text=('Select the filters you ' 
                                                    'would like to use in your '
                                                    'search below:'),
                              font=FONT_B, bg=BG_COLOUR, fg='black')
        filter_txt.grid(column=0, row=0, columnspan=2, rowspan=3)

        r_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=400,
                           bg=BG_COLOUR)
        r_frame.grid(column=0, row=1, columnspan=2, sticky='nsew')
        for i in range(4):
            r_frame.columnconfigure(i, minsize=WIDTH//4)
        r_frame.rowconfigure(2, minsize=40)
        r_frame.rowconfigure(5, minsize=40)

        self.pet_var = tk.IntVar()
        lbl_pet = tk.Label(master=r_frame,
                           text='Would you want pet friendly accommodations?',
                           bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_pet_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey',
                                     variable=self.pet_var, value=1)
        radio_pet_n = tk.Radiobutton(master=r_frame, text='No', bg='grey',
                                     variable=self.pet_var, value=2)

        lbl_pet.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD,
                     pady=10)
        radio_pet_y.grid(row=1, column=0, sticky='nsew', padx=RADIO_PAD, pady=5)
        radio_pet_n.grid(row=1, column=1, sticky='nsew', padx=RADIO_PAD, pady=5)

        self.furn_var = tk.IntVar()
        lbl_furn = tk.Label(master=r_frame,
                            text='Would you want furnished accommodations?',
                            bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_furn_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey',
                                      variable=self.furn_var, value=1)
        radio_furn_n = tk.Radiobutton(master=r_frame, text='No', bg='grey',
                                      variable=self.furn_var, value=2)

        lbl_furn.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD,
                      pady=10)
        radio_furn_y.grid(row=4, column=0, sticky='nsew', padx=RADIO_PAD,
                          pady=5)
        radio_furn_n.grid(row=4, column=1, sticky='nsew', padx=RADIO_PAD,
                          pady=5)

        lbl_price = tk.Label(master=r_frame,
                             text=('What is the maximum price you will rent '
                                   'for?'), bg=BG_COLOUR, fg='black',
                             font=FONT_S)
        self.sldr_price = tk.Scale(master=r_frame, from_=0, to=5000,
                                   orient=tk.HORIZONTAL, bg=BG_COLOUR,
                                   fg='black', label='Select price in CAD',
                                   tickinterval=1000)

        lbl_price.grid(row=6, column=0, columnspan=2, sticky='nsew',
                       padx=Q_XPAD, pady=10)
        self.sldr_price.grid(row=7, rowspan=2, column=0, columnspan=2,
                             sticky='nsew', padx=Q_XPAD, pady=5)

        self.female_var = tk.IntVar()
        lbl_female = tk.Label(master=r_frame, text='Would female-only accomodat'
                                                   'ions work for you?',
                              bg=BG_COLOUR, fg='black', font=FONT_S)
        radio_female_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey',
                                        variable=self.female_var, value=1)
        radio_female_n = tk.Radiobutton(master=r_frame, text='No', bg='grey',
                                        variable=self.female_var, value=2)

        lbl_female.grid(row=0, column=2, columnspan=2, sticky='nsew',
                        padx=Q_XPAD, pady=10)
        radio_female_y.grid(row=1, column=2, sticky='nsew', padx=RADIO_PAD,
                            pady=5)
        radio_female_n.grid(row=1, column=3, sticky='nsew', padx=RADIO_PAD,
                            pady=5)

        self.male_var = tk.IntVar()
        lbl_male = tk.Label(master=r_frame, text='Would male-only accomodations'
                                                 ' work for you?', bg=BG_COLOUR,
                            fg='black', font=FONT_S)
        radio_male_y = tk.Radiobutton(master=r_frame, text='Yes', bg='grey',
                                      variable=self.male_var, value=1)
        radio_male_n = tk.Radiobutton(master=r_frame, text='No', bg='grey',
                                      variable=self.male_var, value=2)

        lbl_male.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=Q_XPAD,
                      pady=10)
        radio_male_y.grid(row=4, column=2, sticky='nsew', padx=RADIO_PAD,
                          pady=5)
        radio_male_n.grid(row=4, column=3, sticky='nsew', padx=RADIO_PAD,
                          pady=5)

        self.cityVar = tk.StringVar()
        self.cityVar.set('Select city to search in')
        cityDrop = tk.OptionMenu(r_frame, self.cityVar, 'Toronto',
                                 'Mississauga / Peel Region',
                                 'Markham / York Region',
                                 'Oakville / Halton Region', 'Hamilton',
                                 'Guelph', 'Kitchener / Waterloo',
                                 'Oshawa / Durham Region', 'Kingston', 'London')
        cityDrop.configure(font=FONT_S, bg=BG_COLOUR, fg='black')
        cityDrop.grid(column=2, columnspan=2, row=6, sticky='nsew', pady=10,
                      padx=30)

        confirm_btn = tk.Button(master=r_frame, text='Confirm Filters',
                                fg='white', font=FONT,
                                highlightbackground=GREEN, command=self.
                                _check_filters)
        confirm_btn.grid(column=2, columnspan=2, row=7, sticky='ew', padx=100,
                         pady=10)

        self.error_text = tk.StringVar()
        error_lbl = tk.Label(master=r_frame, textvariable=self.error_text,
                             fg='red', font=FONT_S, bg=BG_COLOUR)
        error_lbl.grid(column=2, columnspan=2, row=8, sticky='nsew')

    def _check_filters(self):
        values = (self.pet_var, self.furn_var, self.sldr_price, self.female_var,
                  self.male_var)
        valid_filters = True
        for value in values:
            if value.get() == 0:
                valid_filters = False
                self.error_text.set('Please make sure all questions are'
                                    '\nanswered and max price is not $0')

        if self.cityVar.get() == 'Select city to search in':
            valid_filters = False
            self.error_text.set('Please make sure all questions are'
                                '\nanswered and max price is not $0')
        else:
            values += (self.cityVar,)

        if valid_filters:
            self._write_filters(values)
            self._reset_filters(values)
            self.controller.finder = self.controller.create_finder()
            self.controller.show_frame(MainApp)

    def _write_filters(self, values):
        with open('Program Files/filters.txt', 'w') as f:
            for value in values:
                f.write(f'{value.get()}\n')

        with open('Program Files/links.txt', 'w') as f:
            f.write('') # Erase all links found with old filters

    def _reset_filters(self, values):
        self.error_text.set('')
        self.cityVar.set('Select city to search in')
        for i in range(len(values) - 1):
            values[i].set(0)


class MainApp():
    def __init__(self, controller) -> None:
        self.controller = controller
        self.main_frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT, bg=BG_COLOUR)
        self.main_frame.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew')

        # Set up frames for UI
        title_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=ROW_HEIGHT, bg=BG_COLOUR)
        frame_L = tk.Frame(master=self.main_frame, width=WIDTH//2, height=400, bg=BG_COLOUR)
        frame_L_sub = tk.Frame(master=frame_L, width=WIDTH//2, bg=BG_COLOUR)
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
        frame_L_sub.grid(column=0, row=2, sticky='nsew')
        frame_R.grid(row=1, column=1, sticky='nsew')

        # Set minimum sizes for left frame rows/columns
        frame_L.columnconfigure(0, minsize=WIDTH//2)
        frame_L.rowconfigure([0, 1, 3], minsize=100)
        frame_L.rowconfigure(2, minsize=50)
        frame_L_sub.columnconfigure([0, 1], minsize=WIDTH//4)

        self.frames = (title_frame, frame_L, frame_R)

        # Create buttons & slider for left side of screen
        start_btn = tk.Button(master=frame_L, text='Start Search', font=FONT, highlightbackground=GREEN, command=self.search)
        auto_btn = tk.Button(master=frame_L, text='Auto Search', font=FONT, command=self.get_minutes)
        self.time_sldr = tk.Scale(master=frame_L_sub, from_=1, to=10, orient=tk.HORIZONTAL, bg=BG_COLOUR, fg='black', label='Select time in minutes:', tickinterval=1.0)
        self.confirm_btn = tk.Button(master=frame_L_sub, text='Begin Auto Search', font=FONT_S, highlightbackground=GREEN, command=self.start_auto_search)
        self.stop_btn = tk.Button(master=frame_L, text='Stop Auto Search', font=FONT_S, highlightbackground=RED, command=self.stop_auto_search)
        reset_btn = tk.Button(master=frame_L, text='Reset Filters', font=FONT, command=self.reset_filters)

        # Position buttons & slider
        start_btn.grid(column=0, row=0, sticky='nsew', padx=20, pady=20)
        auto_btn.grid(column=0, row=1, sticky='nsew', padx=20, pady=20)
        self.time_sldr.grid(column=0, row=0, sticky='nsew', padx=10, pady=5)
        self.time_sldr.grid_remove()
        self.confirm_btn.grid(column=1, row=0, sticky='nsew', padx=10, pady=20)
        self.confirm_btn.grid_remove()
        self.stop_btn.grid(column=0, row=2, sticky='nsew', padx=80, pady=20)
        self.stop_btn.grid_remove()
        reset_btn.grid(column=0, row=3, sticky='nsew', padx=20, pady=20)

        # Add status window to right of screen
        status_lbl = tk.Label(master=frame_R, text='STATUS', bg=BG_COLOUR, fg='black', font=FONT)
        self.status_text = tk.StringVar()
        status_window = tk.Label(master=frame_R, textvariable=self.status_text, width=35, height=17, bg='white', fg='black')
        self.status_text.set('Waiting for selection...')
        status_lbl.pack(pady=10)
        status_window.pack()

    def search(self):
        self.status_text.set('Searching for listings on kijiji.ca that match\nyour filters...')
        window.update()

        num_results, name = self.controller.finder.search()
        if num_results == 0:
            self.status_text.set(f'Found {num_results} results matching your filters.\nNo new file was created in the Results folder.')
        else:
            self.status_text.set(f'Found {num_results} results matching your filters!\nFind the listings in the Results folder within a\nfile titled: {name}')

    def get_minutes(self):
        self.stop_btn.grid_remove()
        self.time_sldr.grid()
        self.confirm_btn.grid()
        self.status_text.set('Please use the slider to select how often you\nwould like the Auto Search to be performed\n(in minutes), Then press Auto Search again to\nbegin the process')

    def start_auto_search(self):
        self.time = self.time_sldr.get()
        self.time_sldr.grid_remove()
        self.confirm_btn.grid_remove()
        self.stop_btn.grid()
        self._auto_search()

    def _auto_search(self):
        self.search()
        self.status_text.set(f'{self.status_text.get()}\n\nAuto Searching for listings matching your filters\nevery {self.time} minute(s)')
        self.auto_loop = window.after(self.time*60000, self._auto_search)

    def stop_auto_search(self):
        window.after_cancel(self.auto_loop)
        self.stop_btn.grid_remove()
        self.status_text.set('Auto Search has been stopped!\n\nWaiting for selection...')

    def reset_filters(self):
        self.time_sldr.grid_remove()
        self.confirm_btn.grid_remove()
        self.stop_btn.grid_remove()
        self.status_text.set('Waiting for selection...')
        self.controller.show_frame(Filters)


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Student Housing Finder')

    window.columnconfigure([0, 1], minsize=WIDTH//2)
    window.rowconfigure(0, minsize=ROW_HEIGHT)
    window.rowconfigure(1, minsize=400)

    app = Controller()

    window.mainloop()
