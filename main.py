""" some tests """
import os
import sys
import json

import customtkinter as ctk

# ctk.set_appearance_mode('light')

# Font
FONT: str = 'Inter'
TEXT_BODY_LARGE: int = 18
TEXT_BODY_MEDIUM: int = 16
TEXT_BODY_SMALL: int = 14

# Padding
PADDING_NONE: int = 0
PADDING_32: int = 32
PADDING_24: int = 24
PADDING_16: int = 16
PADDING_12: int = 12
PADDING_8: int = 8

# Widgets
BUTTON_HEIGHT: int = 32

# widget/button/default
BUTTON_DEFAULT_FG_COLOR = ("#f6f8fa", "#21252D")
BUTTON_DEFAULT_FG_COLOR_HOVER = ("#f6f8fa", "#272d35")
BUTTON_DEFAULT_TEXT = ('#24292f', '#C9D1D9')
BUTTON_DEFAULT_TEXT_DISABLED = ('#8C959f', '#8B949E')
BUTTON_DEFAULT_BORDER = ('#D0D7DE', "#30363D")

# widget/button/primary
BUTTON_PRIMARY_FG_COLOR = ("#1F883D", "#238636")
BUTTON_PRIMARY_FG_COLOR_HOVER = ("#1C8139", "#29903B")
BUTTON_PRIMARY_FG_COLOR_DISABLED = ("#95D8A6", "#46BF57")
BUTTON_PRIMARY_TEXT = ('white', 'white')
BUTTON_PRIMARY_TEXT_DISABLED = ('#eaf7ed', '#A2dfab')
BUTTON_PRIMARY_BORDER = ('#1f793a', "#38924a")

# widget/button/danger
BUTTON_DANGER_FG_COLOR = BUTTON_DEFAULT_FG_COLOR
BUTTON_DANGER_FG_COLOR_HOVER = ("#a40e26", "#b62324")
BUTTON_DANGER_FG_COLOR_DISABLED = BUTTON_DEFAULT_FG_COLOR
BUTTON_DANGER_TEXT = ('#D1242f', '#f85149')
BUTTON_DANGER_TEXT_DISABLED = ('#e38e94', '#8d3b3b')
BUTTON_DANGER_BORDER = ('#d0d7de', "#30363d")
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

    print(APP_CURRENT_LANGUAGE)


def get_alphabet(lang_code):
    return 'abcdefghijklmnopqrstuvwxyz ' if lang_code == 'en' else 'йцукенгшщзхїфівапролджєґячсмитьбю '


class Card(ctk.CTkFrame):
    def __init__(self, parent, label_text, initial_value, localisation_key, var_type='str', **kwargs):
        super().__init__(master=parent, **kwargs)

        print(localisation_key)

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

        self.attempt: Card = Card(self, 'Attempt', 'None', 'attempts', var_type='str')
        self.attempt.grid(row=0, column=2, sticky='nsew')

        self.last_char: Card = Card(self, 'Last char', 'None', 'last_char', var_type='str')
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


class InputSegment(ctk.CTkFrame):
    def __init__(self, parent, localisation_label_key, localisation_placeholder_key, is_disabled=False, **kwargs):
        super().__init__(parent, **kwargs)

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

    def get_input(self):
        return self.input_var.get()

    def update_input(self, new_value):
        self.input_var.set(new_value)

    def enable_input(self):
        self.input_field.configure(state='normal')
        self.input_field.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['text_color'])

    def disable_input(self):
        self.input_field.configure(state='disabled')
        self.input_field.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color'])


class TopFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

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


class OptionMenu(ctk.CTkOptionMenu):
    def __init__(self, parent, localisation_label_key, initial_value, values, command, **kwargs):

        self.values = values
        self.loc_key = localisation_label_key

        self.menu_var = ctk.StringVar(value=initial_value)

        super().__init__(
            parent,
            height=BUTTON_HEIGHT,
            command=command,
            variable=self.menu_var,
            values=[],
            **kwargs
        )

        bind_localisation(self, localisation_label_key, self.update_loc)

    def update_loc(self, text):
        initial_value = self.menu_var.get().split(' ')[0]
        self.menu_var.set(f'{initial_value} {text}')

        formatted_values = [f'{val} {text}' for val in self.values]
        self.configure(values=formatted_values)


class Button(ctk.CTkButton):
    def __init__(self, parent, localisation_label_key, style='default', command=None, is_disabled=False, **kwargs):

        self.style = style
        self.is_disabled = is_disabled
        self.set_button_style()

        super().__init__(
            parent,
            text='',
            height=BUTTON_HEIGHT,
            border_width=1,
            command=command,
            fg_color=self.fg_color,
            hover_color=self.hover_color,
            border_color=self.border_color,
            text_color=self.text_color,
            text_color_disabled=self.text_color_disabled,
            **kwargs
        )

        if self.is_disabled:
            self.disable_button()

        bind_localisation(self, localisation_label_key)

    def set_button_style(self):
        if self.style == 'default':
            self.fg_color = BUTTON_DEFAULT_FG_COLOR
            self.hover_color = BUTTON_DEFAULT_FG_COLOR_HOVER
            self.border_color = BUTTON_DEFAULT_BORDER
            self.text_color_disabled = BUTTON_DEFAULT_TEXT_DISABLED
            self.text_color = BUTTON_DEFAULT_TEXT
        elif self.style == 'primary':

            if self.is_disabled:
                self.fg_color = BUTTON_PRIMARY_FG_COLOR_DISABLED
            else:
                self.fg_color = BUTTON_PRIMARY_FG_COLOR

            self.text_color_disabled = BUTTON_PRIMARY_TEXT_DISABLED
            self.hover_color = BUTTON_PRIMARY_FG_COLOR_HOVER
            self.border_color = BUTTON_PRIMARY_BORDER
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

    def enable_button(self):
        self.configure(state='normal')

    def disable_button(self):
        self.configure(state='disabled')


class Actions(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color='transparent')

        self.rowconfigure(0, weight=0)
        self.columnconfigure((1, 3), minsize=PADDING_8)
        self.columnconfigure((0, 2, 4), weight=0)

        self.next_button: Button = Button(
            self,
            'next_button_label',
            command=self.next_experiment,
            style='primary',
            is_disabled=True
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
            command=self.next_experiment,
            style='danger',
            is_disabled=False
        )
        self.reset_button.grid(row=0, column=4, sticky='w')

    def next_experiment(self):
        pass

    def reset_button(self):
        pass

    def select_ngram(self, value):
        print(value)


class InputFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure((0, 2, 4, 6), weight=1)
        self.rowconfigure(1, minsize=PADDING_24)
        self.rowconfigure((3, 5), minsize=PADDING_32)

        self.columnconfigure(0, weight=1)

        self.random_text_block = TextBlockSegment(self, localisation_key="random_text_part", initial_text="random_text")
        self.random_text_block.grid(row=0, column=0, sticky='nsew', padx=PADDING_24, pady=(PADDING_24, PADDING_NONE))

        self.used_chars_block = TextBlockSegment(self, localisation_key="used_chars", initial_text="random_text")
        self.used_chars_block.grid(row=2, column=0, sticky='nsew', padx=PADDING_24)

        self.input_block = InputSegment(
            self,
            'main_input_label',
            'main_input_placeholder',
            True
        )
        self.input_block.grid(row=4, column=0, sticky='nsew', padx=PADDING_24)

        self.actions = Actions(self)
        self.actions.grid(row=6, column=0, sticky='nsew', pady=(PADDING_NONE, PADDING_24), padx=PADDING_24)

    def get_random_text_block(self):
        return self.random_text_block

    def get_used_chars_block(self):
        return self.used_chars_block

    def get_input_block(self):
        return self.input_block


class StatusFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.after(100, self.check)

    def check(self):
        print(f'status frame: {self.winfo_height()}')


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, minsize=72)
        self.rowconfigure(2, weight=1)
        self.rowconfigure((1, 3), minsize=PADDING_16)  # row gap (16px)
        self.rowconfigure(4, weight=0)

        self.columnconfigure(0, weight=1)

        self.cards = Cards(self, fg_color='transparent')
        self.cards.grid(row=0, column=0, sticky='nsew')

        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=2, column=0, sticky='nsew')

        self.status_frame = StatusFrame(self, fg_color='orange')
        self.status_frame.grid(row=4, column=0, sticky='nsew')

        self.manager = ExperimentManager(self.cards, self.input_frame, get_alphabet(APP_CURRENT_LANGUAGE))


class RightFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, minsize=PADDING_32)
        self.columnconfigure((0, 2), weight=1)

        self.left_frame = LeftFrame(self, fg_color='blue')
        self.left_frame.grid(row=0, column=0, sticky='nsew')

        self.right_frame = RightFrame(self, fg_color='purple')
        self.right_frame.grid(row=0, column=2, sticky='nsew')


class ExperimentManager:
    def __init__(self, cards: Cards, inputs: InputFrame, alphabet):
        self.cards = cards
        self.input_frame: InputSegment = inputs.get_input_block()
        self.text_block_segment: TextBlockSegment = inputs.get_random_text_block()
        self.used_letters_block: TextBlockSegment = inputs.get_used_chars_block()

        self.full_text = ""
        self.visible_text = ""

        self.ngram_order = 5
        self.attempts = 0
        self.correct_guesses = 0
        self.used_letters = set()
        self.experiment_active = False
        self.alphabet = alphabet

    def start_experiment(self, text):
        self.full_text = text
        self.visible_text = self.full_text[:self.ngram_order]
        self.text_block_segment.update_value(self.visible_text)
        self.input_frame.enable_input()
        self.experiment_active = True
        self.reset_attempts()

    def reset_experiment(self, new_text):
        self.start_experiment(new_text)
        self.correct_guesses = 0
        self.used_letters.clear()
        self.cards.reset_all()

    def input_handler(self, user_input):
        user_input = user_input[0] if len(user_input) > 0 else ''
        self.input_frame.update_input('')

        if user_input not in self.alphabet:
            return 'invalid'

        if user_input in self.used_letters:
            return 'invalid'

        self.used_letters.add(user_input)
        self.attempts += 1

        # updating cards
        self.cards.get_card('attempt').update_value(str(self.attempts))
        self.cards.get_card('last_char').update_value(user_input)

        # update text block
        self.used_letters_block.update_value(self.used_letters)

        next_char = self.full_text[len(self.visible_text)] if len(self.visible_text) < len(self.full_text) else None

        if next_char and user_input == next_char:
            self.correct_guesses += 1
            self.visible_text = self.full_text
            self.text_block_segment.update_value(self.visible_text)
            return 'correct'
        else:
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
        self.resizable(False, False)

        # layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.top_frame = TopFrame(parent=self)
        self.top_frame.grid(row=0, column=0, sticky='nsew', padx=PADDING_32, pady=PADDING_32)

        self.main_frame = MainFrame(parent=self, fg_color='red')
        self.main_frame.grid(row=1, column=0, sticky='nsew', padx=PADDING_32, pady=(PADDING_NONE, PADDING_32))

        # bind escape to close the app
        self.bind('<Escape>', lambda event: self.quit())

        # run app
        self.mainloop()


if __name__ == "__main__":
    App()
# end main
