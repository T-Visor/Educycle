import tkinter    
import sqlite3            

class CreateRequestPage(tkinter.Frame):

    tag_number_choice = None
    priority_level_choice = None
    department_choice = None
    school_choice = None
    staff_choice = None
    start_date_entry = None
    start_date_field = None
    end_date_entry = None
    end_date_field = None

    def __init__(self, parent, controller):
        """ 
            Constructs a new page.

            - parent : the parent class
            - controller : the application
        """
        tkinter.Frame.__init__(self, parent)
        self.controller = controller # for switching between pages

        # for getting a menu options
        self.tag_number_choice = tkinter.StringVar(self)
        self.priority_level_choice = tkinter.StringVar(self)
        self.department_choice = tkinter.StringVar(self)
        self.school_choice = tkinter.StringVar(self)
        self.staff_choice = tkinter.StringVar(self)

        self.populate_window(controller)

    def populate_window(self, controller):
        """ 
            Populates the page with elements and attributes.

            - controller : the application
        """
        self.create_header(controller, 'Create a new service request ticket')
        self.create_menus()
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

    def create_menus(self):
        """ 
            Creates drop-down menus for the current page. 
        """
        # label and drop-down menu for TU tag number
        tag_number_label = tkinter.Label(self, text='TU tag number', font=('Helvetica', 14))
        tag_number_label.pack()
        tag_numbers = self.get_column_info('SELECT TU_Tag_Number FROM Equipment')
        self.tag_number_choice.set(tag_numbers[0])
        tag_number_menu = tkinter.OptionMenu(self, self.tag_number_choice, *tag_numbers)
        tag_number_menu.pack()

        # label and drop-down menu for priority levels
        priority_level_label = tkinter.Label(self, text='Priority level', font=('Helvetica', 14))
        priority_level_label.pack()
        priority_levels = ['1', '2', '3', '4', '5']
        self.priority_level_choice.set(priority_levels[0])
        priority_menu = tkinter.OptionMenu(self, self.priority_level_choice, *priority_levels)
        priority_menu.pack()

        # label and drop-down menu for departments
        department_label = tkinter.Label(self, text='Department', font=('Helvetica', 14))
        department_label.pack()
        departments = self.get_column_info('SELECT Department_name FROM Department')
        self.department_choice.set(departments[0])
        department_menu = tkinter.OptionMenu(self, self.department_choice, *departments)
        department_menu.pack()

        # label and drop-down menu for schools
        school_label = tkinter.Label(self, text='Off Campus School', font=('Helvetica', 14))
        school_label.pack()
        schools = self.get_column_info('SELECT School_Name FROM BPC')
        self.school_choice.set(schools[0])
        school_menu = tkinter.OptionMenu(self, self.school_choice, *schools)
        school_menu.pack()

        # label and drop-down menu for staff
        staff_label = tkinter.Label(self, text='Staff', font=('Helvetica', 14))
        staff_label.pack()
        staff = self.get_column_info('SELECT Name FROM Faculty_Staff')
        self.staff_choice.set(staff[0])
        staff_menu = tkinter.OptionMenu(self, self.staff_choice, *staff)
        staff_menu.pack()

    def create_fields(self):
        """ 
            Create fields for requesting user input 
        """
        # label and field for username
        start_date_label = tkinter.Label(self, text='Start date (mm/dd/yyyy)', font=('Helvetica', 14))
        start_date_label.pack()
        self.start_date_entry = tkinter.StringVar()
        self.start_date_field = tkinter.Entry(self, textvariable=self.start_date_entry)
        self.start_date_field.pack()

        # label and field for password
        end_date_label = tkinter.Label(self, text='End date (mm/dd/yyyy)', font=('Helvetica', 14))
        end_date_label.pack()
        self.end_date_entry = tkinter.StringVar()
        self.end_date_field = tkinter.Entry(self, textvariable=self.end_date_entry)
        self.end_date_field.pack()

    def create_buttons(self, controller):
        """ 
            Creates buttons for the current page.
            
            - controller : the application
        """
        submit_button = tkinter.Button(self, text='Submit request', font=controller.button_font,
                                command=lambda: [self.run_query(), self.clear_fields()])
        submit_button.pack(pady=30)

        return_button = tkinter.Button(self, text='Return to view service requests', font=controller.button_font,
                                command=lambda: controller.show_frame('ServiceRequestsPage'))
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

    def clear_fields(self):
        """ 
            Clears the fields for user input 
        """
        self.start_date_field.delete(0, 'end')
        self.end_date_field.delete(0, 'end')

    def run_query(self):
        """
            Runs a query which will insert all values
            from the page into the table.
        """
        connection = sqlite3.connect('EduCycle.db')
        cursor = connection.cursor()

        # generate a new primary key for the current request
        cursor.execute('SELECT MMSR_ID FROM Service_Request ORDER BY MMSR_ID DESC LIMIT 1') # gets the most recent service ID
        service_request_ID = ''.join(cursor.fetchone()) # convert entry to a string
        service_request_ID = int(service_request_ID) + 1 # increment value by 1

        cursor.execute("""INSERT INTO Service_Request(MMSR_ID, TU_Tag_Number, Priority_level,
                                               Departmment, Off_Campus, Staff_overseer,
                                               StartDate, EndDate) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (service_request_ID, self.tag_number_choice.get(), self.priority_level_choice.get(),
         self.department_choice.get(), self.school_choice.get(), 
         self.staff_choice.get(), self.start_date_entry.get(), self.end_date_entry.get()))

        connection.commit()
        connection.close()
