""" some tests """
import os
import sys
import json
import random

import customtkinter as ctk

ctk.set_appearance_mode('light')

# Base colors
BASE_SURFACE_1 = ('#FFFFFF', '#141414')
BASE_BORDER = ('#E1E1E2', '#3d3d3d')
BASE_FILL_1 = ('#e1e1e2', "#333333")
TEXT_PRIMARY = ('#1a1a1a', '#FFFFFF')
TEXT_SECONDARY = ('#5f5f5f', '#B8B8B8')

# Font
FONT: str = 'Calibri'
TEXT_BODY_LARGE: int = 18
TEXT_BODY_MEDIUM: int = 16
TEXT_BODY_SMALL: int = 14

# Line Height
TEXT_BODY_SMALL_HEIGHT: int = int(TEXT_BODY_SMALL // 1.4)
TEXT_BODY_MEDIUM_HEIGHT: int = int(TEXT_BODY_MEDIUM // 1.4)
TEXT_BODY_LARGE_HEIGHT: int = int(TEXT_BODY_LARGE // 1.4)

# Padding
PADDING_NONE: int = 0
PADDING_32: int = 32
PADDING_24: int = 24
PADDING_16: int = 16
PADDING_12: int = 12
PADDING_8: int = 8

# Widgets
BUTTON_HEIGHT: int = 32
BUTTON_WIDTH: int = 200

# widget/button/default
BUTTON_DEFAULT_FG_COLOR = ("#FCFCFC", "#1F2023")
BUTTON_DEFAULT_TEXT = ('#1A1A1A', '#FFFFFF')
BUTTON_DEFAULT_BORDER = ('#E1E1E2', "#3D3D3D")

BUTTON_DEFAULT_FG_COLOR_HOVER = ("#E1E1E2", "#272d35")
BUTTON_DEFAULT_BORDER_HOVER = BUTTON_DEFAULT_BORDER

BUTTON_DEFAULT_FG_COLOR_DISABLED = ("#FCFCFC", "#333333")
BUTTON_DEFAULT_TEXT_DISABLED = ('#CDCDCE', '#585858')
BUTTON_DEFAULT_BORDER_DISABLED = ('#D0D7DE', "#30363D")

# widget/button/primary
BUTTON_PRIMARY_FG_COLOR = ("#2463EB", "#50A1FF")
BUTTON_PRIMARY_TEXT = ('#FFFFFF', '#141414')
BUTTON_PRIMARY_BORDER = ('#235ad1', "#65acff")

BUTTON_PRIMARY_FG_COLOR_HOVER = ("#357AE9", "#2C87F6")
BUTTON_PRIMARY_BORDER_HOVERED = ('#2463EB', "#52A3FF")

BUTTON_PRIMARY_FG_COLOR_DISABLED = ("#F4F4F5", "#333333")
BUTTON_PRIMARY_TEXT_DISABLED = ('#CDCDCE', '#585858')
BUTTON_PRIMARY_BORDER_DISABLED = BUTTON_PRIMARY_FG_COLOR_DISABLED

# widget/button/danger
BUTTON_DANGER_FG_COLOR = ('#DC2828', '#FF9494')
BUTTON_DANGER_TEXT = ('#FFFFFF', '#141414')
BUTTON_DANGER_BORDER = BUTTON_DANGER_FG_COLOR

BUTTON_DANGER_FG_COLOR_HOVER = ("#FF6565", "#FA4D4D")
BUTTON_DANGER_BORDER_HOVER = BUTTON_DEFAULT_FG_COLOR_HOVER

BUTTON_DANGER_FG_COLOR_DISABLED = ("#F4F4F5", "#333333")
BUTTON_DANGER_TEXT_DISABLED = ('#e38e94', '#8d3b3b')
BUTTON_DANGER_BORDER_DISABLED = BUTTON_DEFAULT_FG_COLOR

# App Settings
APP_TITLE: str = 'LetterGuesser'
APP_SIZE: tuple = (1200, 840)
APP_LANGUAGE_DATA: dict = {}  # where language data stored when load_language() called
APP_WIDGETS_BINDINGS: dict = {}  # where the binding of widget label and localisation key is stored

# localisation staff
APP_DEFAULT_LANGUAGE: str = 'Ukrainian'  # Ukrainian / English
APP_DEFAULT_LANGUAGE_CODE: str = 'uk'  # uk / en
APP_CURRENT_LANGUAGE: str = ''


#  helper func for pyinstaller
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def load_language(lang_code) -> None:
    global APP_LANGUAGE_DATA
    global APP_CURRENT_LANGUAGE

    APP_CURRENT_LANGUAGE = lang_code

    lang_file_path = get_resource_path(f'lang/{lang_code}.json')
    with open(lang_file_path, 'r', encoding='utf-8') as file:
        APP_LANGUAGE_DATA = json.load(file)

    localisation_update()


def load_texts(lang_code: str):
    file_path = get_resource_path(f'texts/{lang_code}.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
    return text_data.replace('\n', '_').replace(' ', '_')


def bind_localisation(widget, translation_key, update_method=None) -> None:
    APP_WIDGETS_BINDINGS[widget] = (translation_key, update_method)
    update_widget_localisation(widget)


def update_widget_localisation(widget) -> None:
    key, method = APP_WIDGETS_BINDINGS[widget]
    translated_text = APP_LANGUAGE_DATA.get(key, f'Missing: {key}')
    if method:
        method(translated_text)
    else:
        widget.configure(text=translated_text)


def localisation_update():
    for widget in APP_WIDGETS_BINDINGS:
        update_widget_localisation(widget)


def get_alphabet(lang_code):
    return 'abcdefghijklmnopqrstuvwxyz ' if lang_code == 'en' else 'йцукенгшщзхїфівапролджєґячсмитьбю '


class Card(ctk.CTkFrame):
    def __init__(self, parent, label_text, initial_value, localisation_key, var_type='str', **kwargs):
        super().__init__(master=parent, **kwargs)

        self.propagate(False)
        self.configure(width=200, height=72)
        self.columnconfigure(0, weight=0)  # for rows to work properly
        self.rowconfigure((0, 1), weight=1)

        # vars for text sizes (font + line height depends on them)
        label_text_size = TEXT_BODY_SMALL
        value_label_text_size = TEXT_BODY_MEDIUM

        # variable type check
        if var_type == 'str':
            self.var_value = ctk.StringVar(value=initial_value)
        elif var_type == 'int':
            self.var_value = ctk.IntVar(value=initial_value)
        else:
            raise ValueError('Incorrect variable type')  # I have no clue how this will work in exe format

        self.value_label = ctk.CTkLabel(
            self,
            textvariable=self.var_value,
            height=int(value_label_text_size * 1.4),  # to make adequate line height
            font=ctk.CTkFont(
                family=FONT,
                size=value_label_text_size,
                weight='bold'  # sadly, there is no 'semibold' keyword
            )
        )

        self.label = ctk.CTkLabel(
            self,
            text=label_text,
            height=int(label_text_size * 1.4),  # to make adequate line height
            font=ctk.CTkFont(
                family=FONT,
                size=label_text_size
            )
        )

        bind_localisation(self.label, localisation_key)

        # placing value label into the card
        self.value_label.grid(
            row=0,
            column=0,
            padx=PADDING_12,  # padding-right:12px, padding-left:12px
            pady=(PADDING_12, PADDING_8),  # padding-top:12px, padding-bottom:8px
            sticky='w'
        )

        # placing label into the card
        self.label.grid(
            row=1,
            column=0,
            padx=PADDING_12,  # padding-right:12px, padding-left:12px
            pady=(PADDING_NONE, PADDING_12),  # padding-top:0px (cause value_label already has it), padding-bottom:12px
            sticky='w'
        )

    def update_value(self, new_value):
        self.var_value.set(new_value)


class Cards(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(master=parent, **kwargs)

        self.columnconfigure((0, 2, 4), weight=1, minsize=180)  # actual columns for the cards
        self.columnconfigure((1, 3), minsize=16)  # column-gap between cards (16px)
        self.rowconfigure(0, weight=1)  # for grid to work correctly

        self.experiment_number: Card = Card(self, 'NaN', 0, 'experiment_number', var_type='int')
        self.experiment_number.grid(row=0, column=0, sticky='nsew')

        self.attempt: Card = Card(self, 'Attempt', '-', 'attempts', var_type='str')
        self.attempt.grid(row=0, column=2, sticky='nsew')

        self.last_char: Card = Card(self, 'Last char', '-', 'last_char', var_type='str')
        self.last_char.grid(row=0, column=4, sticky='nsew')

        self.cards = {
            'experiment_number': self.experiment_number,
            'attempt': self.attempt,
            'last_char': self.last_char
        }

    def get_card(self, key):
        return self.cards.get(key, None)

    def reset_all(self):
        self.experiment_number.update_value(0)
        self.attempt.update_value('-')
        self.last_char.update_value('-')


class TextBlockSegment(ctk.CTkFrame):
    def __init__(self, parent, localisation_key, initial_text, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color='transparent')

        self.rowconfigure(1, minsize=PADDING_12)
        self.columnconfigure(0, weight=1)

        label_text_size = TEXT_BODY_SMALL

        self.label = ctk.CTkLabel(
            self,
            height=int(label_text_size * 1.4),
            font=ctk.CTkFont(
                family=FONT,
                size=label_text_size
            )
        )
        bind_localisation(self.label, localisation_key)
        self.label.grid(row=0, column=0, sticky='w')

        self.text_var = ctk.StringVar(value=initial_text)
        self.text_block = ctk.CTkEntry(
            self,
            textvariable=self.text_var,
            state='disabled',
            height=40,
            border_width=0
        )
        bind_localisation(self.text_block, 'no_input', self.update_value)

        self.text_block.grid(row=2, column=0, sticky='ew')
        self.text_block.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color'][0])

    def update_value(self, new_value):
        self.text_var.set(new_value)

    def reset(self):
        bind_localisation(self.text_block, 'no_input', self.update_value)


class InputSegment(ctk.CTkFrame):
    def __init__(self, parent, manager, localisation_label_key, localisation_placeholder_key, is_disabled=False, **kwargs):
        super().__init__(parent, **kwargs)

        self.manager: ExperimentManager = manager

        # remove frame bg
        self.configure(fg_color='transparent')

        # layout
        self.rowconfigure(1, minsize=PADDING_12)
        self.columnconfigure(0, weight=1)

        # font staff
        label_text_size = TEXT_BODY_SMALL

        # label for the input
        self.label = ctk.CTkLabel(
            self,
            height=int(label_text_size * 1.4),
            font=ctk.CTkFont(
                family=FONT,
                size=label_text_size
            )
        )

        # binding label localisation to the given key
        bind_localisation(self.label, localisation_label_key)

        # placing label into the layout(frame)
        self.label.grid(row=0, column=0, sticky='w')

        # input field
        self.input_var = ctk.StringVar(value='')  # StringVar to hold input value
        self.input_field = ctk.CTkEntry(
            self,
            textvariable=self.input_var,
            height=40,
            font=ctk.CTkFont(
                family=FONT,
                size=label_text_size
            ),
        )

        # bind placeholder
        bind_localisation(self.input_field, localisation_placeholder_key, self.update_input)

        # place input field into the layout
        self.input_field.grid(row=2, column=0, sticky='ew')

        if is_disabled:
            self.disable_input()

        self.input_field.bind('<Return>', self.input_handler)

    def input_handler(self, event):
        self.manager.input_handler(self.get_input())

    def get_input(self):
        return self.input_var.get()

    def clear(self):
        self.input_var.set('')

    def update_input(self, new_value):
        self.input_var.set(new_value)

    def enable_input(self):
        self.input_field.configure(state='normal')
        self.input_field.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['text_color'])

    def disable_input(self):
        self.input_field.configure(state='disabled')
        self.input_field.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color'])


class TopFrame(ctk.CTkFrame):
    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, **kwargs)

        self.manager: ExperimentManager = manager

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.app_name_label = ctk.CTkLabel(self, text=APP_TITLE, font=ctk.CTkFont(family=FONT, size=TEXT_BODY_LARGE))
        self.app_name_label.grid(row=0, column=0, padx=PADDING_12, pady=PADDING_12, sticky='w')

        self.language_selector = ctk.CTkSegmentedButton(self, values=['Ukrainian', 'English'],
                                                        command=self.change_language)
        self.language_selector.set(APP_DEFAULT_LANGUAGE)
        self.language_selector.grid(row=0, column=1, padx=(PADDING_NONE, PADDING_12))

    def change_language(self, langauge):
        lang_code = "en" if langauge == 'English' else "uk"
        load_language(lang_code)
        self.manager.reset_experiment()


class OptionMenu(ctk.CTkOptionMenu):
    def __init__(self, parent, localisation_label_key, initial_value, values, command, **kwargs):
        self.values = values
        self.loc_key = localisation_label_key

        self.menu_var = ctk.StringVar(value=initial_value)

        super().__init__(
            parent,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
            command=command,
            state='normal',
            variable=self.menu_var,
            fg_color=BASE_SURFACE_1,
            button_color=BASE_SURFACE_1,
            text_color=TEXT_SECONDARY,
            button_hover_color=BASE_FILL_1,
            values=[],
            **kwargs
        )

        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)
        bind_localisation(self, localisation_label_key, self.update_loc)

    def on_hover(self, event):
        if self.cget('state') == 'normal':
            self.configure(fg_color=BASE_FILL_1, text_color=TEXT_PRIMARY, button_hover_color=BASE_FILL_1)

    def on_leave(self, event):
        if self.cget('state') == 'normal':
            self.configure(fg_color=BASE_SURFACE_1, text_color=TEXT_SECONDARY)

    def update_loc(self, text):
        initial_value = self.menu_var.get().split(' ')[0]
        self.menu_var.set(f'{initial_value} {text}')

        formatted_values = [f'{val} {text}' for val in self.values]
        self.configure(values=formatted_values)


class Button(ctk.CTkButton):
    def __init__(self, parent, localisation_label_key, style='default', command=None, is_disabled=False, **kwargs):

        self.style = style
        self.is_disabled = is_disabled

        # styles
        self.fg_color: str | None = None
        self.text_color: str | None = None
        self.border_color: str | None = None
        self.hover_color: str | None = None
        self.text_color_disabled: str | None = None

        super().__init__(
            parent,
            text='',
            height=BUTTON_HEIGHT,
            border_width=1,
            command=command,
            **kwargs
        )

        self.set_button_style()

        if self.is_disabled:
            self.disable_button()

        bind_localisation(self, localisation_label_key)

    def set_command(self, function):
        self.configure(command=function)

    def set_button_style(self):
        if self.style == 'default':
            if self.is_disabled:
                self.fg_color = BUTTON_DEFAULT_FG_COLOR_DISABLED
                self.border_color = BUTTON_DEFAULT_BORDER_DISABLED
            else:
                self.fg_color = BUTTON_DEFAULT_FG_COLOR
                self.border_color = BUTTON_DEFAULT_BORDER

            self.text_color_disabled = BUTTON_DEFAULT_TEXT_DISABLED
            self.hover_color = BUTTON_DEFAULT_FG_COLOR_HOVER
            self.text_color = BUTTON_DEFAULT_TEXT

        elif self.style == 'primary':
            if self.is_disabled:
                self.fg_color = BUTTON_PRIMARY_FG_COLOR_DISABLED
                self.border_color = BUTTON_PRIMARY_BORDER_DISABLED
            else:
                self.fg_color = BUTTON_PRIMARY_FG_COLOR
                self.border_color = BUTTON_PRIMARY_BORDER

            self.text_color_disabled = BUTTON_PRIMARY_TEXT_DISABLED
            self.hover_color = BUTTON_PRIMARY_FG_COLOR_HOVER
            self.text_color = BUTTON_PRIMARY_TEXT

        elif self.style == 'danger':

            if self.is_disabled:
                self.fg_color = BUTTON_DANGER_FG_COLOR_DISABLED
                self.border_color = BUTTON_DANGER_BORDER_DISABLED
            else:
                self.fg_color = BUTTON_DANGER_FG_COLOR
                self.border_color = BUTTON_DANGER_BORDER

            self.text_color_disabled = BUTTON_DANGER_TEXT_DISABLED
            self.hover_color = BUTTON_DANGER_FG_COLOR_HOVER
            self.text_color = BUTTON_DANGER_TEXT

        self.configure(
            fg_color=self.fg_color,
            hover_color=self.hover_color,
            border_color=self.border_color,
            text_color=self.text_color,
            text_color_disabled=self.text_color_disabled
        )

    def get_button_state(self):
        return self.cget('state')

    def enable_button(self):
        self.is_disabled = False
        self.configure(state='normal')
        self.set_button_style()

    def disable_button(self):
        self.is_disabled = True
        self.configure(state='disabled')
        self.set_button_style()


class Actions(ctk.CTkFrame):
    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, **kwargs)

        # init manager from the Input Frame
        self.manager: ExperimentManager = manager

        self.configure(fg_color='transparent')

        self.rowconfigure(0, weight=0)
        self.columnconfigure((1, 3), minsize=PADDING_8)
        self.columnconfigure((0, 2, 4), weight=0)

        self.next_button: Button = Button(
            self,
            'start',
            command=self.start_experiment,
            style='primary'
        )
        self.next_button.grid(row=0, column=0, sticky='w')

        self.ngram_selector: OptionMenu = OptionMenu(
            self,
            'char_numbers',
            command=self.select_ngram,
            initial_value=5,
            values=[i for i in range(5, 55, 5)]
        )
        self.ngram_selector.grid(row=0, column=2, sticky='')

        self.reset_button: Button = Button(
            self,
            'reset_button_label',
            command=self.reset_button,
            style='danger',
            is_disabled=False
        )
        self.reset_button.grid(row=0, column=4, sticky='w')

        # sending buttons to the manager
        self.manager.load_buttons([self.next_button, self.ngram_selector, self.reset_button])
        self.manager.load_actions(self)

    def start_experiment(self):
        self.ngram_selector.configure(hover=False, state='disabled')
        self.manager.start_experiment()

    def reset_button(self):
        self.ngram_selector.configure(hover=True, state='normal')
        self.manager.reset_experiment()

    def select_ngram(self, value):
        self.manager.change_ngram(int(value.split(' ')[0]))


class InputFrame(ctk.CTkFrame):
    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, **kwargs)

        # init manager (from the LeftFrame)
        self.manager: ExperimentManager = manager

        # layout
        self.rowconfigure((0, 2, 4, 6), weight=1)
        self.rowconfigure(1, minsize=PADDING_24)
        self.rowconfigure((3, 5), minsize=PADDING_32)
        self.columnconfigure(0, weight=1)

        # where the random part from the text will be displayed
        self.random_text_block = TextBlockSegment(self, localisation_key="random_text_part", initial_text="random_text")
        self.random_text_block.grid(row=0, column=0, sticky='nsew', padx=PADDING_24, pady=(PADDING_24, PADDING_NONE))

        # block for the used chars
        self.used_chars_block = TextBlockSegment(self, localisation_key="used_chars", initial_text="random_text")
        self.used_chars_block.grid(row=2, column=0, sticky='nsew', padx=PADDING_24)

        # main input
        self.input_block = InputSegment(
            self,
            manager,
            'main_input_label',
            'main_input_placeholder',
            True
        )
        self.input_block.grid(row=4, column=0, sticky='nsew', padx=PADDING_24)

        # buttons
        self.actions = Actions(self, self.manager)
        self.actions.grid(row=6, column=0, sticky='nsew', pady=(PADDING_NONE, PADDING_24), padx=PADDING_24)

    def get_random_text_block(self):
        """ util function to access specific block from the class """
        return self.random_text_block

    def get_used_chars_block(self):
        """ util function to access specific block from the class """
        return self.used_chars_block

    def get_input_block(self):
        return self.input_block


class StatusFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.status = TextBlockSegment(
            self,
            'status_label',
            'random_text'
        )
        self.status.grid(row=0, column=0, sticky='nsew', padx=PADDING_24, pady=PADDING_24)

    def get_status_block(self):
        return self.status

    def update_status(self, key):
        bind_localisation(self.status.text_block, key, self.status.update_value)


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, **kwargs)

        # init experiment manager
        self.manager: ExperimentManager = manager

        # remove gray background from the frame
        self.configure(fg_color='transparent')

        # layout settings
        self.rowconfigure(0, minsize=100)  # cards
        self.rowconfigure(2, weight=1)  # input frame
        self.rowconfigure((1, 3), minsize=PADDING_16)  # row gap (16px)
        self.rowconfigure(4, weight=0)  # status frame
        self.columnconfigure(0, weight=1)  # for grid to work correctly

        # init cards
        self.cards = Cards(self, fg_color='transparent')
        self.cards.grid(row=0, column=0, sticky='nsew')

        # init input frame (core of the program)
        self.input_frame = InputFrame(self, self.manager)
        self.input_frame.grid(row=2, column=0, sticky='nsew')

        # init status frame
        self.status_frame = StatusFrame(self)
        self.status_frame.grid(row=4, column=0, sticky='nsew')

    def get_widgets(self):
        """ returns list of the main widgets in the left frame """
        return [self.cards, self.input_frame, self.status_frame]


class ProbabilityTable(ctk.CTkScrollableFrame):
    def __init__(self,  parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
        self.alphabet_len = len(self.alphabet)

        self.attempt_numbers = list(range(1, self.alphabet_len + 1))
        self.attempts_data = [0] * self.alphabet_len
        self.attempt_labels: list = []
        self.labels: list = []

        self.is_data: bool = True  # flag to show/hide absent message


        self.placeholder = ctk.CTkLabel(
            self,
            text='text-placeholder',
            height=TEXT_BODY_MEDIUM_HEIGHT,
            font=ctk.CTkFont(
                family=FONT,
                size=TEXT_BODY_MEDIUM
            ),
            text_color=TEXT_SECONDARY
        )
        bind_localisation(self.placeholder, 'table_placeholder')
        self.placeholder.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.init_widgets()

        if self.is_data:
            self.show_table()
        else:
            self.show_placeholder()

    def init_widgets(self):

        # frame title
        self.title_label = ctk.CTkLabel(
            self,
            text='',
            anchor='w',
            height=TEXT_BODY_MEDIUM_HEIGHT,
            font=ctk.CTkFont(
                family=FONT,
                size=TEXT_BODY_MEDIUM,
                weight='bold'
            )
        )
        bind_localisation(self.title_label, 'probability')
        self.title_label.grid(
            row=0, column=0, columnspan=2, sticky='ew',
            padx=PADDING_12, pady=(PADDING_12, PADDING_16)
        )

        # header for attempts
        self.header_attempt = ctk.CTkLabel(
            self,
            text='',
            height=TEXT_BODY_SMALL_HEIGHT,
            font=ctk.CTkFont(
                family=FONT,
                size=TEXT_BODY_SMALL
            )
        )

        bind_localisation(self.header_attempt, 'attempt')
        self.header_attempt.grid(
            row=1, column=0, sticky='ew',
            padx=PADDING_12, pady=PADDING_8
        )

        # header for probability
        self.header_probability = ctk.CTkLabel(
            self,
            text='',
            height=TEXT_BODY_SMALL_HEIGHT,
            font=ctk.CTkFont(
                family=FONT,
                size=TEXT_BODY_SMALL
            )
        )

        bind_localisation(self.header_probability, 'probability')
        self.header_probability.grid(
            row=1, column=1, sticky='w',
            padx=(PADDING_NONE, PADDING_8), pady=PADDING_8
        )

        # placing aka table items
        for i in range(self.alphabet_len):
            attempt_label = ctk.CTkLabel(
                self,
                text=str(i + 1),
                anchor='w'
            )
            attempt_label.grid(
                row=i+2, column=0, sticky='w',
                padx=PADDING_12
            )

            probability_label = ctk.CTkLabel(
                self,
                text=str(self.attempts_data[i]),
                anchor='w'
            )
            probability_label.grid(row=i + 2, column=1, sticky='w')

            self.attempt_labels.append(attempt_label)
            self.labels.append(probability_label)

    def show_placeholder(self):
        # showing placeholder
        self.placeholder.grid()

        # removing table data
        self.title_label.grid_remove()
        self.header_attempt.grid_remove()
        self.header_probability.grid_remove()

        for label in self.labels:
            label.grid_remove()

        for label in self.attempt_labels:
            label.grid_remove()

    def show_table(self):
        # show table
        self.placeholder.grid_remove()

        self.title_label.grid()
        self.header_attempt.grid()
        self.header_probability.grid()

        for row_index, label in enumerate(self.attempt_labels):
            label.grid(row=row_index + 2, column=0, sticky='w')

        for row_index, label in enumerate(self.labels):
            label.grid(row=row_index + 2, column=1, sticky='w')

    def update_probability(self, new_data):
        self.show_table()
        for i in range(new_data):
            self.attempts_data[i] = new_data[i]
            self.labels[i].configure(text=str(new_data[i]))


class RightFrame(ctk.CTkFrame):
    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color='transparent')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, minsize=PADDING_32)
        self.columnconfigure((0, 2), weight=0)

        self.probability_table: ProbabilityTable = ProbabilityTable(self)
        self.probability_table.grid(row=0, column=0, sticky='nsew')


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, manager, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color='transparent')
        self.manager: ExperimentManager = manager

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, minsize=PADDING_32)
        self.columnconfigure((0, 2), weight=1)

        self.left_frame = LeftFrame(self, self.manager)
        self.left_frame.grid(row=0, column=0, sticky='nsew')

        self.right_frame = RightFrame(self, self.manager)
        self.right_frame.grid(row=0, column=2, sticky='nsew')

        self.manager.load_widgets(self.left_frame.get_widgets())


class ExperimentManager:
    def __init__(self, main_widgets: list):

        self.full_text = ""
        self.visible_text = ""
        self.next_char = ""
        self.text = ''

        self.cards: Cards | None = None
        self.input_frame: InputSegment | None = None
        self.text_block_segment: TextBlockSegment | None = None
        self.used_letters_block: TextBlockSegment | None = None
        self.status_block: StatusFrame | None = None

        self.actions: Actions | None = None
        self.start_button: Button | None = None
        self.ngram_order_menu: OptionMenu | None = None
        self.reset_button: Button | None = None

        self.ngram_order = 5
        self.attempts = 0
        self.correct_guesses = 0
        self.used_letters = []
        self.min_length = 72
        self.experiment_active = False
        self.alphabet = ''
        self.experiment_number = 1

    def change_ngram(self, value: int):
        self.ngram_order = value

    def load_actions(self, actions: Actions):
        self.actions = actions

    def get_text(self, lang_code):
        text_parts = load_texts(lang_code)

        if not text_parts or len(text_parts) < self.min_length:
            return None

        start_idx = random.randint(0, len(text_parts) - self.min_length)
        result = text_parts[start_idx:start_idx + self.min_length]
        return result

    def load_buttons(self, button_list):
        if not button_list:
            return None

        self.start_button = button_list[0]
        self.ngram_order_menu = button_list[1]
        self.reset_button = button_list[2]

    def load_widgets(self, main_widgets: list):
        self.cards = main_widgets[0]
        self.input_frame: InputSegment = main_widgets[1].get_input_block()
        self.text_block_segment: TextBlockSegment = main_widgets[1].get_random_text_block()
        self.used_letters_block: TextBlockSegment = main_widgets[1].get_used_chars_block()
        self.status_block: StatusFrame = main_widgets[2]

    def start_experiment(self):

        # changing start button label (start -> next experiment)
        bind_localisation(self.start_button, 'next_button_label')

        self.ngram_order_menu.configure(state='disabled')

        self.start_button.disable_button()
        self.start_button.get_button_state()
        self.start_button.set_command(self.next_experiment)

        self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
        self.text = self.get_text(APP_CURRENT_LANGUAGE)
        self.full_text = self.text
        self.input_frame.clear()
        self.visible_text = self.full_text[:self.ngram_order]

        self.text_block_segment.update_value(self.visible_text)

        self.next_char = self.get_next_char()
        self.input_frame.enable_input()
        self.experiment_active = True
        self.reset_attempts()

        self.cards.get_card('experiment_number').update_value(self.experiment_number)

    def next_experiment(self):
        self.experiment_number += 1
        self.used_letters.clear()
        self.used_letters_block.reset()
        self.start_experiment()

        self.cards.get_card('last_char').update_value('-')
        self.status_block.get_status_block().reset()

    def reset_experiment(self):

        self.experiment_number = False

        # resetting all
        self.correct_guesses = 0
        self.used_letters.clear()
        self.cards.reset_all()
        self.experiment_number = 0

        # resetting input frame
        self.input_frame.disable_input()

        # resetting text blokcs
        self.text_block_segment.reset()
        self.status_block.get_status_block().reset()
        self.used_letters_block.reset()

        # resetting menu and buttons
        self.ngram_order_menu.configure(state='normal')
        self.start_button.enable_button()

        # changing start_button label back to start
        bind_localisation(self.start_button, 'start')

    def get_next_char(self):
        """Get the next character that should be guessed based on the visible text."""
        if len(self.visible_text) < len(self.full_text):
            return self.full_text[len(self.visible_text)]
        return None

    def input_handler(self, user_input):
        user_input = user_input[0] if len(user_input) > 0 else ''
        self.input_frame.clear()

        if user_input not in self.alphabet:
            self.status_block.update_status("invalid_char")
            return 'invalid'

        if user_input == '':
            return 'invalid'

        if user_input == ' ':
            user_input = '_'

        if user_input in self.used_letters:
            self.status_block.update_status("used_char")
            return 'invalid'

        self.used_letters.append(user_input)
        self.attempts += 1

        if len(self.used_letters) > len(self.alphabet):
            return 'invalid'

        # updating cards
        self.cards.get_card('attempt').update_value(str(self.attempts))
        self.cards.get_card('last_char').update_value(user_input)

        # update text block
        used_letters_str = ' , '.join(self.used_letters)
        self.used_letters_block.update_value(used_letters_str)

        next_char = self.next_char
        print(next_char)

        if next_char and user_input == next_char:

            self.start_button.enable_button()

            self.status_block.update_status("win")
            self.correct_guesses += 1
            self.visible_text = self.full_text
            self.text_block_segment.update_value(self.visible_text)
            self.input_frame.clear()
            self.input_frame.disable_input()

            return 'correct'
        else:
            self.status_block.update_status("incorrect")
            return 'incorrect'

    def reset_attempts(self):
        self.attempts = 0
        self.cards.get_card('attempt').update_value('-')


class App(ctk.CTk):
    def __init__(self):
        # windows setup
        super().__init__()
        self.title(APP_TITLE)

        load_language(APP_DEFAULT_LANGUAGE_CODE)  # by default loading ENG localisation

        self.attributes('-topmost', True)  # for easier testing, can be removed if needed

        # offsets to run app in the center of the screen 
        display = (self.winfo_screenwidth(), self.winfo_screenheight())  # host display width x height
        left = int(display[0] / 2 - APP_SIZE[0] / 2)
        top = int(display[1] / 2 - APP_SIZE[1] / 2)
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{left}+{top}')
        self.minsize(APP_SIZE[0], APP_SIZE[1])  # precaution, if resizable(false, false) fails
        self.maxsize(APP_SIZE[0], APP_SIZE[1])  # precaution, if resizable(false, false) fails
        self.resizable(False, False)

        # layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # manager
        self.manager: ExperimentManager = ExperimentManager([])

        self.top_frame = TopFrame(self, self.manager)
        self.top_frame.grid(row=0, column=0, sticky='nsew', padx=PADDING_32, pady=PADDING_32)

        self.main_frame = MainFrame(self, self.manager)
        self.main_frame.grid(row=1, column=0, sticky='nsew', padx=PADDING_32, pady=(PADDING_NONE, PADDING_32))

        # bind escape to close the app
        self.bind('<Escape>', lambda event: self.quit())

        # run app
        self.mainloop()


if __name__ == "__main__":
    App()
# end main
