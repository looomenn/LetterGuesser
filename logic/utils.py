""" Utility functions """

import os
import sys


def get_resource_path(relative_path):
    """
    util function for PyInstaller
    :param relative_path: relative path to the asset
    """
    try:
        base_path = sys._MEIPASS  # ignore warning,
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def load_texts(lang_code: str):
    file_path = get_resource_path(f'assets/texts/{lang_code}.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
    return text_data.replace('\n', '_').replace(' ', '_')

