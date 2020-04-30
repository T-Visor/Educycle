import tkinter              

class StartPage(tkinter.Frame):

    current_option = None

    def __init__(self, parent, controller):
        """ 
            Constructs a new page.

            - parent : the parent class
            - controller : the application
        """
        tkinter.Frame.__init__(self, parent)

        self.controller = controller # for switching between pages
        self.current_option = tkinter.StringVar(self) # for getting a menu option

        self.populate_window(controller)

    def populate_window(self, controller):
        """ 
            Populates the page with elements and attributes.

            - controller : the application
        """
        self.create_header(controller, 'Select a menu item to view information')
        self.create_menu(controller)
        self.create_buttons(controller)

    ############################### PAGE PROPERTIES ############################### 

    def create_header(self, controller, header):
        """ 
            Creates a header for the current page.
            
            - controller : the application
            - header : contents of the header
        """
        label = tkinter.Label(self, text=header, font=controller.header_font)
        label.pack(side='top', fill='x', pady=10)


    def create_menu(self, controller):
        """ 
            Creates a drop-down menu for the current page. 

            - controller : the application
        """
        application_pages = ['BaltimoreSchoolsPage','TowsonParticipantsPage', 'ServiceRequestsPage',
                             'EquipmentPage', 'ComputersPage', 'PartsPage', 'AudioVisualPage'] # add pages for the application here

        # default to the first page in the list
        self.current_option.set(application_pages[0])

        menu_button = tkinter.OptionMenu(self, self.current_option, *application_pages)
        menu_button.pack()

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        # change to the page which was selected from the drop-down menu
        change_page_button = tkinter.Button(self, text='Go to selected page', font=controller.button_font,
                                command=lambda: controller.show_frame(self.current_option.get()))
        change_page_button.place(relx=0.5, rely=0.2, anchor='center')

        logout_button = tkinter.Button(self, text='Log out', font=controller.button_font,
                                       command=lambda: controller.show_frame('LoginPage'))
        logout_button.place(relx=0.5, rely=0.5, anchor='center')