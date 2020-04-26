import tkinter                

class LoginPage(tkinter.Frame):

    username_entry = None
    username_field = None
    password_entry = None
    password_field = None

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
        self.create_fields()
        self.create_button(controller)

    ############################### PAGE PROPERTIES ############################### 

    def create_fields(self):
        """ 
            Create fields for requesting user input 
        """
        # label and field for username
        self.username_label = tkinter.Label(self, text='username', font=('Helvetica', 14))
        self.username_label.pack()
        self.username_entry = tkinter.StringVar()
        self.username_field = tkinter.Entry(self, textvariable=self.username_entry)
        self.username_field.pack()

        # label and field for password
        self.password_label = tkinter.Label(self, text='password', font=('Helvetica', 14))
        self.password_label.pack()
        self.password_entry = tkinter.StringVar()
        self.password_field = tkinter.Entry(self, textvariable=self.password_entry, show='*')
        self.password_field.pack()

    def create_button(self, controller):
        """ 
            Creates a button for the current page.
            
            - controller : the application
        """
        button = tkinter.Button(self, text='Enter', font=('Helvetica', 14),
                                command=lambda: [self.enter_credentials(controller), self.clear_fields()])
        button.place(relx=0.5, rely=0.3, anchor='center')

    ################################ EVENT HANDLERS ###################################

    def enter_credentials(self, controller):
        """ 
            Submits the credentials from the fields

            - controller : the application
        """
        if self.username_entry.get() == 'educycle' and self.password_entry.get() == 'database':
            controller.show_frame('StartPage')
        else:
            print('Wrong username or password')

    def clear_fields(self):
        """ 
            Clears the fields for user input 
        """
        self.username_field.delete(0, 'end')
        self.password_field.delete(0, 'end')
