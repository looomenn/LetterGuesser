from pathlib import Path

from unittest.mock import MagicMock, patch

import polib
import pytest

from letterguesser.logic.Localisation import Localisation


@pytest.fixture
def localisation():
    """Fixture to create a Localisation instance with mock paths."""
    with patch('letterguesser.logic.utils.get_resource_path', return_value='/mock/path'):
        loc = Localisation()
        loc.load_language = MagicMock(wraps=loc.load_language)  # Wrap to track internal calls
        return loc


def test_singleton_pattern(localisation):
    """Test Localisation follows the singleton pattern."""
    another_instance = Localisation()
    assert another_instance is localisation


def test_load_language(localisation):
    """Test language loading with a mock translation."""
    with patch('gettext.translation') as mock_translation:
        mock_translation.return_value = MagicMock()  # Mock the translation object
        localisation.load_language('en')

        # Confirm `gettext.translation` was called with the expected parameters
        mock_translation.assert_called_once_with(
            localisation.domain,
            localedir=localisation.locale_dir,
            languages=['en'],
            fallback=True
        )


def test_translate(localisation):
    """Test translation retrieval with a mock translation."""
    mock_translation = MagicMock()
    mock_translation.gettext.return_value = "Hello"
    localisation.current_translation = mock_translation
    assert localisation.translate("greet") == "Hello"


def test_widget_binding(localisation):
    """Test binding widgets to a translation key."""
    localisation.current_translation = MagicMock()
    localisation.current_translation.gettext.return_value = "Hello"  # Mock gettext return

    widget = MagicMock()
    localisation.bind(widget, 'greet')

    # Confirm `_update_method` exists and has the expected effect
    assert widget._update_method
    widget._update_method()  # Manually trigger the update to verify behavior

    # Ensure configure was called exactly twice
    assert widget.configure.call_count == 2
    widget.configure.assert_any_call(text="Hello")


def test_update_all_widgets(localisation):
    """Test updating all bound widgets."""
    widget1 = MagicMock()
    widget2 = MagicMock()
    localisation.widgets = [widget1, widget2]
    localisation.update_all_widgets()
    widget1._update_method.assert_called_once()
    widget2._update_method.assert_called_once()


BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE_DIR / "letterguesser" / "assets" / "locales"
SUPPORTED_LANGUAGES = ["en", "uk"]


def load_po_file(lang):
    """Helper function to load a .po file for a specific language."""
    po_file_path = LOCALE_DIR / lang / "LC_MESSAGES" / "messages.po"
    assert po_file_path.is_file(), f"{po_file_path} does not exist."
    return polib.pofile(po_file_path)


@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_po_files_msgid_consistency(lang):
    """Test that all .po files have consistent msgid entries across languages."""
    # Load the .po file for each language and collect all msgid entries
    reference_entries = None
    discrepancies = {}

    for lang in SUPPORTED_LANGUAGES:
        po_file = load_po_file(lang)
        msgid_set = {entry.msgid for entry in po_file}

        # Set the reference entries to the first language processed
        if reference_entries is None:
            reference_entries = msgid_set
        else:
            # Compare current language msgid set with reference
            if msgid_set != reference_entries:
                discrepancies[lang] = msgid_set.symmetric_difference(reference_entries)

    # If there are discrepancies, list them and fail the test
    assert not discrepancies, f"Inconsistent msgid entries found across languages: {discrepancies}"
