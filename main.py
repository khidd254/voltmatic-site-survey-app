"""
Voltmatic Energy Solutions Site Survey App
A professional Android application for conducting solar site surveys
"""
import os
import sys
from datetime import datetime
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty

# Set window size for desktop testing
if platform != 'android':
    Window.size = (400, 700)
    Window.top = 50

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class VoltmaticApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize theme with company colors
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "A400"
        self.theme_cls.theme_style = "Light"
        
        # App configuration
        self.title = "Voltmatic Energy Solutions"
        self.icon = "assets/images/logo.png"
        
        # Initialize components
        self.screen_manager = None
        self.db = None
        
    def build(self):
        # Load KV files
        self.load_kv_files()
        
        # Import components
        from app.database import DatabaseManager
        from app.screens.home_screen import HomeScreen
        from app.screens.clients_screen import ClientsScreen
        from app.screens.survey_screen import SurveyScreen
        from app.screens.client_form_screen import ClientFormScreen
        from app.screens.surveys_list_screen import SurveysListScreen
        from app.screens.call_history_screen import CallHistoryScreen
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Add screens
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(ClientsScreen(name='clients'))
        self.screen_manager.add_widget(ClientFormScreen(name='client_form'))
        self.screen_manager.add_widget(SurveyScreen(name='survey'))
        self.screen_manager.add_widget(SurveysListScreen(name='surveys_list'))
        self.screen_manager.add_widget(CallHistoryScreen(name='call_history'))
        
        
        # Set initial screen
        self.screen_manager.current = 'home'
        
        return self.screen_manager
    
    def load_kv_files(self):
        """Load all KV files"""
        kv_files = [
            'app/screens/home_screen.kv',
            'app/screens/surveys_list_screen.kv',
            'app/screens/clients_screen.kv',
            'app/screens/survey_screen.kv',
            'app/screens/client_form_screen.kv',
            'app/screens/call_history_screen.kv',
            'app/widgets/client_card.kv',
            'app/widgets/survey_form.kv'
        ]
        
        for kv_file in kv_files:
            if os.path.exists(kv_file):
                Builder.load_file(kv_file)
    
    def on_pause(self):
        """Handle app pause (Android)"""
        return True
    
    def on_resume(self):
        """Handle app resume (Android)"""
        pass

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs('assets/icons', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Run the application
    app = VoltmaticApp()
    app.run()
