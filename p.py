from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import random

class BrightLight(Widget):
    def __init__(self, **kwargs):
        super(BrightLight, self).__init__(**kwargs)
        self.color = (0.5, 0.5, 0.5, 1)  # خاکستری پیش‌فرض
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.update_rect()
    
    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color)
            Rectangle(pos=self.pos, size=self.size)
    
    def set_color(self, color):
        self.color = color
        self.update_rect()

class TrafficLightApp(App):
    def build(self):
        # ساخت لایه اصلی با پس‌زمینه تیره
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with self.main_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # پس‌زمینه تیره
            Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
        
        # دکمه قرمز شروع
        self.start_button = Button(
            text='start',
            background_color=(1, 0, 0, 1),
            background_normal='',
            font_size=40,
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1)  # متن سفید
        )
        self.start_button.bind(on_press=self.start_sequence)
        self.main_layout.add_widget(self.start_button)
        
        # برچسب برای شمارش با رنگ سفید
        self.count_label = Label(
            text='',
            font_size=100,  # بزرگتر
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1),  # رنگ سفید
            bold=True
        )
        self.main_layout.add_widget(self.count_label)
        
        # لایه برای چراغ‌ها
        self.lights_layout = GridLayout(cols=2, rows=1, spacing=50, size_hint=(1, 0.4))
        
        # ایجاد چراغ اول با رنگ پررنگ
        self.light1 = BrightLight()
        self.lights_layout.add_widget(self.light1)
        
        # ایجاد چراغ دوم با رنگ پررنگ
        self.light2 = BrightLight()
        self.lights_layout.add_widget(self.light2)
        
        self.main_layout.add_widget(self.lights_layout)
        
        # دکمه سبز برای شروع مجدد
        self.restart_button = Button(
            text='Restart',
            background_color=(0, 1, 0, 1),
            background_normal='',
            font_size=35,
            size_hint=(1, 0.15),
            disabled=True,
            color=(0, 0, 0, 1)  # متن سیاه
        )
        self.restart_button.bind(on_press=self.restart_app)
        self.main_layout.add_widget(self.restart_button)
        
        # اطمینان از به‌روزرسانی پس‌زمینه
        self.main_layout.bind(pos=self.update_bg, size=self.update_bg)
        
        return self.main_layout
    
    def update_bg(self, *args):
        self.main_layout.canvas.before.clear()
        with self.main_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
    
    def start_sequence(self, instance):
        self.start_button.disabled = True
        self.count_label.text = 'Ready...'
        Clock.schedule_once(self.count_1, 1)
    
    def count_1(self, dt):
        self.count_label.text = '1'
        Clock.schedule_once(self.count_2, 1)
    
    def count_2(self, dt):
        self.count_label.text = '2'
        Clock.schedule_once(self.count_3, 1)
    
    def count_3(self, dt):
        self.count_label.text = '3'
        Clock.schedule_once(self.turn_on_light1, 1)
    
    def turn_on_light1(self, dt):
        # رنگ‌های بسیار پررنگ و روشن
        colors = [
            (0.0, 1.0, 0.0, 1.0),    # سبز خالص - بسیار روشن
            (1.0, 0.0, 0.0, 1.0),    # قرمز خالص - بسیار روشن
            (1.0, 1.0, 0.0, 1.0)     # زرد خالص - بسیار روشن
        ]
        color1 = random.choice(colors)
        self.light1.set_color(color1)
        
        Clock.schedule_once(self.turn_on_light2, 0.05)
    
    def turn_on_light2(self, dt):
        colors = [
            (0.0, 1.0, 0.0, 1.0),    # سبز خالص
            (1.0, 0.0, 0.0, 1.0)     # قرمز خالص
        ]
        color2 = random.choice(colors)
        self.light2.set_color(color2)
        
        self.count_label.text = 'wait...'
        Clock.schedule_once(self.enable_restart_button, 2)
    
    def enable_restart_button(self, dt):
        self.restart_button.disabled = False
        self.count_label.text = 'finished!'
        self.count_label.color = (1, 1, 1, 1)  # سفید
    
    def restart_app(self, instance):
        self.start_button.disabled = False
        self.restart_button.disabled = True
        self.count_label.text = ''
        self.count_label.color = (1, 1, 1, 1)  # سفید
        
        # خاموش کردن چراغ‌ها
        self.light1.set_color((0.3, 0.3, 0.3, 1))  # خاکستری تیره
        self.light2.set_color((0.3, 0.3, 0.3, 1))  # خاکستری تیره

if __name__ == '__main__':
    TrafficLightApp().run()
