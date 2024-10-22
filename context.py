""" Main context file """

from config import APP_DEFAULT_LANGUAGE_CODE

from logic.ExperimentManger import ExperimentManager
from logic.Localisation import Localisation

# Global instance of the Localisation
localisation: Localisation = Localisation(
    default_lang=APP_DEFAULT_LANGUAGE_CODE,
    locale_dir='assets/locales'
)

# Global instance of the Experiment Manager
manager: ExperimentManager = ExperimentManager(localisation)


__all__ = ['localisation', 'manager']