""" Localisation module """

import gettext
from babel import Locale

from .utils import get_resource_path
from config import APP_DEFAULT_LANGUAGE_CODE


class Localisation:
    """
    Localisation class
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Localisation, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 default_lang='uk',
                 domain='messages',
                 locale_dir='locales'
                 ):
        """
        :param default_lang: Default langauge code ('en', or 'uk' supported)
        :param domain: Domain name for the .mo (babel) files
        :param locale_dir: Dir containing .mo files
        """

        # avoid re-init
        if hasattr(self, 'initialized'):
            print('Localisation module already initialized')
            return

        self.domain: str = domain
        self.default_lang: str = default_lang
        self.locale_dir: str = get_resource_path(locale_dir)

        self.widgets = []
        self.current_locale = None
        self.current_translation = None

        self.load_language(self.default_lang)

    def load_language(self, lang_code: str) -> None:
        """
        Loads specified language via lang code
        :param lang_code: Language code (available: uk, en)
        :return: None
        """
        try:
            self.current_translation = gettext.translation(
                self.domain,
                localedir=self.locale_dir,
                languages=[lang_code],
                fallback=True
            )

            self.current_translation.install()
            self.current_locale = Locale(lang_code)
            self.update_all_widgets()
        except Exception as e:
            print(f'[Localisation] Error loading language {lang_code}: {str(e)}')
            self.current_translation = gettext.NullTranslations()
            self.current_locale = Locale(APP_DEFAULT_LANGUAGE_CODE)

    def translate(self, key) -> str:
        """
        Translates a given key.
        :param key: Key to be translated.
        :return: Translated text.
        """
        return self.current_translation.gettext(key)

    def bind(self,
             widget,
             translation_key,
             update_method=None
             ) -> None:
        """
        Bind a widget to a translation key for automatic updates.
        :param widget: The widget to bind (Tkinter or CTkinter)
        :param translation_key: The translation key for the widget's text.
        :param update_method: Method to update the widget text
        :return: None
        """

        def update_widget():
            translated_text = self.translate(translation_key)
            if update_method:
                update_method(translated_text)
            else:
                widget.configure(text=translated_text)

        widget._update_method = update_widget
        self.widgets.append(widget)
        update_widget()

    def update_all_widgets(self) -> None:
        """
        Update all bound widgets with the latest translation.
        :return: None
        """
        for widget in self.widgets:
            if hasattr(widget, '_update_method'):
                widget._update_method()

    def add_widget(self, widget) -> None:
        """
        Adds a widget to the list of bound widgets for localisation update
        :param widget: Widget to add
        :return: None
        """

        if widget not in self.widgets:
            self.widgets.append(widget)

    def get_locale(self) -> str:
        """
        Return the current locale.
        :return: Current locale.
        """
        return str(self.current_locale)
    