from letterguesser.gui.frames.BaseFrame import BaseFrame

from .ListItem import ListItem


class List(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.items = []

    def get_items(self):
        return self.items if self.items else []

    def add_item(self, data):
        is_odd = len(self.items) % 2 == 1
        item = ListItem(self, data, is_odd)
        self.add_widget(item, fill='x')

        self.items.append(item)

    def update_items(self, data):
        for item in self.items:
            item.destroy()
        self.items.clear()

        for i in data:
            self.add_item(i)

    def clear(self):
        for item in self.items:
            item.destroy()
        self.items.clear()