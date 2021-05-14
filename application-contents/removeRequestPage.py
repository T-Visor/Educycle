import tkinter    
import sqlite3            

class RemoveRequestPage(tkinter.Frame):

    service_ID_entry = None
    service_ID_field = None

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
        self.create_header(controller, 'Remove a service request')
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
        service_ID_label = tkinter.Label(self, text='Enter a service request ID', font=('Helvetica', 14))
        service_ID_label.pack()
        self.service_ID_entry = tkinter.StringVar()
        self.service_ID_field = tkinter.Entry(self, textvariable=self.service_ID_entry)
        self.service_ID_field.pack()

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        submit_button = tkinter.Button(self, text='Submit', font=controller.button_font,
                                command=lambda: [self.run_query(), self.clear_field()])
        submit_button.pack(pady=30)

        return_button = tkinter.Button(self, text='Return to view service requests', font=controller.button_font,
                                command=lambda: controller.show_frame('ServiceRequestsPage'))
        return_button.pack()

    ################################ EVENT HANDLERS ###################################

    def run_query(self):
        """
            Runs a query which will remove an entry from a table
        """
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')

        print(self.service_ID_entry.get())

        cursor.execute('DELETE FROM Service_Request WHERE MMSR_ID=?',
        ([self.service_ID_entry.get()])) # use brackets around the parameter to prevent an error binding with sqlite

        connection.commit()
        connection.close()

    def clear_field(self):
        """ 
            Clears the field for user input 
        """
        self.service_ID_field.delete(0, 'end')