import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# تسجيل الخط العربي باش يظهر مريقل
LabelBase.register(name='ArabicFont', fn_regular='Arial.ttf')

class ExpertElectricApp(App):
    def build(self):
        # الخلفية الرئيسية (BoxLayout عمودي)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # العنوان العلوي
        title_text = get_display(reshape("خبير الكهرباء"))
        header = Label(text=title_text, font_name='ArabicFont', font_size='40sp', size_hint_y=0.2, color=(1, 0.8, 0, 1))
        layout.add_widget(header)

        # بوتون 1: حسابات الكابلات
        btn1 = Button(text=get_display(reshape("حساب مقطع الكابلات")), font_name='ArabicFont', font_size='25sp', background_color=(0.2, 0.2, 0.2, 1))
        layout.add_widget(btn1)

        # بوتون 2: أعطال وصيانة
        btn2 = Button(text=get_display(reshape("دليل الأعطال والصيانة")), font_name='ArabicFont', font_size='25sp', background_color=(0.2, 0.2, 0.2, 1))
        layout.add_widget(btn2)

        # بوتون 3: أسعار السلعة
        btn3 = Button(text=get_display(reshape("أسعار الأدوات الكهربائية")), font_name='ArabicFont', font_size='25sp', background_color=(0.2, 0.2, 0.2, 1))
        layout.add_widget(btn3)

        return layout

if __name__ == '__main__':
    ExpertElectricApp().run()
