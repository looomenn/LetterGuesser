""" Experiment Manager """

from config import *


class ExperimentManager:
    """"
    Class that manages experiments
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ExperimentManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, localisation,  main_widgets: list):

        # avoid re-init
        if hasattr(self, 'initialized'):
            print('Experiment Manager already initialized')
            return

        self.localisation = localisation
    #
    #     self.full_text = ""
    #     self.visible_text = ""
    #     self.next_char = ""
    #     self.text = ''
    #
    #     self.cards: Cards | None = None
    #     self.input_frame: InputSegment | None = None
    #     self.text_block_segment: TextBlockSegment | None = None
    #     self.used_letters_block: TextBlockSegment | None = None
    #     self.status_block: StatusFrame | None = None
    #
    #     # tables
    #     self.guessed_chars_frame: GuessedChars | None = None
    #     self.probability_frame: ProbabilityTable | None = None
    #
    #     self.actions: Actions | None = None
    #     self.start_button: Button | None = None
    #     self.ngram_order_menu: OptionMenu | None = None
    #     self.reset_button: Button | None = None
    #
    #     self.ngram_order = 5
    #     self.attempts = 0
    #     self.correct_guesses = 0
    #     self.used_letters = []
    #     self.min_length = 72
    #     self.experiment_active = False
    #     self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
    #     self.experiment_number = 1
    #     self.attempt_counts = [0] * len(self.alphabet)
    #
    # def load_right_frame(self, frames: list[ProbabilityTable | GuessedChars]):
    #     self.probability_frame = frames[0]
    #     self.guessed_chars_frame = frames[1]
    #
    # def change_ngram(self, value: int):
    #     self.ngram_order = value
    #
    # def load_actions(self, actions: Actions):
    #     self.actions = actions
    #
    # def get_text(self, lang_code):
    #     text_parts = load_texts(lang_code)
    #
    #     if not text_parts or len(text_parts) < self.min_length:
    #         return None
    #
    #     start_idx = random.randint(0, len(text_parts) - self.min_length)
    #     result = text_parts[start_idx:start_idx + self.min_length]
    #     return result
    #
    # def load_buttons(self, button_list):
    #     if not button_list:
    #         return None
    #
    #     self.start_button = button_list[0]
    #     self.ngram_order_menu = button_list[1]
    #     self.reset_button = button_list[2]
    #
    # def load_widgets(self, main_widgets: list):
    #     self.cards = main_widgets[0]
    #     self.input_frame: InputSegment = main_widgets[1].get_input_block()
    #     self.text_block_segment: TextBlockSegment = main_widgets[1].get_random_text_block()
    #     self.used_letters_block: TextBlockSegment = main_widgets[1].get_used_chars_block()
    #     self.status_block: StatusFrame = main_widgets[2]
    #
    # def start_experiment(self):
    #
    #     # get current alphabet
    #     self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
    #
    #     # changing start button label (start -> next experiment)
    #     bind_localisation(self.start_button, 'next_button_label')
    #
    #     self.ngram_order_menu.configure(state='disabled')
    #
    #     self.start_button.disable_button()
    #     self.start_button.get_button_state()
    #     self.start_button.set_command(self.next_experiment)
    #
    #     self.text = self.get_text(APP_CURRENT_LANGUAGE)
    #     self.full_text = self.text
    #     self.input_frame.clear()
    #     self.visible_text = self.full_text[:self.ngram_order]
    #
    #     self.text_block_segment.update_value(self.visible_text)
    #
    #     self.next_char = self.get_next_char()
    #     self.input_frame.enable_input()
    #     self.experiment_active = True
    #     self.reset_attempts()
    #
    #     self.cards.get_card('experiment_number').update_value(self.experiment_number)
    #
    # def next_experiment(self):
    #     self.experiment_number += 1
    #     self.used_letters.clear()
    #     self.used_letters_block.reset()
    #     self.start_experiment()
    #
    #     self.cards.get_card('last_char').update_value('-')
    #     self.status_block.get_status_block().reset()
    #
    # def reset_experiment(self):
    #
    #     # additional check for alphabet
    #     self.alphabet = get_alphabet(APP_CURRENT_LANGUAGE)
    #
    #     self.experiment_number = False
    #
    #     # resetting tables
    #     self.probability_frame.reset()
    #
    #     # resetting all
    #     self.correct_guesses = 0
    #     self.used_letters.clear()
    #     self.cards.reset_all()
    #     self.experiment_number = 0
    #     self.attempt_counts = [0] * len(self.alphabet)
    #
    #     # resetting input frame
    #     self.input_frame.disable_input()
    #
    #     # resetting text blocks
    #     self.text_block_segment.reset()
    #     self.status_block.get_status_block().reset()
    #     self.used_letters_block.reset()
    #
    #     # resetting menu and buttons
    #     self.ngram_order_menu.configure(state='normal')
    #     self.start_button.enable_button()
    #
    #     # changing start_button label back to start
    #     bind_localisation(self.start_button, 'start')
    #
    # def get_next_char(self):
    #     """Get the next character that should be guessed based on the visible text."""
    #     if len(self.visible_text) < len(self.full_text):
    #         return self.full_text[len(self.visible_text)]
    #     return None
    #
    # def input_handler(self, user_input):
    #     user_input = user_input[0] if len(user_input) > 0 else ''
    #     self.input_frame.clear()
    #
    #     if user_input not in self.alphabet:
    #         self.status_block.update_status("invalid_char")
    #         return 'invalid'
    #
    #     if user_input == '':
    #         return 'invalid'
    #
    #     if user_input == ' ':
    #         user_input = '_'
    #
    #     if user_input in self.used_letters:
    #         self.status_block.update_status("used_char")
    #         return 'invalid'
    #
    #     self.used_letters.append(user_input)
    #     self.attempts += 1
    #
    #     if len(self.used_letters) > len(self.alphabet):
    #         return 'invalid'
    #
    #     # updating cards
    #     self.cards.get_card('attempt').update_value(str(self.attempts))
    #     self.cards.get_card('last_char').update_value(user_input)
    #
    #     # update text block
    #     used_letters_str = ' , '.join(self.used_letters)
    #     self.used_letters_block.update_value(used_letters_str)
    #
    #     next_char = self.next_char
    #     print(next_char)
    #
    #     if next_char and user_input == next_char:
    #
    #         # init probability table
    #         self.probability_frame.init_table()
    #
    #         print(self.attempt_counts, self.attempts)
    #         self.attempt_counts[self.attempts - 1] += 1
    #
    #         self.calc_prob()
    #
    #         self.start_button.enable_button()
    #
    #         self.guessed_chars_frame.add_char(next_char, self.attempts)
    #
    #         self.status_block.update_status("win")
    #         self.correct_guesses += 1
    #         self.visible_text = self.full_text
    #         self.text_block_segment.update_value(self.visible_text)
    #         self.input_frame.clear()
    #         self.input_frame.disable_input()
    #
    #         return 'correct'
    #     else:
    #         self.status_block.update_status("incorrect")
    #         return 'incorrect'
    #
    # def calc_prob(self):
    #     for i, count in enumerate(self.attempt_counts):
    #         if count > 0:
    #             prob = count / sum(self.attempt_counts)
    #             self.probability_frame.update_prob(i+1, prob)
    #
    # def reset_attempts(self):
    #     self.attempts = 0
    #     self.cards.get_card('attempt').update_value('-')
    #
