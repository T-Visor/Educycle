# add pages here via importing
from startPage import *
from baltimoreSchoolsPage import *
from serviceRequestsPage import *
from loginPage import *
from towsonParticipantsPage import * 
from createRequestPage import *
from equipmentPage import *
from enterEquipmentPage import *
from enterAVPage import *
from enterComputerPage import *
from enterPartPage import *
from removeEquipmentPage import *
from removeRequestPage import *
from computersPage import *
from audioVisualPage import *
from partsPage import *
from tkinter import font as tkfont 

class Application(tkinter.Tk):

    def __init__(self):
        """ 
            Constructs a new application (collection of pages). 
        """    
        tkinter.Tk.__init__(self)
        self.title('EduCycle Database Application')
        self.button_font = tkfont.Font(family='Helvetica', size=14)
        self.header_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # The container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for windows in (StartPage, BaltimoreSchoolsPage, TowsonParticipantsPage, 
                        ServiceRequestsPage, LoginPage, CreateRequestPage, 
                        EquipmentPage, EnterEquipmentPage, EnterAVPage,
                        EnterComputerPage, EnterPartPage, RemoveEquipmentPage,
                        RemoveRequestPage, ComputersPage, AudioVisualPage, PartsPage): # add pages for the application here
            page_name = windows.__name__
            window = windows(parent=container, controller=self)
            self.pages[page_name] = window

            # Place all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            window.grid(row=0, column=0, sticky='nsew')

        # first page to be shown for the application
        self.show_frame('LoginPage')

    def show_frame(self, page_name):
        """ 
        Show the page associated with the given name 
        
        - page_name : name of the class window (string) 
        """
        frame = self.pages[page_name]
        frame.tkraise()