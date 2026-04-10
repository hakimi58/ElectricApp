from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
import arabic_reshaper
from bidi.algorithm import get_display

class ElectricApp(App):
    # دالة سحرية باش العربي يظهر مريڨل ومن اليمين لليسار
    def format_arabic(self, text):
        reshaped_text = arabic_reshaper.reshape(text) # تلصيق الحروف
        return get_display(reshaped_text) # قلب الاتجاه من اليمين لليسار

    def build(self):
        # المجلد الرئيسي للتطبيق
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # اسم ملف الخط اللي رفعتو إنت
        ar_font = "Arial.ttf" 

        # العنوان بالعربي
        title_text = self.format_arabic("تطبيق خبير الكهرباء")
        label = Label(
            text=title_text, 
            font_size='35sp', 
            font_name=ar_font,
            color=(0, 1, 0, 1) # لون أخضر
        )
        
        # الزر بالعربي
        btn_text = self.format_arabic("اضغط هنا يا حكيم")
        btn = Button(
            text=btn_text, 
            size_hint=(1, 0.2), 
            font_name=ar_font,
            background_color=(0.1, 0.5, 0.8, 1) # لون أزرق
        )
        btn.bind(on_press=self.on_click)
        
        layout.add_widget(label)
        layout.add_widget(btn)
        
        return layout

    def on_click(self, instance):
        # تغيير نص الزر عند الضغط
        instance.text = self.format_arabic("أحلى جو.. العربي خدم!")

if __name__ == "__main__":
    ElectricApp().run()
