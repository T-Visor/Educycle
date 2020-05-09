import tkinter    
import sqlite3            

class RemoveEquipmentPage(tkinter.Frame):

    tag_number_entry = None
    tag_number_field = None

    def __init__(self, parent, controller):
        """ 
            Constructs a new page.

            - parent : the parent class
            - controller : the application
        """
        tkinter.Frame.__init__(self, parent)
        self.controller = controller # for switching between pages
        self.populate_window(controller)

    def populate_window(self, controller):
        """ 
            Populates the page with elements and attributes.

            - controller : the application
        """
        self.create_header(controller, 'Remove equipment')
        self.create_field()
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

    def create_field(self):
        """ 
            Creates a field for requesting user input 
        """
        # label and field for TU tag number
        tag_number_label = tkinter.Label(self, text='Enter TU tag number', font=('Helvetica', 14))
        tag_number_label.pack()
        self.tag_number_entry = tkinter.StringVar()
        self.tag_number_field = tkinter.Entry(self, textvariable=self.tag_number_entry)
        self.tag_number_field.pack()

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        submit_button = tkinter.Button(self, text='Submit', font=controller.button_font,
                                command=lambda: [self.run_query(), self.clear_field()])
        submit_button.pack(pady=30)

        return_button = tkinter.Button(self, text='Return to view equipment', font=controller.button_font,
                                command=lambda: controller.show_frame('EquipmentPage'))
        return_button.pack()

    ################################ EVENT HANDLERS ###################################

    def run_query(self):
        """
            Runs a query which will remove an entry from a table
        """
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')

        cursor.execute('DELETE FROM Equipment WHERE TU_Tag_Number=?',
        ([self.tag_number_entry.get()])) # use brackets around the parameter to prevent an error binding with sqlite

        connection.commit()
        connection.close()

    def clear_field(self):
        """ 
            Clears the field for user input 
        """
        self.tag_number_field.delete(0, 'end')