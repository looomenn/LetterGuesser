# core
import gui
import random

# utils
from config import *
from .utils import *


class ExperimentManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ExperimentManager, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 localisation,
                 ):

        # avoid re-init
        if hasattr(self, 'initialized'):
            print('Experiment Manager already initialized')
            return

        # cached widgets / frames
        self.cards: gui.widgets.CardGroup | None = None
        self.input: gui.widgets.InputBlock | None = None
        self.status: gui.widgets.TextBlockSegment | None = None
        self.actions: gui.widgets.ButtonGroup | None = None
        self.used_chars: gui.widgets.TextBlockSegment | None = None
        self.given_text: gui.widgets.TextBlockSegment | None = None

        self.prob_table: gui.frames.ProbabilityTable | None = None
        self.attempts_table: gui.frames.AttemptsTable | None = None

        self.localisation = localisation

        self.text = ""
        self.next_char = ""
        self.full_text = ""
        self.visible_text = ""

        # some counters
        self.attempts = 0
        self.min_length = 72
        self.ngram_order = 5
        self.used_letters = []
        self.experiment_number = 1
        self.is_active = False
        self.attempt_counts = [0] * len(self.localisation.get_alphabet())

        self.widgets = {}

    def load_widgets(self, widgets: dict):
        """
        Load widgets into ExperimentManager dynamically.
        :param widgets: A dict. of widgets instances (example: {'probability_frame': ProbabilityTable})
        """
        self.widgets.update(widgets)

    def get_widget(self, widget_name: str):
        """
        Return a specific widget by its name.
        :param widget_name: The key name of the widget.
        :return: The widget instance if found, otherwise None
        """
        return self.widgets.get(widget_name)

    def change_ngram(self, value: str):
        value = value.split(' ')[0].strip()
        self.ngram_order = int(value)

    def get_text(self, lang_code: str):
        text_parts = load_texts(lang_code)

        if not text_parts or len(text_parts) < self.min_length:
            return None

        start_idx = random.randint(0, len(text_parts) - self.min_length)
        result = text_parts[start_idx:start_idx + self.min_length]
        return result

    def get_next_char(self):
        """Get the next character that should be guessed based on the visible text."""
        if len(self.visible_text) < len(self.full_text):
            return self.full_text[len(self.visible_text)]
        return None

    def start_experiment(self):

        self.is_active = True

        self.prob_table = self.get_widget('prob_table')
        self.attempts_table = self.get_widget('attempts_table')

        # widgets
        self.actions = self.get_widget('actions')
        self.input = self.get_widget('input')
        self.given_text = self.get_widget('random_text')
        self.cards = self.get_widget('cards')

        self.status = self.get_widget('status')
        self.used_chars = self.get_widget('used_chars')

        # get random text part
        self.text = self.get_text(self.localisation.get_locale())

        # enabling reset button
        reset_btn: gui.widgets.Button = self.actions.get_button('button_reset_button_label')
        reset_btn.enable()

        # start button shenanigans
        start_btn: gui.widgets.Button = self.actions.get_button('button_start')  # we need Button instance yeah
        self.localisation.bind(start_btn, 'next_button_label')  # re-bind new label (from start -> next experiment)
        start_btn.disable()  # disabled it
        start_btn.set_command(self.next_experiment)  # now button starts next experiment

        # N-gram menu shenanigans
        ngram_menu: gui.widgets.OptionMenu = self.actions.get_button('button_char_numbers')  # getting instance
        ngram_menu.disable()  # and disabling it...

        # text shenanigans
        self.full_text = self.text
        self.visible_text = self.full_text[:self.ngram_order]
        self.next_char = self.get_next_char()

        self.given_text.update_value(self.visible_text)  # show random part

        # input shenanigans
        self.input.clear()
        self.input.enable()

        self.attempts = 0
        self.cards.get_card('card_attempts').update_value('-')
        self.cards.get_card('card_experiment_number').update_value(self.experiment_number)

    def next_experiment(self):
        self.experiment_number += 1
        self.used_letters.clear()

        self.used_chars.reset()
        self.status.reset()

        self.cards.get_card('card_attempts').reset()
        self.cards.get_card('card_last_char').reset()

        self.start_experiment()

    def reset_experiment(self):

        if not self.is_active:
            return

        self.prob_table.reset_table()
        self.attempts_table.reset_table()

        alphabet = self.localisation.get_alphabet()

        start_btn = self.actions.get_button('button_start')
        reset_btn = self.actions.get_button('button_reset_button_label')
        ngram_menu = self.actions.get_button('button_char_numbers')

        self.used_letters.clear()
        self.experiment_number = 0
        self.attempt_counts = [0] * len(alphabet)
        self.cards.reset_all()

        # frames staff
        self.input.disable()
        self.input.reset()
        self.status.reset()
        self.used_chars.reset()
        self.given_text.reset()

        # buttons staff
        reset_btn.disable()
        start_btn.enable()
        start_btn.reset()
        ngram_menu.enable()

    def input_handler(self, user_input):
        alphabet = self.localisation.get_alphabet()

        start_btn = self.actions.get_button('button_start')

        user_input = user_input[0] if len(user_input) > 0 else ''
        self.input.clear()

        if user_input not in alphabet:
            self.status.rebind("invalid_char")
            return 'invalid'

        if user_input == '':
            return 'invalid'

        if user_input == ' ':
            user_input = '_'

        if user_input in self.used_letters:
            self.status.rebind("used_char")
            return 'invalid'

        self.used_letters.append(user_input)
        self.attempts += 1

        if len(self.used_letters) > len(alphabet):
            return 'invalid'  # should never be reached

        # updating cards
        self.cards.get_card('card_attempts').update_value(str(self.attempts))
        self.cards.get_card('card_last_char').update_value(user_input)

        # update text block
        used_letters_str = ' , '.join(self.used_letters)
        self.used_chars.update_value(used_letters_str)

        next_char = self.next_char
        print(next_char)

        if next_char and user_input == next_char:

            self.prob_table.init()

            print(self.attempt_counts, self.attempts)
            self.attempt_counts[self.attempts - 1] += 1

            self.calc_prob()

            start_btn.enable()

            self.attempts_table.add_char(next_char, self.attempts)

            self.status.rebind("win")
            self.visible_text = self.full_text
            self.given_text.update_value(self.visible_text)
            self.input.clear()
            self.input.disable()

            return 'correct'
        else:
            self.status.rebind("incorrect")
            return 'incorrect'

    def calc_prob(self):
        for i, count in enumerate(self.attempt_counts):
            if count > 0:
                prob = count / sum(self.attempt_counts)
                self.prob_table.update_prob(i+1, round(prob, 4))