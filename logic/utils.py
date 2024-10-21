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
