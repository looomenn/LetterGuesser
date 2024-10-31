""" Main context file """
import logging.config

from config import APP_DEFAULT_LANGUAGE_CODE
from letterguesser.logic.ExperimentManager import ExperimentManager
from letterguesser.logic.Localisation import Localisation

# Global instance of the Localisation
localisation: Localisation = Localisation(
    default_lang=APP_DEFAULT_LANGUAGE_CODE,
    locale_dir='assets/locales'
)


logger = logging.getLogger('LetterGuesser')

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - [%(module)s] %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'root': {'level': 'DEBUG', 'handlers': ['stdout']}
    }
}

logging.config.dictConfig(logging_config)

# Global instance of the Experiment Manager
manager: ExperimentManager = ExperimentManager(localisation, logger)

__all__ = ['localisation', 'manager', 'logger']
