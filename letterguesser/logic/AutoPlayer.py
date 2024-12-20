"""AutoPlayer module."""

import os
import random
from datetime import datetime

from letterguesser.context import localisation
from letterguesser.logic.ExperimentManager import ExperimentManager


class AutoPlayer:
    """AutoPlayer class."""

    def __init__(self,
                 alphabet: str = 'en',
                 save_folder: str = '.',
                 guess_function: callable = None
                 ):
        """
        Initialize the AutoPlayer class.

        :param alphabet: Language code for localisation module.
        :param save_folder: Where should game sessions be saved.
        :param guess_function: Custom function for guessing letters.
        """
        self.localisation = localisation
        self.save_folder = save_folder
        self.guess_function = guess_function if guess_function else self.make_guess

        if alphabet == 'en':
            self.localisation.load_language('en')
        else:
            self.localisation.load_language('uk')

        self.alphabet = self.localisation.get_alphabet()
        self.manager = ExperimentManager(self.localisation, None)

        self.data = []
        self.text_parts = []

        self.global_used_letters = []
        self.global_probabilities = {}

        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def display_banner(self):
        """Display banner."""
        print("=" * 40)
        print("LetterGuesser v2 AutoPlayer")
        print("Developed for automated game sessions")
        print("=" * 40)
        print(f"Alphabet: {self.alphabet}")
        print(f"Save Folder: {self.save_folder}")
        print("=" * 40)

    def play_game(self, num_games: int = 10, ngram_order: int = 5):
        """
        Handle game state.

        :param num_games: Number of games to play.
        :param ngram_order: Order of the ngram to use.
        """

        self.display_banner()

        print(f'Games: {num_games:<3} Ngram Order: {ngram_order}')
        print("=" * 40)

        for _ in range(1, num_games + 1):
            print(f'[Experiment: {_}] Starting...')

            self.manager.change_ngram(str(ngram_order))
            self.manager.start_experiment()
            data = self.play_experiment()

            self.text_parts.append({
                "experiment": _,
                "text": self.manager.full_text
            })

            self.data.append(data)
            self.manager.next_experiment()

            print(f'[Experiment: {_}] Completed with {data["attempts"]} attempts.'
                  f' Success: {data["success"]}\n')
        self.save_res(num_games)

    def play_experiment(self):
        data = {
            "experiment_number": self.manager.experiment_number,
            "used_letters": [],
            "attempts": 0,
            "success": False,
            "correct_char": '',
            "text": self.manager.visible_text,
        }

        print(f'[Experiment: {data["experiment_number"]}] Starting '
              f'guessing...')

        while self.manager.visible_text != self.manager.full_text:
            guess, status = self.guess_function(data)

            print(f'[Experiment: {data["experiment_number"]}]'
                  f' Guess: {guess}({ord(guess)})')
            result = self.manager.input_handler(guess)

            if guess == ' ':
                guess = '_'

            if result == "correct":
                print(f'[Experiment: {data["experiment_number"]}]'
                      f' Correct Guess! ({guess})')
                data["success"] = True
                data["correct_char"] = guess

                guessed_char = {
                    "char": guess,
                    "attempt": self.manager.attempts,
                    "binary": ''.join(
                        '1' if i == self.manager.attempts - 1 else '0' for i in range(len(self.alphabet))
                    )
                }
                self.global_used_letters.append(guessed_char)

            if guess not in data['used_letters']:
                data["used_letters"].append(guess)

            data["attempts"] = self.manager.attempts

            self.update_probabilities()

        return data

    def update_probabilities(self):
        """Update the probabilities of the guesses."""
        total_attempts = sum(self.manager.attempt_counts)
        if total_attempts > 0:

            self.global_probabilities = {
                i + 1: round(count / total_attempts, 4)
                for i, count in enumerate(self.manager.attempt_counts)
            }
        else:
            self.global_probabilities = {i + 1: 0 for i in
                                         range(len(self.manager.attempt_counts))}

    def make_guess(self, data) -> tuple[str, str]:
        """Make a guess."""
        remaining_letters = [
            letter for letter in self.alphabet if
            letter not in self.manager.used_letters
        ]

        if not remaining_letters:
            raise ValueError("No remaining letters to guess.")
        return random.choice(remaining_letters), "default"

    def save_res(self, num_experiments):
        """Save the game results into file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.save_folder, f"guession_{timestamp}.txt")
        print(f"Saving results to file: {filename}")

        with open(filename, "w", encoding='utf-8') as file:
            file.write("Game: AutoPlay LetterGuesser\n")
            file.write(f"Number of Experiments: {num_experiments}\n")
            file.write(f"N-gram Order: {self.manager.ngram_order}\n")
            file.write("Experiment details:\n")
            for part, experiment in zip(self.text_parts, self.data):
                file.write(f"\tExperiment {experiment['experiment_number']}:\n")
                file.write(f"\t\tAttempts: {experiment['attempts']}\n")
                file.write(f"\t\tCorrect char: {experiment['correct_char']}\n")
                file.write(f"\t\tUsed Letters: {', '.join(experiment['used_letters'])}\n")
                file.write(f"\t\tText: {part['text']}\n")
                file.write("\n")

            file.write("\nGlobal Guessed Letters (Session):\n")
            for letter_info in self.global_used_letters:
                file.write(
                    f"\tChar: {letter_info['char']:<5} Attempt: {letter_info['attempt']:<5}"
                    f"Binary: {letter_info['binary']}\n"
                    )
            file.write("\nGlobal Probabilities (Session):\n")
            for attempt, prob in self.global_probabilities.items():
                file.write(f"\t{attempt}: {prob:}\n")
        print("Results saved successfully.")


if __name__ == "__main__":
    game = AutoPlayer(save_folder='test')
    game.play_game(num_games=10, ngram_order=50)
