# core
import customtkinter as ctk

# frames
from .BaseFrame import BaseFrame

# utils
from config import *
from styles import *


class HeaderFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # app title
        self.app_name_label = ctk.CTkLabel(
            self,
            height=text_large_height,
            text=APP_TITLE,
            font=ctk.CTkFont(
                family=font,
                size=text_large
            )
        )
        self.add_widget(self.app_name_label, side='left', fill='y', expand=True, pady=pad_4, padx=(pad_4, pad_0))

        # language selector
        self.language_selector = ctk.CTkSegmentedButton(
            self,
            values=['Ukrainian', 'English'],
            command=self.change_language
        )

        self.language_selector.set(APP_DEFAULT_LANGUAGE)
        self.add_widget(self.language_selector, side='left', fill=None, expand=False, padx=(pad_0, pad_4))

    def toggle_langauge(self, event=None):
        curr_lang = self.localisation.get_locale()

        if curr_lang == "en":
            self.language_selector.set('Ukrainian')
            self.localisation.load_language('uk')
        else:
            self.language_selector.set('English')
            self.localisation.load_language('en')

        self.manager.reset_experiment()

    def change_language(self, langauge):
        lang_code = "en" if langauge == 'English' else "uk"
        self.localisation.load_language(lang_code)

        self.manager.reset_experiment()
