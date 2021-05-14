import tkinter    
import sqlite3            

class EnterEquipmentPage(tkinter.Frame):

    equipment_choice = None
    storage_location_choice = None

    def __init__(self, parent, controller):
        """ 
            Constructs a new page.

            - parent : the parent class
            - controller : the application
        """
        tkinter.Frame.__init__(self, parent)
        self.controller = controller # for switching between pages

        # for getting menu options
        self.equipment_choice = tkinter.StringVar(self)
        self.storage_location_choice = tkinter.StringVar(self)

        self.populate_window(controller)

    def populate_window(self, controller):
        """ 
            Populates the page with elements and attributes.

            - controller : the application
        """
        self.create_header(controller, 'Enter new equipment')
        self.create_menus()
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

    def create_menus(self):
        """ 
            Creates drop-down menus for the current page. 
        """
        # label and drop-down menu equipment type
        equipment_type_label = tkinter.Label(self, text='Equipment type', font=('Helvetica', 14))
        equipment_type_label.pack()
        equipment_types = ['AV equip', 'computer', 'Comp part']
        self.equipment_choice.set(equipment_types[0])
        equipment_menu = tkinter.OptionMenu(self, self.equipment_choice, *equipment_types)
        equipment_menu.pack()

        # label and drop-down menu for storage location number
        storage_location_label = tkinter.Label(self, text='Storage location number', font=('Helvetica', 14))
        storage_location_label.pack()
        location_numbers = self.get_column_info('SELECT OfficeID FROM Office')
        self.storage_location_choice.set(location_numbers[0])
        storage_location_menu = tkinter.OptionMenu(self, self.storage_location_choice, *location_numbers)
        storage_location_menu.pack()

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        submit_button = tkinter.Button(self, text='Submit information', font=controller.button_font,
                                command=lambda: [self.run_query(), self.choose_next_page(controller)])
        submit_button.pack(pady=30)

        return_button = tkinter.Button(self, text='Return to view equipment', font=controller.button_font,
                                command=lambda: controller.show_frame('EquipmentPage'))
        return_button.pack()

    ################################ HELPER METHOD ###################################

    def get_column_info(self, query):
        """
            Uses a query to retrieve all entries from a column.

            - query : the sqlite query statement

            returns : a list of column values from the query
        """
        results = []
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()

        cursor.execute(query)

        # get the query results as a list of strings
        for entry in cursor:
            results.append(str(entry))

        # strip away the unnecessary characters which are present
        # when the query results were converted to strings
        for i, result in enumerate(results):
            results[i] = results[i].replace('(', '')
            results[i] = results[i].replace(')', '')
            results[i] = results[i].replace(',', '')
            results[i] = results[i].replace("'", '')

        connection.close()
        return results

    ################################ EVENT HANDLERS ###################################

    def run_query(self):
        """
            Runs a query which will insert all values
            from the page into the table.
        """
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()

        # generate a new tag number for the current piece of equipment
        cursor.execute('SELECT TU_Tag_Number FROM Equipment ORDER BY TU_Tag_Number DESC LIMIT 1') # gets the most recent service ID
        tu_tag_number = ''.join(cursor.fetchone()) # convert entry to a string
        tu_tag_number = int(tu_tag_number) + 1 # increment value by 1

        # generate a new manufacturer code for the current piece of equipment
        cursor.execute('SELECT Manufacturer_code FROM Equipment ORDER BY Manufacturer_code DESC LIMIT 1') # gets the most recent service ID
        manufacturer_code = ''.join(cursor.fetchone()) # convert entry to a string
        manufacturer_code = int(manufacturer_code) + 1 # increment value by 1

        cursor.execute("""INSERT INTO Equipment(TU_Tag_Number, Manufacturer_code,
                                                Type, Storage_location) 
                       VALUES (?, ?, ?, ?)""",
        (tu_tag_number, manufacturer_code, self.equipment_choice.get(), self.storage_location_choice.get()))

        connection.commit()
        connection.close()

    def choose_next_page(self, controller):
        """
            Determines which page to go into
            based off a selection from the user

            controller : the application
        """
        type_of_equipment = self.equipment_choice.get()

        if type_of_equipment == 'AV equip':
            controller.show_frame('EnterAVPage')
        elif type_of_equipment == 'computer':
            controller.show_frame('EnterComputerPage')
        elif type_of_equipment == 'Comp part':
            controller.show_frame('EnterPartPage')
