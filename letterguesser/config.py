"""
Global constants.

This file defines global constants used throughout the application, including default
settings, supported languages, and alphabets.
"""
APP_TITLE: str = 'LetterGuesser'
APP_SIZE: tuple[int, int] = (1300, 740)
DEFAULT_THEME: str = 'jetbrains_dark'

DEFAULT_LANGUAGE: str = 'Ukrainian'  # Ukrainian / English
DEFAULT_LANGUAGE_CODE: str = 'uk'  # uk / en

LANGUAGES: dict[str, str] = {
    'uk': 'Ukrainian',
    'en': 'English'
}

ALPHABET_EN: str = 'abcdefghijklmnopqrstuvwxyz '
ALPHABET_UK: str = 'йцукенгшщзхїфівапролджєґячсмитьбю '
