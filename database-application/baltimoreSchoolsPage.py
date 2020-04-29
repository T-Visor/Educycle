import tkinter                
import sqlite3
from tkinter import ttk

class BaltimoreSchoolsPage(tkinter.Frame):

    results_table = None

    def __init__(self, parent, controller):
        """ 
            Constructs a new page.

            - parent : the parent class
            - controller : the application
        """
        tkinter.Frame.__init__(self, parent)

        self.controller = controller # for switching between pages
        self.results_table = ttk.Treeview(self, column=('1', '2', '3')) # table to store results from query
        self.results_table['show'] = 'headings' # eliminates the blank colum for the table view

        self.populate_window(controller)

    def populate_window(self, controller):
        """ 
            Populates the page with elements and attributes.

            - controller : the application
        """
        # Query: Get all the participating Baltimore Public County Schools
        query = 'SELECT * FROM BPC'

        self.create_header(controller, 'All participating Baltimore County Public Schools')
        self.run_query(query)
        self.create_button(controller)

    ############################### PAGE PROPERTIES ############################### 

    def create_header(self, controller, header):
        """ 
            Creates a header for the current page.
            
            - controller : the application
            - header : contents of the header
        """
        label = tkinter.Label(self, text=header, font=controller.header_font)
        label.pack(side='top', fill='x', pady=20)

    def create_button(self, controller):
        """ 
            Creates a button for the current page.
            
            - controller : the application
        """
        button = tkinter.Button(self, text='Go to the start page', font=controller.button_font,
                           command=lambda: controller.show_frame('StartPage'))
        button.pack(pady=50)

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

        # fill the top row with the column names
        for index, name in enumerate(column_names, 1):
            self.results_table.heading(index, text=name)

        # fill the rest of the table values from the query
        for entry in results:
            self.results_table.insert('', tkinter.END, values=entry)

        self.results_table.pack(fill='both', expand=False)
        connection.close()
