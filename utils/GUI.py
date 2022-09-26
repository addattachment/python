from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter as tk

"""
Class to create the GUI to enter additional information
"""


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player_name = None
        self.title("AddAttachment")

        window_width = 1200
        window_height = 800
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
        textbox = ttk.Entry(name_frame, textvariable=self.player_name)
        textbox.pack(fill="x", expand=True)

        # entered_button = ttk.Button(name_frame, text="Enter", command=self.login_clicked)
        # entered_button.pack(fill="x", expand=True, pady=10)

        close_button = ttk.Button(name_frame, text="Save & close", command=self.destroy)
        close_button.pack(pady=20)

    # def login_clicked(self):
    #     """ callback when the login button clicked
    #     """
    #     msg = f'You entered name: {self.player_name.get()}'
    #     showinfo(
    #         title='Information',
    #         message=msg
    #     )

    def get_results(self):
        return self.player_name.get()
