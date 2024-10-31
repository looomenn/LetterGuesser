import random
import warnings

from .Event import Event
from .utils import load_texts


class ExperimentManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ExperimentManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, localisation, logger):
        # avoid re-init
        if hasattr(self, 'initialized'):
            print('Experiment Manager already initialized')
            return

        self.localisation = localisation
        self.logger = logger

        self.button_events = {
            'state_change': Event(),
            'label_change': Event(),
            'command_change': Event()
        }

        self.card_events = {
            'update': Event(),
            'reset': Event(),
            'reset_all': Event()
        }

        self.input_events = {
            'state_change': Event(),
            'reset': Event(),
            'clear': Event()
        }

        self.block_events = {
            'clear': Event(),
            'reset': Event(),
            'update': Event(),
            'rebind': Event()
        }

        self.table_events = {
            'reset': Event(),
            'init': Event(),
            'update': Event()
        }

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

    def load_widgets(self, widgets: dict) -> None:
        """
        Load widgets into ExperimentManager dynamically.
        DEPRECATED: Use event-based method (see logic/Event class) to communicate with widgets

        :param widgets: A dict. of widgets instances (example: {'probability_frame': ProbabilityTable})
        """
        warnings.warn(f'load_widgets() is deprecated and will be removed in a future version', stacklevel=2)

    def get_widget(self, widget_name: str) -> None:
        """
        Return a specific widget by its name.
        DEPRECATED: Use event-based method (see logic/Event class) to communicate with widgets

        :param widget_name: The key name of the widget.
        :return: The widget instance if found, otherwise None
        """
        warnings.warn(f'get_widget() is deprecated and will be removed in a future version', stacklevel=2)

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
        """ Starts the experiment """

        self.is_active = True
        self.attempts = 0

        # get random text part
        self.text = self.get_text(self.localisation.get_locale())

        # enabling reset button
        self.button_events['state_change'].notify(button_name='button_reset', state='enable')

        # changing start button to next experiment button
        self.button_events['label_change'].notify(button_name='button_start', label='next')
        self.button_events['state_change'].notify(button_name='button_start', state='disable')
        self.button_events['command_change'].notify(button_name='button_start', command=self.next_experiment)

        # Enabling button to select N order
        self.button_events['state_change'].notify(button_name='button_char_numbers', state='disable')

        # text shenanigans
        self.full_text = self.text
        self.visible_text = self.full_text[:self.ngram_order]  # get part of the text base on the N
        self.next_char = self.get_next_char()

        # display random(given) text in the TextBlockSegment
        self.block_events['update'].notify(block_name='random_text', text=self.visible_text)

        # input shenanigans
        self.input_events['clear'].notify()
        self.input_events['state_change'].notify(state='enable')

        # cards shenanigans
        self.card_events['update'].notify(card_name='card_attempts', value=0)
        self.card_events['update'].notify(card_name='card_experiment_number', value=self.experiment_number)

    def next_experiment(self):
        self.experiment_number += 1
        self.used_letters.clear()

        self.block_events['reset'].notify(block_name='used_chars')
        self.block_events['reset'].notify(block_name='status')

        self.card_events['reset'].notify(card_name='card_attempts')
        self.card_events['reset'].notify(card_name='card_last_char')

        self.start_experiment()

    def reset_experiment(self):

        # flag check for language toggle
        if not self.is_active:
            return

        self.is_active = False

        self.table_events['reset'].notify(table_name='prob_table')
        self.table_events['reset'].notify(table_name='attempts_table')

        alphabet = self.localisation.get_alphabet()

        self.used_letters.clear()
        self.experiment_number = 0
        self.attempt_counts = [0] * len(alphabet)

        # cards events
        self.card_events['reset_all'].notify()  # reset all cards

        # input events
        self.input_events['state_change'].notify(state='disable')  # disable input block
        self.input_events['reset'].notify()  # reset input block

        # block events
        self.block_events['reset'].notify(block_name='status')  # reset user chars block
        self.block_events['reset'].notify(block_name='used_chars')  # reset user chars block
        self.block_events['reset'].notify(block_name='random_text')  # reset random text block

        # button events
        self.button_events['state_change'].notify(button_name='button_start', state='enable')
        self.button_events['state_change'].notify(button_name='button_reset', state='disable')
        self.button_events['state_change'].notify(button_name='button_char_numbers', state='enable')

    def input_handler(self, user_input) -> str:
        """
        Main input handler
        :param user_input: User input from InputBlock
        :return: String 'correct' or 'incorrect'
        """

        alphabet = self.localisation.get_alphabet()

        user_input = user_input[0] if len(user_input) > 0 else ''
        self.input_events['clear'].notify()

        if user_input not in alphabet:
            self.block_events['rebind'].notify(block_name='status', key='invalid_char')
            return 'invalid'

        if user_input == '':
            return 'invalid'

        if user_input == ' ':
            user_input = '_'

        if user_input in self.used_letters:
            self.block_events['rebind'].notify(block_name='status', key='used_char')
            return 'invalid'

        self.used_letters.append(user_input)
        self.attempts += 1

        if len(self.used_letters) > len(alphabet):
            return 'invalid'  # should never be reached

        # updating cards
        self.card_events['update'].notify(card_name='card_attempts', value=self.attempts)
        self.card_events['update'].notify(card_name='card_last_char', value=user_input)

        # update text block
        used_letters_str = ' , '.join(self.used_letters)
        self.block_events['update'].notify(block_name='used_chars', text=used_letters_str)

        next_char = self.next_char

        if next_char and user_input == next_char:

            self.table_events['init'].notify(table_name='prob_table')

            self.attempt_counts[self.attempts - 1] += 1

            self.calc_prob()

            self.button_events['state_change'].notify(button_name='button_start', state='enable')

            self.table_events['update'].notify(
                table_name='attempts_table',
                update_method='add_char',
                char=next_char,
                attempt=self.attempts,
            )

            self.block_events['rebind'].notify(block_name='status', key='win')

            self.visible_text = self.full_text
            self.block_events['update'].notify(block_name='random_text', text=self.visible_text)

            self.input_events['clear'].notify()
            self.input_events['state_change'].notify(state='disable')

            return 'correct'
        else:
            self.block_events['rebind'].notify(block_name='status', key='incorrect')
            return 'incorrect'

    def calc_prob(self):
        """ Calculates the probability based on attempts. Inserts them into probability table"""
        for i, count in enumerate(self.attempt_counts):
            if count > 0:
                prob = count / sum(self.attempt_counts)
                self.table_events['update'].notify(
                    table_name='prob_table',
                    update_method='update_prob',
                    index=i+1,
                    new_value=round(prob, 4)
                )
