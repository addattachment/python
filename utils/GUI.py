from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter as tk

"""
Class to create the GUI to enter additional information
"""


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player_treatment = None
        self.age_error = None
        self.textbox_label = None
        self.textbox_age = None
        self.player_gender = None
        self.player_age = None
        self.player_id = None
        self.contingency = None
        self.title("AddAttachment")

        window_width = 400
        window_height = 400
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.create_widgets()

    def create_widgets(self):
        name_frame = ttk.Frame(self)
        name_frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.player_name = tk.StringVar()
        ttk.Label(name_frame, justify=tk.LEFT, text="Naam speler").grid(row=0)
        textbox = ttk.Entry(name_frame, textvariable=self.player_name)
        textbox.grid(row=0, column=1)

        self.player_id = tk.StringVar()
        ttk.Label(name_frame, justify=tk.LEFT, text="Identificatie speler").grid(row=1)
        textbox = ttk.Entry(name_frame, textvariable=self.player_id)
        textbox.grid(row=1, column=1)

        self.contingency = tk.IntVar()
        tk.Label(name_frame, justify=tk.LEFT, text="Contingentie speler").grid(row=2)
        radio_cont = ttk.Radiobutton(name_frame, text="20", variable=self.contingency, value=20)
        radio_cont.grid(row=2, column=1)
        radio_cont2 = ttk.Radiobutton(name_frame, text="80", variable=self.contingency, value=80)
        radio_cont2.grid(row=2, column=2)
        # entered_button = ttk.Button(name_frame, text="Enter", command=self.login_clicked)
        # entered_button.pack(fill="x", expand=True, pady=10)

        vcmd = (self.register(self.validate_age), '%P')
        ivcmd = (self.register(self.on_invalid),)
        self.player_age = tk.IntVar()
        self.textbox_label = ttk.Label(name_frame, foreground='red', justify=tk.LEFT, text="Leeftijd speler")
        self.textbox_label.grid(row=3)
        self.textbox_age = ttk.Entry(name_frame, textvariable=self.player_age)
        self.textbox_age.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.textbox_age.grid(row=3, column=1)
        self.age_error = ttk.Label(name_frame, foreground='red')
        self.age_error.grid(row=3, column=2)

        self.player_gender = tk.StringVar()
        tk.Label(name_frame, justify=tk.LEFT, text="Geslacht speler").grid(row=4)
        radio_gend = ttk.Radiobutton(name_frame, text="M", variable=self.player_gender, value="M")
        radio_gend.grid(row=4, column=1)
        radio_gend2 = ttk.Radiobutton(name_frame, text="V", variable=self.player_gender, value="V")
        radio_gend2.grid(row=4, column=2)

        self.player_treatment = tk.StringVar()
        tk.Label(name_frame, justify=tk.LEFT, text="Treatment speler").grid(row=5)
        radio_treat = ttk.Radiobutton(name_frame, text="A", variable=self.player_treatment, value="A")
        radio_treat.grid(row=5, column=1)
        radio_treat2 = ttk.Radiobutton(name_frame, text="B", variable=self.player_treatment, value="B")
        radio_treat2.grid(row=5, column=2)

        close_button = ttk.Button(name_frame, text="Save & close", command=self.destroy)
        close_button.grid(row=8, column=0)

    # def login_clicked(self):
    #     """ callback when the login button clicked
    #     """
    #     msg = f'You entered name: {self.player_name.get()}'
    #     showinfo(
    #         title='Information',
    #         message=msg
    #     )

    def get_results(self):
        results = {
            "name": self.player_name.get(),
            "id": self.player_id.get(),
            "contingency": self.contingency.get(),
            "age": self.player_age.get(),
            "gender": self.player_gender.get(),
            "treatment": self.player_treatment.get()
        }
        return results

    def show_message(self, error='', color='black'):
        self.age_error['text'] = error
        self.textbox_label['foreground'] = color
        self.textbox_age['foreground'] = color

    def validate_age(self, value):
        if int(value) < 9 or int(value) > 12:
            return False
        self.show_message()
        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        print("not good")
        self.show_message('Please enter a valid age', 'red')
