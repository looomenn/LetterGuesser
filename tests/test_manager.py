from unittest.mock import MagicMock, patch

import pytest

from letterguesser.logic.ExperimentManager import ExperimentManager


@pytest.fixture
def experiment_manager():
    localisation_mock = MagicMock()
    localisation_mock.get_alphabet.return_value = ['a', 'b', 'c', 'd']
    localisation_mock.get_locale.return_value = "en"
    logger_mock = MagicMock()
    manager = ExperimentManager(localisation=localisation_mock, logger=logger_mock)
    return manager


def test_singleton_pattern(experiment_manager):
    """Test that ExperimentManager follows the singleton pattern."""
    another_instance = ExperimentManager(localisation=experiment_manager.localisation, logger=experiment_manager.logger)
    assert another_instance is experiment_manager


def test_get_next_char(experiment_manager):
    """Test fetching the next character in sequence."""
    experiment_manager.full_text = "abcdef"
    experiment_manager.visible_text = "abc"
    next_char = experiment_manager.get_next_char()
    assert next_char == 'd'

    experiment_manager.visible_text = "abcdef"
    next_char = experiment_manager.get_next_char()
    assert next_char is None


def test_start_experiment(experiment_manager):
    """Test that start_experiment initializes the experiment correctly."""
    with patch.object(experiment_manager, 'get_text', return_value="testing") as mock_get_text:
        experiment_manager.start_experiment()
        assert experiment_manager.is_active
        assert experiment_manager.text == "testing"
        assert experiment_manager.visible_text == experiment_manager.text[:experiment_manager.ngram_order]


def test_next_experiment(experiment_manager):
    """Test advancing to the next experiment."""
    initial_experiment_number = experiment_manager.experiment_number
    experiment_manager.next_experiment()
    assert experiment_manager.experiment_number == initial_experiment_number + 1
    assert experiment_manager.used_letters == []


def test_reset_experiment(experiment_manager):
    """Test resetting the experiment."""
    experiment_manager.is_active = True
    experiment_manager.reset_experiment()
    assert experiment_manager.is_active is False
    assert experiment_manager.used_letters == []
    assert experiment_manager.experiment_number == 0


def test_input_handler_correct_input(experiment_manager):
    """Test input handler with a correct input character."""
    experiment_manager.full_text = "a"
    experiment_manager.next_char = "a"
    result = experiment_manager.input_handler("a")
    assert result == "correct"


def test_input_handler_incorrect_input(experiment_manager):
    """Test input handler with an incorrect input character."""
    experiment_manager.full_text = "a"
    experiment_manager.next_char = "a"
    result = experiment_manager.input_handler("b")
    assert result == "incorrect"


def test_input_handler_invalid_input(experiment_manager):
    """Test input handler with an invalid input character."""
    result = experiment_manager.input_handler("1")
    assert result == "invalid"
