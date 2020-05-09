import tkinter    
import sqlite3            

class EnterPartPage(tkinter.Frame):

    parts_ID_entry = None
    parts_ID_field = None
    peripheral_type_entry = None
    peripheral_type_field = None

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
        self.create_header(controller, 'Enter computer peripheral information')
        self.create_fields()
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

    def create_fields(self):
        """ 
            Create fields for requesting user input 
        """
        # label and field for model number
        parts_ID_label = tkinter.Label(self, text='Parts ID', font=('Helvetica', 14))
        parts_ID_label.pack()
        self.parts_ID_entry = tkinter.StringVar()
        self.parts_ID_field = tkinter.Entry(self, textvariable=self.parts_ID_entry)
        self.parts_ID_field.pack()

        # label and field for manufacturer
        peripheral_type_label = tkinter.Label(self, text='Type (mouse, keyboard, etc)', font=('Helvetica', 14))
        peripheral_type_label.pack()
        self.peripheral_type_entry = tkinter.StringVar()
        self.peripheral_type_field = tkinter.Entry(self, textvariable=self.peripheral_type_entry)
        self.peripheral_type_field.pack()

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        submit_button = tkinter.Button(self, text='Submit information', font=controller.button_font,
                                command=lambda: [self.run_query(), self.clear_fields()])
        submit_button.pack(pady=30)

        return_button = tkinter.Button(self, text='Return to view equipment', font=controller.button_font,
                                command=lambda: controller.show_frame('EquipmentPage'))
        return_button.pack()

    ################################ EVENT HANDLERS ###################################

    def run_query(self):
        """
            Runs a query which will insert all values
            from the page into the table.
        """
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()

        # Get the tag number which was entered in the Equipment entry page
        cursor.execute('SELECT TU_Tag_Number FROM Equipment ORDER BY TU_Tag_Number DESC LIMIT 1') # gets the most recent tag number
        tu_tag_number = ''.join(cursor.fetchone()) # convert entry to a string

        # Get the current location which was entered in the Equipment entry page
        cursor.execute('SELECT Storage_Location FROM Equipment ORDER BY Storage_Location DESC LIMIT 1') # gets the most recent location number
        current_location = ''.join(cursor.fetchone()) # convert entry to a string

        cursor.execute("""INSERT INTO Computer_Parts(PartsID, TU_Tag_Number, Parts_Type, current_location) 
                       VALUES (?, ?, ?, ?)""",
        (self.parts_ID_entry.get(), tu_tag_number, self.peripheral_type_entry.get(), current_location))

        connection.commit()
        connection.close()

    def clear_fields(self):
        """ 
            Clears the fields for user input 
        """
        self.parts_ID_field.delete(0, 'end')
        self.peripheral_type_field.delete(0, 'end')
