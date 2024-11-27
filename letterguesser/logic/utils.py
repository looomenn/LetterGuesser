"""
Utility functions for the LetterGuesser application.

Contains helper functions for resource loading and text file operations.
"""

import sass

import re
import sys
from pathlib import Path


def get_resource_path(relative_path: str | Path) -> Path:
    """
    Get the absolute path for a resource, compatible with PyInstaller.

    :param relative_path: Path relative to the project root.
    :return: Absolute path to the resource.
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS) / 'letterguesser'
    else:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path


def load_texts(lang_code: str) -> str:
    """
    Load text data for a specific language from a text file.

    :param lang_code: Language code, such as 'en' or 'uk'.
    :return: Text data as a single string with specific formatting.
    """
    file_path = get_resource_path(f'assets/texts/{lang_code}.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
    return text_data.replace('\n', '_').replace(' ', '_')


def compile_scss(theme_folder: Path, primitives: Path) -> dict:
    """
    Compile the SCSS for the given theme.

    :param theme_folder: Path to the theme folder.
    :param primitives: Path to the primitives.
    :return: Dictionary containing the compiled CSS variables.
    """
    theme_file = get_resource_path(theme_folder / 'theme.scss')
    primitive_file = get_resource_path(primitives)

    if not theme_file.exists():
        raise FileNotFoundError(f'SCSS file not found: {theme_file}')

    if not primitive_file.exists():
        raise FileNotFoundError(f'Primitives file not found: {primitives}')

    scss = f"""
    @import "{primitive_file.as_posix()}";
    @import "{theme_file.as_posix()}";
    """

    try:
        compiled_css = sass.compile(string=scss)
    except Exception as e:
        raise RuntimeError(f'Could not compile SCSS file: {e}')

    var_pattern = re.compile(r'--([\w-]+):\s*([^;]+);')
    variables = {}
    for match in var_pattern.finditer(compiled_css):
        key = match[1].replace('-', '_')
        value = match[2].strip()
        variables[key] = value

    return variables
