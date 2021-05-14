import tkinter    
import sqlite3            

class EnterAVPage(tkinter.Frame):

    serial_number_entry = None
    serial_number_field = None
    model_number_entry = None
    model_number_field = None

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
        self.create_header(controller, 'Enter A/V equipment information')
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
        # label and field for serial number
        serial_number_label = tkinter.Label(self, text='Serial number', font=('Helvetica', 14))
        serial_number_label.pack()
        self.serial_number_entry = tkinter.StringVar()
        self.serial_number_field = tkinter.Entry(self, textvariable=self.serial_number_entry)
        self.serial_number_field.pack()

        # label and field for model number
        model_number_label = tkinter.Label(self, text='Model number', font=('Helvetica', 14))
        model_number_label.pack()
        self.model_number_entry = tkinter.StringVar()
        self.model_number_field = tkinter.Entry(self, textvariable=self.model_number_entry)
        self.model_number_field.pack()

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

        # Get the office ID number which was entered in the Equipment entry page
        cursor.execute('SELECT OfficeID FROM Office ORDER BY OfficeID DESC LIMIT 1') # gets the most recent office ID
        office_number = ''.join(cursor.fetchone()) # convert entry to a string

        # Get the room number based off the office ID number
        query_for_storage_location = 'SELECT RoomID FROM OFFICE WHERE OfficeID = "{}"' # gets the roomID 
        query_for_storage_location = query_for_storage_location.format(office_number) # complete the query
        cursor.execute(query_for_storage_location) # run another query for room number
        room_number = ''.join(cursor.fetchone()) # convert entry to a string
        room_number = 'Room ' + room_number

        cursor.execute("""INSERT INTO Audio_Visual_Eq(Serial_Number, Model_Number, TU_Tag_Number,
                                                      Storage_Location, Office_Location) 
                       VALUES (?, ?, ?, ?, ?)""",
        (self.serial_number_entry.get(), self.model_number_entry.get(), 
        tu_tag_number, room_number, office_number))

        print((self.serial_number_entry.get(), self.model_number_entry.get(), 
        tu_tag_number, room_number, office_number))

        connection.commit()
        connection.close()

    def clear_fields(self):
        """ 
            Clears the fields for user input 
        """
        self.serial_number_field.delete(0, 'end')
        self.model_number_field.delete(0, 'end')
