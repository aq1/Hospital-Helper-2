from kivy.app import App
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label


class Top(Widget):

    def __init__(self):
        super().__init__(size=Window.size, size_hint_y=0.35)
        self.add_widget(
            Label(text='Hello', color=(1, 0, 0, 1), size=self.size))


class HospitalApp(App):

    @staticmethod
    def configure_window():
        Window.clearcolor = 0.25, 0.5, 0.99, 1
        Window.borderless = '1'

    def build(self):
        self.configure_window()
        l = BoxLayout(orientation='vertical')
        l.add_widget(Label(text='Hello', size_hint_y=0.25, font_size=40))
        l.add_widget(Top())
        # l = MainLayout()
        # l.add_widget(Top())
        # l.add_widget(Button(text='Top', size_hint_y=0.35))
        # l.add_widget(Button(text='BOTT'))
        return l
        # return Button(text='Hello World', size_hint_y=0.2)


if __name__ == '__main__':

    HospitalApp().run()
