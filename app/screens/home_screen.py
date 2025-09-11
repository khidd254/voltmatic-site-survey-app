"""
Home screen for Voltmatic Energy Solutions Site Survey App
"""
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

class HomeScreen(Screen):
    """Main home screen with dashboard and quick actions"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
    
    def on_enter(self):
        """Called when screen is entered"""
        if not self.db:
            from app.database import DatabaseManager
            self.db = DatabaseManager()
        self.load_dashboard_data()
    
    def load_dashboard_data(self, dt=None):
        """Load dashboard statistics and recent surveys"""
        if not self.db:
            return
        
        try:
            # Get statistics
            clients = self.db.get_clients()
            surveys = self.db.get_site_surveys()
            recent_surveys = self.db.get_recent_surveys(3)
            
            # Update dashboard cards
            if hasattr(self.ids, 'clients_count'):
                self.ids.clients_count.text = str(len(clients))
            if hasattr(self.ids, 'surveys_count'):
                self.ids.surveys_count.text = str(len(surveys))
            if hasattr(self.ids, 'pending_surveys'):
                pending = len([s for s in surveys if s['status'] == 'pending'])
                self.ids.pending_surveys.text = str(pending)
            
            # Load recent surveys
            self.load_recent_surveys(recent_surveys)
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def load_recent_surveys(self, surveys):
        """Load recent surveys into the list"""
        if not hasattr(self.ids, 'recent_surveys_list'):
            return
        
        # Clear existing items
        self.ids.recent_surveys_list.clear_widgets()
        
        for survey in surveys:
            # Create survey card
            card = MDCard(
                size_hint_y=None,
                height="80dp",
                padding="10dp",
                spacing="5dp",
                elevation=2,
                radius=[8],
                md_bg_color=(1, 1, 1, 1)
            )
            
            # Add survey info
            from kivymd.uix.label import MDLabel
            from kivymd.uix.boxlayout import MDBoxLayout
            
            content = MDBoxLayout(orientation='vertical', spacing="2dp")
            
            title = MDLabel(
                text=f"{survey['client_name']} - {survey['site_address'][:30]}...",
                font_style="Subtitle2",
                theme_text_color="Primary",
                size_hint_y=None,
                height="20dp"
            )
            
            subtitle = MDLabel(
                text=f"Date: {survey['survey_date']} | Status: {survey['status'].title()}",
                font_style="Caption",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="16dp"
            )
            
            content.add_widget(title)
            content.add_widget(subtitle)
            card.add_widget(content)
            
            self.ids.recent_surveys_list.add_widget(card)
    
    def go_to_clients(self):
        """Navigate to clients screen"""
        self.manager.current = 'clients'
    
    def add_client(self):
        """Navigate to add client form"""
        self.manager.current = 'client_form'
    
    def view_surveys(self):
        """Navigate to surveys screen"""
        self.manager.current = 'surveys_list'
    
    def go_to_surveys(self):
        """Navigate to surveys list"""
        # For now, go to clients screen
        self.manager.current = 'clients'
    
    def go_to_new_survey(self):
        """Navigate to new survey screen"""
        self.manager.current = 'survey'
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        self.load_dashboard_data(0)
