from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from app.database import DatabaseManager


class SurveysListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.dialog = None
        self.client_id = None
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_surveys()
    
    def set_client(self, client_id):
        """Set the client to filter surveys for"""
        self.client_id = client_id
    
    def set_client_filter(self, client_id):
        """Set the client to filter surveys for (alternative method name)"""
        self.client_id = client_id
        
    def load_surveys(self):
        """Load and display surveys for the selected client"""
        surveys_container = self.ids.surveys_container
        surveys_container.clear_widgets()
        
        # Update header with client name
        if self.client_id:
            client = self.db.get_client(self.client_id)
            if client:
                self.ids.header_label.text = f"Surveys for {client['name']}"
        
        try:
            # Get surveys for specific client or all surveys
            if self.client_id:
                surveys = self.db.get_site_surveys(client_id=self.client_id)
            else:
                surveys = self.db.get_site_surveys()
            
            if not surveys:
                no_surveys_label = MDLabel(
                    text="No surveys found for this client" if self.client_id else "No surveys found",
                    theme_text_color="Secondary",
                    halign="center",
                    size_hint_y=None,
                    height="48dp"
                )
                surveys_container.add_widget(no_surveys_label)
                return
            
            for survey in surveys:
                survey_card = self.create_survey_card(survey)
                surveys_container.add_widget(survey_card)
                
        except Exception as e:
            self.show_error_dialog(f"Error loading surveys: {str(e)}")
    
    def create_survey_card(self, survey):
        """Create a card widget for a survey"""
        card = MDCard(
            size_hint_y=None,
            height="120dp",
            padding="15dp",
            spacing="10dp",
            elevation=3,
            radius=[12],
            md_bg_color=(1, 1, 1, 1)
        )
        
        main_layout = MDBoxLayout(
            orientation='horizontal',
            spacing="15dp"
        )
        
        # Survey info
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing="5dp"
        )
        
        # Get client name
        client = self.db.get_client(survey['client_id'])
        client_name = client['name'] if client else "Unknown Client"
        
        # Survey title
        title_label = MDLabel(
            text=f"Survey for {client_name}",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="25dp"
        )
        info_layout.add_widget(title_label)
        
        # Survey date
        date_label = MDLabel(
            text=f"Date: {survey['survey_date']}",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(date_label)
        
        # Property type and bedrooms
        property_label = MDLabel(
            text=f"Property: {survey.get('property_type', 'N/A')} - {survey.get('number_of_bedrooms', 0)} bedrooms",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(property_label)
        
        # Status
        status_label = MDLabel(
            text=f"Status: {survey.get('status', 'pending').title()}",
            font_style="Caption",
            theme_text_color="Primary",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(status_label)
        
        main_layout.add_widget(info_layout)
        
        # Action buttons
        actions_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width="80dp",
            spacing="5dp"
        )
        
        view_button = MDIconButton(
            icon="eye",
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1),
            on_release=lambda x: self.view_survey(survey)
        )
        actions_layout.add_widget(view_button)
        
        edit_button = MDIconButton(
            icon="pencil",
            theme_text_color="Custom",
            text_color=(1, 0.6, 0, 1),
            on_release=lambda x: self.edit_survey(survey)
        )
        actions_layout.add_widget(edit_button)
        
        main_layout.add_widget(actions_layout)
        card.add_widget(main_layout)
        
        return card
    
    def view_survey(self, survey):
        """View survey details"""
        # Get client info
        client = self.db.get_client(survey['client_id'])
        client_name = client['name'] if client else "Unknown Client"
        
        # Parse appliances
        import ast
        try:
            appliances = ast.literal_eval(survey.get('appliances', '[]'))
            appliances_text = ", ".join(appliances) if appliances else "None selected"
        except:
            appliances_text = survey.get('appliances', 'None')
        
        # Handle None values safely
        monthly_spending = survey.get('monthly_spending') or 0
        recommended_size = survey.get('recommended_system_size') or 0
        estimated_cost = survey.get('estimated_cost') or 0
        bedrooms = survey.get('number_of_bedrooms') or 0
        lights = survey.get('number_of_lights') or 0
        
        details_text = f"""
Client: {client_name}
Date: {survey['survey_date']}
Surveyor: {survey.get('surveyor_name', 'N/A')}
Site Address: {survey.get('site_address', 'N/A')}

Property Information:
• Type: {survey.get('property_type', 'N/A')}
• Roof Type: {survey.get('roof_type', 'N/A')}
• Bedrooms: {bedrooms}
• Lights: {lights}
• Appliances: {appliances_text}

System Information:
• KPLC Available: {survey.get('kplc_availability', 'N/A')}
• System Type: {survey.get('system_type', 'N/A')}
• Monthly Bill: KSh {monthly_spending:,.2f}

Recommendations:
• System Size: {recommended_size} kW
• Estimated Cost: KSh {estimated_cost:,.2f}

Notes: {survey.get('notes', 'No notes')}
Status: {survey.get('status', 'pending').title()}
        """
        
        self.dialog = MDDialog(
            title="Survey Details",
            text=details_text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
    
    def edit_survey(self, survey):
        """Edit survey (navigate to survey screen with pre-filled data)"""
        # Navigate to survey screen with survey data
        self.manager.get_screen('survey').load_survey_data(survey)
        self.manager.current = 'survey'
    
    def close_dialog(self, *args):
        """Close the dialog"""
        if self.dialog:
            self.dialog.dismiss()
    
    def show_error_dialog(self, message):
        """Show error dialog"""
        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
    
    def go_back(self):
        """Navigate back to clients screen"""
        self.manager.current = 'clients'
