import customtkinter as ctk

from config import *
from letterguesser.gui.frames import HeaderFrame, MainFrame

from letterguesser.styles.padding import pad_0, pad_6
from context import localisation, manager


class App(ctk.CTk):
    def __init__(self):

        # windows setup
        super().__init__()
        self.title(APP_TITLE)

        # from context set global localisation instance
        self.localisation = localisation
        self.manager = manager

        self.attributes('-topmost', True)  # for easier testing, can be removed if needed

        # offsets to run app in the center of the screen 
        display = (self.winfo_screenwidth(), self.winfo_screenheight())  # host display width x height
        left = int(display[0] / 2 - APP_SIZE[0] / 2)
        top = int(display[1] / 2 - APP_SIZE[1] / 2)
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{left}+{top}')

        # windows constraints
        self.minsize(APP_SIZE[0], APP_SIZE[1])  # precaution, if resizable(false, false) fails
        self.maxsize(APP_SIZE[0], APP_SIZE[1])  # precaution, if resizable(false, false) fails
        self.resizable(False, False)

        # main layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.header_frame = HeaderFrame(self)
        self.header_frame.grid(row=0, column=0, sticky='nsew', padx=pad_6, pady=pad_6)

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=1, column=0, sticky='nsew', padx=pad_6, pady=(pad_0, pad_6))

        # key binds
        self.bind('<Escape>', lambda event: self.quit())
        self.bind('<Control-l>', lambda event: self.header_frame.toggle_langauge())

        # run app
        self.mainloop()


if __name__ == "__main__":
    App()
# end main
