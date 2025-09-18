from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class VoltmaticApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text='Voltmatic Site Survey App', 
                     font_size='24sp', 
                     size_hint_y=None, 
                     height='60dp')
        
        btn1 = Button(text='Start Survey', size_hint_y=None, height='50dp')
        btn2 = Button(text='View Clients', size_hint_y=None, height='50dp')
        btn3 = Button(text='Settings', size_hint_y=None, height='50dp')
        
        layout.add_widget(title)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        
        return layout

VoltmaticApp().run()
