import tkinter                
import sqlite3
from tkinter import ttk

class PartsPage(tkinter.Frame):

    results_table = None

    def __init__(self, parent, controller):
        """ 
            Constructs a new page.

            - parent : the parent class
            - controller : the application
        """
        tkinter.Frame.__init__(self, parent)

        self.controller = controller # for switching between pages
        self.results_table = ttk.Treeview(self, column=('1', '2', '3', '4')) # table to store results from query
        self.results_table['show'] = 'headings' # eliminates the blank colum for the table view

        self.populate_window(controller)

    def populate_window(self, controller):
        """ 
            Populates the page with elements and attributes.

            - controller : the application
        """
        # Query: Get all computer parts
        query = 'SELECT * FROM Computer_parts'

        self.create_header(controller, 'All computer parts (peripherals)')
        self.run_query(query)
        self.create_buttons(controller)

    ############################### PAGE PROPERTIES ############################### 

    def create_header(self, controller, header):
        """ 
            Creates a header for the current page.
            
            - controller : the application
            - header : contents of the header
        """
        label = tkinter.Label(self, text=header, font=controller.header_font)
        label.pack(side='top', fill='x', pady=20)

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        refresh_button = tkinter.Button(self, text='Refresh', font=controller.button_font,
                                        command=self.refresh)
        refresh_button.pack(pady=10)

        return_button = tkinter.Button(self, text='Go to the start page', font=controller.button_font,
                           command=lambda: controller.show_frame('StartPage'))
        return_button.pack(pady=20)

    ################################ EVENT HANDLERS ###################################

    def run_query(self, query):
        """
            Runs a query which will interact with the database.

            - query : the sqlite query statement
        """
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()

        cursor.execute(query)
        column_names = list(map(lambda name: name[0], cursor.description))
        results = cursor.fetchall()

        # ensures there are no duplicate entries
        self.results_table.delete(*self.results_table.get_children())

        # fill the top row with the column names
        for index, name in enumerate(column_names, 1):
            self.results_table.heading(index, text=name)

        # fill the rest of the table values from the query
        for entry in results:
            self.results_table.insert('', tkinter.END, values=entry)

        self.results_table.pack(fill='both', expand=False)
        connection.close()

    def refresh(self):
        """
            A wrapper method which will just re-run a query
        """
        query = 'SELECT * FROM Computer_parts'
        self.run_query(query)
