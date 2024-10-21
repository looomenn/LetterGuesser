"""
LetterGuesser
Author: Ange1o
License: MIT
Version: v3
"""

import json
import random

from CTkTable import *
import customtkinter as ctk

from gui.frames import *
from config import *
from styles import *


from logic import utils
from context import localisation
# from logic.ExperimentManger import ExperimentManger

ctk.set_appearance_mode('light')

# APP_LANGUAGE_DATA: dict = {}  # where language data stored when load_language() called
# APP_WIDGETS_BINDINGS: dict = {}  # where the binding of widget label and localisation key is stored


# def load_language(lang_code) -> None:
#     global APP_LANGUAGE_DATA
#     global APP_CURRENT_LANGUAGE
#
#     APP_CURRENT_LANGUAGE = lang_code
#
#     lang_file_path = get_resource_path(f"lang/{lang_code}.json")
#     with open(lang_file_path, 'r', encoding='utf-8') as file:
#         APP_LANGUAGE_DATA = json.load(file)
#
#     localisation_update()

#
# def load_texts(lang_code: str):
#     file_path = utils.get_resource_path(f'texts/{lang_code}.txt')
#
#     with open(file_path, 'r', encoding='utf-8') as file:
#         text_data = file.read()
#     return text_data.replace('\n', '_').replace(' ', '_')
#
#
# def bind_localisation(widget, translation_key, update_method=None) -> None:
#     APP_WIDGETS_BINDINGS[widget] = (translation_key, update_method)
#     update_widget_localisation(widget)
#
#
# def update_widget_localisation(widget) -> None:
#     key, method = APP_WIDGETS_BINDINGS[widget]
#     translated_text = APP_LANGUAGE_DATA.get(key, f'Missing: {key}')
#     if method:
#         method(translated_text)
#     else:
#         widget.configure(text=translated_text)
#
#
# def localisation_update():
#     for widget in APP_WIDGETS_BINDINGS:
#         update_widget_localisation(widget)
#
#
# def get_alphabet(lang_code):
#     return 'abcdefghijklmnopqrstuvwxyz ' if lang_code == 'en' else 'йцукенгшщзхїфівапролджєґячсмитьбю '


# class Actions(ctk.CTkFrame):
#     def __init__(self, parent, manager, **kwargs):
#         super().__init__(parent, **kwargs)
#
#         # init manager from the Input Frame
#         self.manager: ExperimentManager = manager
#
#         self.configure(fg_color='transparent')
#
#         self.rowconfigure(0, weight=0)
#         self.columnconfigure((1, 3), minsize=PADDING_8)
#         self.columnconfigure((0, 2, 4), weight=0)
#
#         self.next_button: Button = Button(
#             self,
#             'start',
#             command=self.start_experiment,
#             style='primary'
#         )
#         self.next_button.grid(row=0, column=0, sticky='w')
#
#         self.ngram_selector: OptionMenu = OptionMenu(
#             self,
#             'char_numbers',
#             command=self.select_ngram,
#             initial_value=5,
#             values=[i for i in range(5, 55, 5)]
#         )
#         self.ngram_selector.grid(row=0, column=2, sticky='')
#
#         self.reset_button: Button = Button(
#             self,
#             'reset_button_label',
#             command=self.reset_button,
#             style='danger',
#             is_disabled=False
#         )
#         self.reset_button.grid(row=0, column=4, sticky='w')
#
#         # sending buttons to the manager
#         self.manager.load_buttons([self.next_button, self.ngram_selector, self.reset_button])
#         self.manager.load_actions(self)
#
#     def start_experiment(self):
#         self.ngram_selector.configure(hover=False, state='disabled')
#         self.manager.start_experiment()
#
#     def reset_button(self):
#         self.ngram_selector.configure(hover=True, state='normal')
#         self.manager.reset_experiment()
#
#     def select_ngram(self, value):
#         self.manager.change_ngram(int(value.split(' ')[0]))
#
#
# class InputFrame(ctk.CTkFrame):
#     def __init__(self, parent, manager, **kwargs):
#         super().__init__(parent, **kwargs)
#
#         # init manager (from the LeftFrame)
#         self.manager: ExperimentManager = manager
#
#         # layout+
#         self.rowconfigure((0, 2, 4, 6), weight=1)
#         self.rowconfigure(1, minsize=PADDING_24)
#         self.rowconfigure((3, 5), minsize=PADDING_32)
#         self.columnconfigure(0, weight=1)
#
#         # where the random part from the text will be displayed
#         self.random_text_block = TextBlockSegment(self, localisation_key="random_text_part", initial_text="random_text")
#         self.random_text_block.grid(row=0, column=0, sticky='nsew', padx=PADDING_24, pady=(PADDING_24, PADDING_NONE))
#
#         # block for the used chars
#         self.used_chars_block = TextBlockSegment(self, localisation_key="used_chars", initial_text="random_text")
#         self.used_chars_block.grid(row=2, column=0, sticky='nsew', padx=PADDING_24)
#
#         # main input
#         self.input_block = InputSegment(
#             self,
#             manager,
#             'main_input_label',
#             'main_input_placeholder',
#             True
#         )
#         self.input_block.grid(row=4, column=0, sticky='nsew', padx=PADDING_24)
#
#         # buttons
#         self.actions = Actions(self, self.manager)
#         self.actions.grid(row=6, column=0, sticky='nsew', pady=(PADDING_NONE, PADDING_24), padx=PADDING_24)
#
#     def get_random_text_block(self):
#         """ util function to access specific block from the class """
#         return self.random_text_block
#
#     def get_used_chars_block(self):
#         """ util function to access specific block from the class """
#         return self.used_chars_block
#
#     def get_input_block(self):
#         return self.input_block
#
#
# class StatusFrame(ctk.CTkFrame):
#     def __init__(self, parent, **kwargs):
#         super().__init__(parent, **kwargs)
#
#         self.grid_rowconfigure(0, weight=1)
#         self.columnconfigure(0, weight=1)
#
#         self.status = TextBlockSegment(
#             self,
#             'status_label',
#             'random_text'
#         )
#         self.status.grid(row=0, column=0, sticky='nsew', padx=PADDING_24, pady=PADDING_24)
#
#     def get_status_block(self):
#         return self.status
#
#     def update_status(self, key):
#         bind_localisation(self.status.text_block, key, self.status.update_value)
#
#
# # class LeftFrame(ctk.CTkFrame):
# #     def __init__(self, parent, manager, **kwargs):
# #         super().__init__(parent, **kwargs)
# #
# #         # init experiment manager
# #         self.manager: ExperimentManager = manager
# #
# #         # remove gray background from the frame
# #         self.configure(fg_color='transparent')
# #
# #         # layout settings
# #         self.rowconfigure(0, minsize=100)  # cards
# #         self.rowconfigure(2, weight=1)  # input frame
# #         self.rowconfigure((1, 3), minsize=PADDING_16)  # row gap (16px)
# #         self.rowconfigure(4, weight=0)  # status frame
# #         self.columnconfigure(0, weight=1)  # for grid to work correctly
# #
# #         # init cards
# #         self.cards = Cards(self, fg_color='transparent')
# #         self.cards.grid(row=0, column=0, sticky='nsew')
# #
# #         # init input frame (core of the program)
# #         self.input_frame = InputFrame(self, self.manager)
# #         self.input_frame.grid(row=2, column=0, sticky='nsew')
# #
# #         # init status frame
# #         self.status_frame = StatusFrame(self)
# #         self.status_frame.grid(row=4, column=0, sticky='nsew')
# #
# #     def get_widgets(self):
# #         """ returns list of the main widgets in the left frame """
# #         return [self.cards, self.input_frame, self.status_frame]
#
#
# class ProbabilityTable(ctk.CTkScrollableFrame):
#     def __init__(self,  parent, **kwargs):
#         super().__init__(parent, **kwargs)
#
#         self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
#         self.alphabet_len = len(self.alphabet)
#         self.probability_data = []
#
#         self.rowconfigure((0, 1), weight=1)
#         self.columnconfigure(0, weight=1)
#
#         # frame title
#         self.title_label = ctk.CTkLabel(
#             self,
#             text='',
#             anchor='w',
#             height=TEXT_BODY_MEDIUM_HEIGHT,
#             font=ctk.CTkFont(
#                 family=FONT,
#                 size=TEXT_BODY_MEDIUM,
#                 weight='bold'
#             )
#         )
#         bind_localisation(self.title_label, 'probability')
#         self.title_label.grid(
#             row=0, column=0, sticky='nsew',
#             padx=PADDING_12, pady=(PADDING_12, PADDING_16)
#         )
#
#         # table placeholder
#         self.placeholder = ctk.CTkLabel(
#             self,
#             text='text-placeholder',
#             height=TEXT_BODY_MEDIUM_HEIGHT,
#             font=ctk.CTkFont(
#                 family=FONT,
#                 size=TEXT_BODY_MEDIUM
#             ),
#             text_color=TEXT_SECONDARY
#         )
#
#         bind_localisation(self.placeholder, 'table_placeholder')
#         self.placeholder.grid(row=1, column=0, sticky='nsew', pady=(72, 0))
#
#         # table
#         self.table = CTkTable(self, column=2, corner_radius=8, row=self.alphabet_len, justify='w')
#         self.table.grid(row=1, column=0, sticky='nsew', padx=PADDING_12)
#         self.table.grid_remove()
#
#         self.header_keys: list[str] = ['attempt', 'probability']
#         self.headers: list = ['', '']
#         self.bind_headers()
#
#         # self.init_table()
#
#     def bind_headers(self):
#         self.header_attempt, self.header_prob = ctk.CTkLabel(self, text=''), ctk.CTkLabel(self, text='')
#
#         bind_localisation(self.header_attempt, 'attempt', self.update_header_attempt)
#         bind_localisation(self.header_prob, 'probability', self.update_header_prob)
#
#     def update_header_attempt(self, text):
#         self.headers[0] = text
#         self.update_table()
#
#     def update_header_prob(self, text):
#         self.headers[1] = text
#         self.update_table()
#
#     def show_placeholder(self):
#         # showing placeholder
#         self.placeholder.grid()
#         self.table.grid_remove()
#
#     def hide_placeholder(self):
#         self.placeholder.grid_remove()
#         self.table.grid()
#
#     def init_table(self):
#         self.probability_data = [self.headers]
#
#         for i in range(1, self.alphabet_len + 1):
#             self.probability_data.append([i, 0])
#
#         self.update_table()
#
#     def update_table(self):
#         if not self.probability_data or len(self.probability_data) == 1:
#             self.show_placeholder()
#         else:
#             self.hide_placeholder()
#             self.table.update_values(self.probability_data)
#
#     def get_row(self, index):
#         if index == 0:
#             raise IndexError('You trying to access table header')
#
#         return self.table.get_row(index)
#
#     def check_index(self, index):
#
#         for idx, row in enumerate(self.probability_data):
#             if row[0] == index:
#                 return index
#         return None
#
#     def update_prob(self, index, new_value: int | float):
#
#         idx = self.check_index(index)
#
#         if idx is None or idx > len(self.probability_data):
#             raise IndexError('No such index')
#
#         self.table.insert(idx, 1, new_value)
#
#     def reset(self):
#         self.probability_data = []
#         self.update_table()
#
#
# class GuessedChars(ctk.CTkScrollableFrame):
#     def __init__(self, parent, manager, **kwargs):
#         super().__init__(parent, **kwargs)
#
#         self.manager: ExperimentManager = manager
#
#         self.columnconfigure(0, weight=1)
#
#         self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
#         self.alphabet_len = len(self.alphabet)
#         self.guessed_data = []
#
#         self.table = CTkTable(
#             self,
#             hover=False,
#             row=self.alphabet_len,
#             column=1,
#             justify='left',
#         )
#         self.table.grid(row=0, column=0, sticky='nsew', padx=PADDING_12)
#
#     def placeholder(self):
#         self.table.add_row('Data is absent')
#
#     def clear_placeholder(self):
#         self.table.update_values([''])
#
#     def add_char(self, char, attempt):
#         binary = ['0'] * self.alphabet_len
#
#         if attempt <= self.alphabet_len:
#             binary[attempt - 1] = '1'
#
#         binary_string = ''.join(binary)
#
#         symbol_label = f'Symbol: {char:}     Attempt: {attempt}\n{binary_string}'
#
#         self.guessed_data.append([symbol_label])
#
#         self.table.update_values(self.guessed_data)
#
#
# class RightFrame(ctk.CTkFrame):
#     def __init__(self, parent, manager, **kwargs):
#         super().__init__(parent, **kwargs)
#
#         self.manager: ExperimentManager = manager
#
#         self.configure(fg_color='transparent')
#
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure((0, 2), weight=1)
#         self.rowconfigure(1, minsize=PADDING_16)
#
#         self.probability_table: ProbabilityTable = ProbabilityTable(self)
#         self.probability_table.grid(row=0, column=0, sticky='nsew')
#
#         self.guessed_table: GuessedChars = GuessedChars(self, manager)
#         self.guessed_table.grid(row=2, column=0, sticky='nsew')
#
#         self.manager.load_right_frame([self.probability_table, self.guessed_table])
#
#
# # class MainFrame(ctk.CTkFrame):
# #     def __init__(self, parent, manager, **kwargs):
# #         super().__init__(parent, **kwargs)
# #
# #         self.configure(fg_color='transparent')
# #         self.manager: ExperimentManager = manager
# #
# #         self.rowconfigure(0, weight=1)
# #         self.columnconfigure(1, minsize=PADDING_32)
# #         self.columnconfigure((0, 2), weight=1)
# #
# #         self.left_frame = LeftFrame(self, self.manager)
# #         self.left_frame.grid(row=0, column=0, sticky='nsew')
# #
# #         self.right_frame = RightFrame(self, self.manager)
# #         self.right_frame.grid(row=0, column=2, sticky='nsew')
# #
# #         self.manager.load_widgets(self.left_frame.get_widgets())


class App(ctk.CTk):
    def __init__(self):

        # windows setup
        super().__init__()
        self.title(APP_TITLE)

        # from context set global localisation instance
        self.localisation = localisation

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
