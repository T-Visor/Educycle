import tkinter    
import sqlite3            

class EnterComputerPage(tkinter.Frame):

    model_number_entry = None
    model_number_field = None
    computer_type_entry = None
    computer_type_field = None
    cost_entry = None
    cost_field = None
    is_educycle_entry = None
    is_educycle_field = None

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
        self.create_header(controller, 'Enter computer information')
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
        model_number_label = tkinter.Label(self, text='Model number', font=('Helvetica', 14))
        model_number_label.pack()
        self.model_number_entry = tkinter.StringVar()
        self.model_number_field = tkinter.Entry(self, textvariable=self.model_number_entry)
        self.model_number_field.pack()

        # label and field for manufacturer
        computer_type_label = tkinter.Label(self, text='Manufacturer', font=('Helvetica', 14))
        computer_type_label.pack()
        self.computer_type_entry = tkinter.StringVar()
        self.computer_type_field = tkinter.Entry(self, textvariable=self.computer_type_entry)
        self.computer_type_field.pack()

        # label and field for cost
        cost_label = tkinter.Label(self, text='Cost', font=('Helvetica', 14))
        cost_label.pack()
        self.cost_entry = tkinter.StringVar()
        self.cost_field = tkinter.Entry(self, textvariable=self.cost_entry)
        self.cost_field.pack()

        # label and field for this computer being an EduCycle computer
        is_educycle_label = tkinter.Label(self, text='EduCycle computer? (Y/n)', font=('Helvetica', 14))
        is_educycle_label.pack()
        self.is_educycle_entry = tkinter.StringVar()
        self.is_educycle_field = tkinter.Entry(self, textvariable=self.is_educycle_entry)
        self.is_educycle_field.pack()

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

        cursor.execute("""INSERT INTO Computer(Model_Number, TU_Tag_Number, Computer_Type,
                                               Current_Location, Cost, EduCycle_Computer) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
        (self.model_number_entry.get(), tu_tag_number, self.computer_type_entry.get(),
         office_number, self.cost_entry.get(), self.is_educycle_entry.get()))

        print(self.model_number_entry.get(), tu_tag_number, self.computer_type_entry.get(),
         office_number, self.cost_entry.get(), self.is_educycle_entry.get())

        connection.commit()
        connection.close()

    def clear_fields(self):
        """ 
            Clears the fields for user input 
        """
        self.model_number_field.delete(0, 'end')
        self.computer_type_field.delete(0, 'end')
        self.is_educycle_field.delete(0, 'end')
        self.cost_field.delete(0, 'end')
