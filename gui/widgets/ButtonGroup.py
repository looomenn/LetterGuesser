# frames
from gui.frames.BaseFrame import BaseFrame

# widgets
from .Button import Button
from .OptionMenu import OptionMenu

# utils
from styles.padding import *


class ButtonGroup(BaseFrame):
    def __init__(self,
                 parent: BaseFrame,
                 configs: [dict],
                 gap: int = pad_2,
                 **kwargs
                 ):
        """
        Inits ButtonGroup class
        :param parent: The parent widget.
        :param configs: A list of dicts where each one specifies: type(button, option_menu), label_key, style,
         command and is_disabled (se Button Class).
        :param gap: The gap between buttons.
        :param kwargs: Additional keywords for CTkButton class
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.buttons = {}

        for i, config in enumerate(configs):
            
            widget_type = config.get('type', 'button')

            if widget_type == 'button':
                item = Button(
                    parent=self,
                    label_key=config['label_key'],
                    style=config.get('style', 'default'),
                    command=config.get('command', None),
                    is_disabled=config.get('is_disabled', False)
                )
            elif widget_type == 'option_menu':
                item = OptionMenu(
                    parent=self,
                    label_key=config['label_key'],
                    initial_value=config.get('initial_value', ''),
                    values=config.get('values', []),
                    command=config.get('command')
                )
            else:
                raise ValueError(f"Unsupported widget type: {widget_type}")

            self.add_widget(
                item,
                side='left',
                expand=False,
                fill='x',
                padx=(pad_0, gap) if i < len(configs) - 1 else pad_0,
            )

            self.buttons[f'button_{config["label_key"]}'] = item

    def get_button(self, key) -> Button | None:
        """
        Returns a specific button by its key.
        :param key: The key of the button (e.g., 'button_<label_key>')
        :return: The Button instance or None if not found.
        """
        return self.buttons.get(key, None)

    def disable(self, key):
        button = self.get_button(key)
        if button:
            button.disable()

    def enable(self, key):
        button = self.get_button(key)
        if button:
            button.enable()

    def update_label(self, key, new_label_key):
        button = self.get_button(key)
        if button:
            button.localisation.bind(button, new_label_key)

    def enable_all(self):
        """ Enables all buttons in the group """
        for button in self.buttons.values():
            button.enable()

    def disable_all(self):
        """ Disables all buttons in the group """
        for button in self.buttons.values():
            button.disable()
