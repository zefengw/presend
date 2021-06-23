from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color



class MainWidget(Widget):
    bottom = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_icon_bar()

    # def homepage(self):
    def init_icon_bar(self):
        with self.canvas:
            Color(0,0,0)
            self.bottom = Rectangle()


class PresendApp(App):
    pass

PresendApp().run()