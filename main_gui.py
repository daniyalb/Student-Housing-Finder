import tkinter as tk
from typing import Any
import beepy
from PIL import Image, ImageTk
from finder import Finder
from os.path import exists

# Global Variable Initialization
ROW_HEIGHT = 80
WIDTH = 852
HEIGHT = 480
Q_XPAD = 10
RADIO_PAD = 30
BG_COLOUR = '#DBDBDB'
GREEN = '#53A548'
RED = '#E3170A'
TEXT_COLOUR = '#071013'
TEXT_COLOUR_LIGHT = 'white'
BTN_CLR = '#133C55'
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
            The Controller object that determines which screen is currently
            being shown
        main_frame:
            A Tkinter frame representing the main frame for the filter selection
            screen, this is accessed by the Controller object to display the
            filter screen
    """
    # === Private Attributes ===
    # _t_frame:
    #    The Tkinter frame representing the title section for the filter
    #    selection screen
    # _f_frame:
    #    Tkinter frame representing the filter question section of the screen
    # _pet_var:
    #    A Tkinter integer variable representing the option selected by the user
    #    for if they want a pet-friendly accommodation, a value of  0 meaning
    #    unselected, 1 meaning yes, 2 meaning no
    # _furn_var:
    #    A Tkinter integer variable representing the option selected by the user
    #    for if they want a furnished accommodation, a value of  0 meaning
    #    unselected, 1 meaning yes, 2 meaning no
    # _sldr_price:
    #    A Tkinter slider object which allows the user to input the maximum
    #    price they would like to rent for
    # _female_var:
    #    A Tkinter integer variable representing the option selected by the user
    #    for if they want female-only accommodations, a value of  0 meaning
    #    unselected, 1 meaning yes, 2 meaning no
    # _male_var:
    #    A Tkinter integer variable representing the option selected by the user
    #    for if they want male-only accommodations, a value of  0 meaning
    #    unselected, 1 meaning yes, 2 meaning no
    # _cityVar:
    #    A Tkinter string variable that represents the user's selection for
    #    which city they want to search in
    # _error_text:
    #    A Tkinter string variable that represents an error message that
    #    displays when the user has not made a selection for all questions
    # _values:
    #    A tuple containing all of the Tkinter variables representing the user's
    #    answer to each of the filter questions

    controller: Controller
    main_frame: tk.Frame
    _t_frame: tk.Frame
    _f_frame: tk.Frame
    _pet_var: tk.IntVar
    _furn_var: tk.IntVar
    _sldr_price: tk.Scale
    _female_var: tk.IntVar
    _male_var: tk.IntVar
    _cityVar: tk.StringVar
    _error_text: tk.StringVar
    _values: tuple

    def __init__(self, controller) -> None:
        """ Initialize all attributes and create the frames, labels, buttons,
        and radio buttons in order to have the user input the filters they
        want to search with
        """
        self.controller = controller
        self.main_frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT,
                                   bg=BG_COLOUR)
        self.main_frame.grid(column=0, row=0, columnspan=2, rowspan=2,
                             sticky='nsew')

        self._make_frames()

        filter_txt = tk.Label(master=self._t_frame,
                              text=('Select the filters you would like to use '
                                    'in your search below:'), font=FONT_B,
                              bg=BG_COLOUR, fg=TEXT_COLOUR)
        filter_txt.grid(column=0, row=0, columnspan=2, rowspan=3)

        self._make_questions()

        confirm_btn = tk.Button(master=self.f_frame, text='Confirm Filters',
                                fg=TEXT_COLOUR_LIGHT, font=FONT,
                                highlightbackground=GREEN, command=self.
                                _check_filters)
        confirm_btn.grid(column=2, columnspan=2, row=7, sticky='ew', padx=100,
                         pady=10)

        self._error_text = tk.StringVar()
        error_lbl = tk.Label(master=self.f_frame, textvariable=self._error_text,
                             fg=RED, font=FONT_S, bg=BG_COLOUR)
        error_lbl.grid(column=2, columnspan=2, row=8, sticky='nsew')

    def _make_frames(self):
        """ Initialize the frames for the filter select screen such as the
        title frame <self.t_frame> and filter frame <self.f_frame>
        """
        self._t_frame = tk.Frame(master=self.main_frame, width=WIDTH, height=50,
                                 bg=BG_COLOUR)
        self._t_frame.grid(column=0, row=0, columnspan=2, sticky='nsew')
        self._t_frame.columnconfigure(0, minsize=WIDTH // 2)
        self._t_frame.columnconfigure(1, minsize=WIDTH // 2)
        self._t_frame.rowconfigure(0, minsize=80 // 3)
        self._t_frame.rowconfigure(1, minsize=80 // 3)
        self._t_frame.rowconfigure(2, minsize=80 // 3)

        self.f_frame = tk.Frame(master=self.main_frame, width=WIDTH,
                                height=400, bg=BG_COLOUR)
        self.f_frame.grid(column=0, row=1, columnspan=2, sticky='nsew')
        for i in range(4):
            self.f_frame.columnconfigure(i, minsize=WIDTH // 4)
        self.f_frame.rowconfigure(2, minsize=40)
        self.f_frame.rowconfigure(5, minsize=40)

    def _make_questions(self):
        """ Create the labels, radio buttons, sliders, and dropdown menus for
        each of the questions asking the user to input their option for the
        filter
        """
        self._pet_var = tk.IntVar()
        lbl_pet = tk.Label(master=self.f_frame,
                           text='Would you want pet friendly accommodations?',
                           bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_S)
        radio_pet_y = tk.Radiobutton(master=self.f_frame, text='Yes',
                                     bg=BTN_CLR, variable=self._pet_var,
                                     value=1)
        radio_pet_n = tk.Radiobutton(master=self.f_frame, text='No', bg=BTN_CLR,
                                     variable=self._pet_var, value=2)

        lbl_pet.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD,
                     pady=10)
        radio_pet_y.grid(row=1, column=0, sticky='nsew', padx=RADIO_PAD, pady=5)
        radio_pet_n.grid(row=1, column=1, sticky='nsew', padx=RADIO_PAD, pady=5)

        self._furn_var = tk.IntVar()
        lbl_furn = tk.Label(master=self.f_frame,
                            text='Would you want furnished accommodations?',
                            bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_S)
        radio_furn_y = tk.Radiobutton(master=self.f_frame, text='Yes',
                                      bg=BTN_CLR, variable=self._furn_var,
                                      value=1)
        radio_furn_n = tk.Radiobutton(master=self.f_frame, text='No',
                                      bg=BTN_CLR, variable=self._furn_var,
                                      value=2)

        lbl_furn.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=Q_XPAD,
                      pady=10)
        radio_furn_y.grid(row=4, column=0, sticky='nsew', padx=RADIO_PAD,
                          pady=5)
        radio_furn_n.grid(row=4, column=1, sticky='nsew', padx=RADIO_PAD,
                          pady=5)

        lbl_price = tk.Label(master=self.f_frame,
                             text=('What is the maximum price you will rent '
                                   'for?'), bg=BG_COLOUR, fg=TEXT_COLOUR,
                             font=FONT_S)
        self._sldr_price = tk.Scale(master=self.f_frame, from_=0, to=5000,
                                    orient=tk.HORIZONTAL, bg=BG_COLOUR,
                                    fg=TEXT_COLOUR, label='Select price in CAD',
                                    tickinterval=1000)

        lbl_price.grid(row=6, column=0, columnspan=2, sticky='nsew',
                       padx=Q_XPAD, pady=10)
        self._sldr_price.grid(row=7, rowspan=2, column=0, columnspan=2,
                              sticky='nsew', padx=Q_XPAD, pady=5)

        self._female_var = tk.IntVar()
        lbl_female = tk.Label(master=self.f_frame,
                              text='Would female-only accommodations work for '
                                   'you?',
                              bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_S)
        radio_female_y = tk.Radiobutton(master=self.f_frame, text='Yes',
                                        bg=BTN_CLR, variable=self._female_var,
                                        value=1)
        radio_female_n = tk.Radiobutton(master=self.f_frame, text='No',
                                        bg=BTN_CLR, variable=self._female_var,
                                        value=2)

        lbl_female.grid(row=0, column=2, columnspan=2, sticky='nsew',
                        padx=Q_XPAD, pady=10)
        radio_female_y.grid(row=1, column=2, sticky='nsew', padx=RADIO_PAD,
                            pady=5)
        radio_female_n.grid(row=1, column=3, sticky='nsew', padx=RADIO_PAD,
                            pady=5)

        self._male_var = tk.IntVar()
        lbl_male = tk.Label(master=self.f_frame, text='Would male-only '
                                                      'accommodations work for '
                                                      'you?', bg=BG_COLOUR,
                            fg=TEXT_COLOUR, font=FONT_S)
        radio_male_y = tk.Radiobutton(master=self.f_frame, text='Yes',
                                      bg=BTN_CLR, variable=self._male_var,
                                      value=1)
        radio_male_n = tk.Radiobutton(master=self.f_frame, text='No',
                                      bg=BTN_CLR, variable=self._male_var,
                                      value=2)

        lbl_male.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=Q_XPAD,
                      pady=10)
        radio_male_y.grid(row=4, column=2, sticky='nsew', padx=RADIO_PAD,
                          pady=5)
        radio_male_n.grid(row=4, column=3, sticky='nsew', padx=RADIO_PAD,
                          pady=5)

        self._cityVar = tk.StringVar()
        self._cityVar.set('Select city to search in')
        city_drop = tk.OptionMenu(self.f_frame, self._cityVar, 'Toronto',
                                  'Mississauga / Peel Region',
                                  'Markham / York Region',
                                  'Oakville / Halton Region', 'Hamilton',
                                  'Guelph', 'Kitchener / Waterloo',
                                  'Oshawa / Durham Region', 'Kingston',
                                  'London')
        city_drop.configure(font=FONT_S, bg=BG_COLOUR, fg=TEXT_COLOUR)
        city_drop.grid(column=2, columnspan=2, row=6, sticky='nsew', pady=10,
                       padx=30)

    def _check_filters(self):
        """ Check through the values of all questions to confirm if the user
        has selected an option, if they have not, make an error message visible
        telling them to select an option for each question. If they have, call
        methods to write the filters to a file, reset the current question
        boxes, create a Finder object, and finally display the main application
        screen.
        """
        self._values = (self._pet_var, self._furn_var, self._sldr_price,
                        self._female_var, self._male_var)
        valid_filters = True
        for value in self._values:
            if value.get() == 0:
                valid_filters = False
                self._error_text.set('Please make sure all questions are'
                                     '\nanswered and max price is not $0')

        if self._cityVar.get() == 'Select city to search in':
            valid_filters = False
            self._error_text.set('Please make sure all questions are'
                                 '\nanswered and max price is not $0')
        else:
            self._values += (self._cityVar,)

        if valid_filters:
            self._write_filters()
            self._reset_filters()
            self.controller.create_finder()
            self.controller.show_frame(MainApp)

    def _write_filters(self):
        """ Writes the currently selected filters to a txt file and erases the
        links.txt file as the filters have been changed so all links found with
        old filters are no longer valid
        """
        with open('Program Files/filters.txt', 'w') as f:
            for value in self._values:
                f.write(f'{value.get()}\n')

        with open('Program Files/links.txt', 'w') as f:
            f.write('')

    def _reset_filters(self):
        """ Resets the error text and the value of each of the filter questions
        """
        self._error_text.set('')
        self._cityVar.set('Select city to search in')
        for i in range(len(self._values) - 1):
            self._values[i].set(0)


class MainApp:
    """ The MainApp class for this program

        This class is responsible for displaying the main page of the app with
        options to search, auto search, and reset filters. It also contains
        methods to begin a search, start auto searching, end auto search, and
        reset filters.

        === Public Attributes ===
        controller:
            The Controller object that determines which screen is currently
            being shown
        main_frame:
            A Tkinter frame representing the main frame for the main app screen,
            this is accessed by the Controller object to display the main app
            screen
    """
    # === Private Attributes ===
    # _title_frame:
    #    The tkinter frame containing positioned at the top of the screen
    #    containing the logo for this application
    # _frame_l:
    #    The tkinter frame containing the widgets on the left side of the
    #    screen
    # _frame_l_sub:
    #    A tkinter frame which is contained in the <_frame_l> frame and
    #    hold the time slider widget, begin auto search button, and stop
    #    auto search button
    # _frame_r:
    #    The tkinter frame for the right side of the screen, contains the
    #    status window
    # _status_text:
    #    A tkinter string variable representing the text currently displayed
    #    in the status window
    # _time_sldr:
    #    A tkinter scale that appears to allow the user to select how often
    #    they want auto search to be performed
    # _auto_loop:
    #    A tkinter after loop that performs the auto search
    # _confirm_btn:
    #    A tkinter button, theconfirm button that the user selects when
    #    they have chosen a frequency for auto search to be performed
    # _stop_btn:
    #    A tkinter button that appears when auto search starts, allows
    #    the user to stop the auto search and end <_auto_loop>

    controller: Controller
    main_frame: tk.Frame
    _title_frame: tk.Frame
    _frame_l: tk.Frame
    _frame_l_sub: tk.Frame
    _frame_r: tk.Frame
    _status_text: tk.StringVar
    _time_sldr: tk.Scale
    _auto_loop: Any
    _confirm_btn: tk.Button
    _stop_btn: tk.Button

    def __init__(self, controller) -> None:
        """ Initialize the attributes for this class and set up all frames,
        buttons, and labels for the main app screen
        """
        self.controller = controller

        self._title_frame, self._frame_l, self._frame_l_sub, self._frame_r = \
            self._make_frames()

        # Set up header for application
        logo = Image.open('logo.png')
        logo = ImageTk.PhotoImage(logo)
        logo_lbl = tk.Label(master=self._title_frame, image=logo, bg=BG_COLOUR)
        logo_lbl.image = logo
        logo_lbl.grid(column=0, row=0, sticky='nsew')

        self._make_buttons()

        # Set the auto loop initially to None
        self._auto_loop = None

        # Add status window to right of screen
        status_lbl = tk.Label(master=self._frame_r, text='STATUS', bg=BG_COLOUR,
                              fg=TEXT_COLOUR, font=FONT)
        self._status_text = tk.StringVar()
        status_window = tk.Label(master=self._frame_r, textvariable=self.
                                 _status_text, width=35, height=17, bg='white',
                                 fg=TEXT_COLOUR)
        self._status_text.set('Waiting for selection...')
        status_lbl.pack(pady=10)
        status_window.pack()

    def _make_frames(self) -> tuple:
        """ Set up the frames for the main app, configure their minimum
        sizes, and place them into their positions on the screen
        """
        # Set up main frame
        self.main_frame = tk.Frame(master=window, width=WIDTH, height=HEIGHT,
                                   bg=BG_COLOUR)
        self.main_frame.grid(column=0, row=0, columnspan=2, rowspan=2,
                             sticky='nsew')

        # Set up frames for UI
        title_frame = tk.Frame(master=self.main_frame, width=WIDTH,
                               height=ROW_HEIGHT, bg=BG_COLOUR)
        frame_l = tk.Frame(master=self.main_frame, width=WIDTH // 2, height=400,
                           bg=BG_COLOUR)
        frame_l_sub = tk.Frame(master=frame_l, width=WIDTH // 2, bg=BG_COLOUR)
        frame_r = tk.Frame(master=self.main_frame, width=WIDTH // 2, height=400,
                           bg=BG_COLOUR)

        # Set minimum sizes for left frame rows/columns
        frame_l.columnconfigure(0, minsize=WIDTH // 2)
        frame_l.rowconfigure(0, minsize=100)
        frame_l.rowconfigure(1, minsize=100)
        frame_l.rowconfigure(2, minsize=50)
        frame_l.rowconfigure(3, minsize=100)
        frame_l_sub.columnconfigure(0, minsize=WIDTH // 4)
        frame_l_sub.columnconfigure(1, minsize=WIDTH // 4)

        # Set grid locations of frames
        title_frame.grid(row=0, columnspan=2, sticky='nsew')
        frame_l.grid(row=1, column=0, sticky='nsew')
        frame_l_sub.grid(column=0, row=2, sticky='nsew')
        frame_r.grid(row=1, column=1, sticky='nsew')

        return title_frame, frame_l, frame_l_sub, frame_r

    def _make_buttons(self):
        """ Create the buttons, assign their commands, and place them into
        their location on the screen
        """
        # Create buttons & slider for left side of screen
        start_btn = tk.Button(master=self._frame_l, text='Start Search',
                              font=FONT, fg=TEXT_COLOUR_LIGHT,
                              highlightbackground=GREEN, command=self.search)
        auto_btn = tk.Button(master=self._frame_l, text='Auto Search', font=FONT,
                             fg=TEXT_COLOUR_LIGHT, highlightbackground=BTN_CLR,
                             command=self.get_minutes)
        self._time_sldr = tk.Scale(master=self._frame_l_sub, from_=1, to=10,
                                  orient=tk.HORIZONTAL, bg=BG_COLOUR,
                                  fg=TEXT_COLOUR,
                                  label='Select time in minutes:',
                                  tickinterval=1.0)
        self._confirm_btn = tk.Button(master=self._frame_l_sub,
                                     text='Begin Auto Search', font=FONT_S,
                                     fg=TEXT_COLOUR_LIGHT,
                                     highlightbackground=GREEN,
                                     command=self.start_auto_search)
        self._stop_btn = tk.Button(master=self._frame_l, text='Stop Auto Search',
                                  font=FONT_S, fg=TEXT_COLOUR_LIGHT,
                                  highlightbackground=RED,
                                  command=self.stop_auto_search)
        reset_btn = tk.Button(master=self._frame_l, text='Reset Filters',
                              font=FONT, fg=TEXT_COLOUR_LIGHT,
                              highlightbackground=BTN_CLR, command=self.
                              reset_filters)

        # Position buttons & slider
        start_btn.grid(column=0, row=0, sticky='nsew', padx=20, pady=20)
        auto_btn.grid(column=0, row=1, sticky='nsew', padx=20, pady=20)
        self._time_sldr.grid(column=0, row=0, sticky='nsew', padx=10, pady=5)
        self._time_sldr.grid_remove()
        self._confirm_btn.grid(column=1, row=0, sticky='nsew', padx=10, pady=20)
        self._confirm_btn.grid_remove()
        self._stop_btn.grid(column=0, row=2, sticky='nsew', padx=80, pady=20)
        self._stop_btn.grid_remove()
        reset_btn.grid(column=0, row=3, sticky='nsew', padx=20, pady=20)

    def search(self):
        """ This method is called when the "Start Search" button is pressed,
        it initiates the search method in the Finder object found in
        <self.controller>, then displays the results of the search in the
        status box
        """
        self._status_text.set('Searching for listings on kijiji.ca that match'
                             '\nyour filters...')
        window.update()

        num_results, name = self.controller.finder.search()
        if num_results == 0:
            self._status_text.set(f'Found {num_results} results matching your '
                                 f'filters.\nNo new file was created in the '
                                 f'Results folder.')
        else:
            self._status_text.set(f'Found {num_results} results matching your '
                                 f'filters!\nFind the listings in the Results '
                                 f'folder within a\nfile titled: {name}')
            beepy.beep(sound=5)

    def get_minutes(self):
        """ Removes the start button if its being displays and displays the
        slider and asks the user to input the frequency they would like auto
        search to be performed
        """
        self._stop_btn.grid_remove()
        self._time_sldr.grid()
        self._confirm_btn.grid()
        self._status_text.set('Please use the slider to select how often you'
                             '\nwould like the Auto Search to be performed'
                             '\n(in minutes), Then press \"Begin Auto Search\"')

    def start_auto_search(self):
        """ This method is called when the user presses the button to begin the
        auto search, it removes the slider and confirm button for starting an
        auto search and places the stop auto search button on the screen,
        finally calling the self._auto_search() method
        """
        self._time_sldr.grid_remove()
        self._confirm_btn.grid_remove()
        self._stop_btn.grid()
        self._auto_search()

    def _auto_search(self):
        """ This method performs an auto search every few minutes as specified
        by the user by calling the self.search() method, it also updates the
        user on when auto search is being performed
        """
        self.search()
        self._status_text.set(f'{self._status_text.get()}\n\nAuto Searching for '
                             f'listings matching your filters\nevery '
                             f'{self._time_sldr.get()} minute(s)')
        self._auto_loop = window.after(self._time_sldr.get() * 60000,
                                      self._auto_search)

    def stop_auto_search(self):
        """ Stops the Tkinter loop that causes auto search to be perfomed
        every few minutes, removes the stop button and informs the user that
        auto search has stopped
        """
        window.after_cancel(self._auto_loop)
        self._auto_loop = None
        self._stop_btn.grid_remove()
        self._status_text.set('Auto Search has been stopped!\n\nWaiting for '
                             'selection...')

    def reset_filters(self):
        """ Removes temporary elements from the main app such as the buttons
        and slider asking the user to input auto search frequency, resets
        the status box text, and then calls show_frame() in the self.controller
        object to show the filter select screen
        """
        self._time_sldr.grid_remove()
        self._confirm_btn.grid_remove()
        self._stop_btn.grid_remove()
        if self._auto_loop:
            self.stop_auto_search()
        self._status_text.set('Waiting for selection...')
        self.controller.show_frame(Filters)


if __name__ == '__main__':
    window = tk.Tk()  # Set up the main window for Tkinter
    window.title('Student Housing Finder')

    window.columnconfigure(0, minsize=WIDTH//2)
    window.columnconfigure(1, minsize=WIDTH//2)
    window.rowconfigure(0, minsize=ROW_HEIGHT)
    window.rowconfigure(1, minsize=400)

    app = Controller()

    window.mainloop()
