from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        # بوتون بسيطة بالأنڨليزي باش نتأكدوا إنو التطبيق يخدم
        return Button(text='HAKIMI ELECTRIC V0.3')

if __name__ == '__main__':
    TestApp().run()
