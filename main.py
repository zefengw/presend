from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from connection import db
import time, cv2 as cv

Window.size = (300, 500)


screen_helper="""
<SearchWidget@Screen>:
    MDTextField:
        hint_text: "Enter username"
        helper_text: "Forgot Username"
        helper_text_mode: "on_focus"
        pos_hint: {"x": 0.05, "y": 0.85}
        size_hint_x: 0.9

<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()

BoxLayout:
    orientation: "vertical"
    md_bg_color: app.theme_cls.primary_color
    MDToolbar:
        title: "             P R E S E N D"
        elevation: 20
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: "home"
            icon: "home"
            BoxLayout:
                orientation: "horizontal"
                Button:
                Button:
        MDBottomNavigationItem:
            name: "explore"
            icon: "search-web"
            SearchWidget:
        MDBottomNavigationItem:
            name: "record"
            icon: "plus"
            CameraClick:
        MDBottomNavigationItem:
            name: "notification"
            icon: "bell"
            BoxLayout:
                orientation: "horizontal"
                Button:
                Button:
                Button:
                Button:
        MDBottomNavigationItem:
            name: "profile"
            icon: "face-profile"
            BoxLayout:
                orientation: "horizontal"
                Button:
                Button:
                Button:
                Button:
                Button:

"""
class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")
class PresendApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        screen = Builder.load_string(screen_helper)
        return screen

    #def submit:
        #saves info to user
#The variable __name__ for the file/module that is run will be always __main__(i.e., main.py)
#But the __name__ variable for all other modules that are being imported will be set to their module's name.

if __name__ == "__main__":
    PresendApp().run()