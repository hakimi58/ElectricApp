from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class ElectricApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # عنوان التطبيق
        label = Label(text="Expert Electric App", font_size='30sp', color=(0, 1, 0, 1))
        
        # زر للتجربة
        btn = Button(text="اضغط هنا للتجربة", size_hint=(1, 0.2))
        btn.bind(on_press=self.on_click)
        
        layout.add_widget(label)
        layout.add_widget(btn)
        
        return layout

    def on_click(self, instance):
        instance.text = "خدمت مريڨلة يا حكيم!"

if __name__ == "__main__":
    ElectricApp().run()
