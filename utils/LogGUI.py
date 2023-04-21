# self.input_frame = ttk.Frame(self)
#         self.input_frame.pack(padx=10, pady=10, fill='x', expand=True)
#         # Add text widget to display logging info
#         st = ScrolledText(self.input_frame, state='disabled')
#         st.configure(font='TkFixedFont')
#         st.grid(column=0, row=1)#, sticky='w', columnspan=4)
#         # Create textLogger
#         text_handler = TextHandler(st)
#
#         # Logging configuration
#         logging.basicConfig(filename='test.log',
#                             level=logging.INFO,
#                             format='%(asctime)s - %(levelname)s - %(message)s')
#
#         # Add the handler to logger
#         logger = logging.getLogger()
#         logger.addHandler(text_handler)
import logging
import tkinter
from tkinter import *
import threading


class App(threading.Thread):

    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()
        logging.info("here")

    def run(self):
        loop_active = True
        while loop_active:
            user_input = raw_input("Give me your command! Just type \"exit\" to close: ")
            if user_input == "exit":
                loop_active = False
                self.root.quit()
                self.root.update()
            else:
                label = Label(self.root, text=user_input)
                label.pack()


ROOT = Tk()
APP = App(ROOT)
LABEL = Label(ROOT, text="Hello, world!")
LABEL.pack()
ROOT.mainloop()
