"""
Site survey screen for collecting survey data
"""
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime

class SurveyScreen(Screen):
    """Screen for conducting site surveys"""
    
    client_id = NumericProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.dialog = None
        self.selected_client = None
        self.property_type_menu = None
        self.kplc_menu = None
        self.system_type_menu = None
        self.roof_type_menu = None
    
    def on_enter(self):
        """Called when screen is entered"""
        if not self.db:
            from app.database import DatabaseManager
            self.db = DatabaseManager()
        
        # Check if client is selected
        if not self.client_id:
            self.show_error("Please select a client first before creating a survey")
            self.manager.current = 'clients'
            return
        
        # Set current date and time when entering survey
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ids.survey_date_field.text = current_datetime
    
    def set_client(self, client_id):
        """Set the client for this survey"""
        self.client_id = client_id
        if self.db:
            client = self.db.get_client(client_id)
            if client:
                self.selected_client = client
                self.ids.client_name.text = f"Client: {client['name']}"
                self.ids.site_address_field.text = client['address']
    
    def open_date_picker(self):
        """Open date picker for survey date"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
    
    def get_date(self, instance, value, date_range):
        """Get selected date"""
        self.ids.survey_date_field.text = str(value)
        instance.dismiss()
    
    def show_property_type_menu(self):
        """Show property type dropdown menu"""
        menu_items = [
            {"text": "Bungalow", "viewclass": "OneLineListItem", "on_release": lambda x="Bungalow": self.set_property_type(x)},
            {"text": "Mansion", "viewclass": "OneLineListItem", "on_release": lambda x="Mansion": self.set_property_type(x)},
            {"text": "Commercial", "viewclass": "OneLineListItem", "on_release": lambda x="Commercial": self.set_property_type(x)},
        ]
        self.property_type_menu = MDDropdownMenu(
            caller=self.ids.property_type,
            items=menu_items,
            width_mult=4,
        )
        self.property_type_menu.open()
    
    def set_property_type(self, property_type):
        """Set selected property type"""
        self.ids.property_type.text = property_type
        self.property_type_menu.dismiss()
    
    def show_kplc_menu(self):
        """Show KPLC availability dropdown menu"""
        menu_items = [
            {"text": "Yes", "viewclass": "OneLineListItem", "on_release": lambda x="Yes": self.set_kplc_availability(x)},
            {"text": "No", "viewclass": "OneLineListItem", "on_release": lambda x="No": self.set_kplc_availability(x)},
        ]
        self.kplc_menu = MDDropdownMenu(
            caller=self.ids.kplc_availability,
            items=menu_items,
            width_mult=4,
        )
        self.kplc_menu.open()
    
    def set_kplc_availability(self, availability):
        """Set KPLC availability"""
        self.ids.kplc_availability.text = availability
        self.kplc_menu.dismiss()
    
    def show_system_type_menu(self):
        """Show system type dropdown menu"""
        menu_items = [
            {"text": "Backup", "viewclass": "OneLineListItem", "on_release": lambda x="Backup": self.set_system_type(x)},
            {"text": "Off-grid", "viewclass": "OneLineListItem", "on_release": lambda x="Off-grid": self.set_system_type(x)},
            {"text": "Hybrid", "viewclass": "OneLineListItem", "on_release": lambda x="Hybrid": self.set_system_type(x)},
        ]
        self.system_type_menu = MDDropdownMenu(
            caller=self.ids.system_type,
            items=menu_items,
            width_mult=4,
        )
        self.system_type_menu.open()
    
    def set_system_type(self, system_type):
        """Set selected system type"""
        self.ids.system_type.text = system_type
        self.system_type_menu.dismiss()
    
    def show_roof_type_menu(self):
        """Show roof type dropdown menu"""
        menu_items = [
            {"text": "Flat Roof", "viewclass": "OneLineListItem", "on_release": lambda x="Flat Roof": self.set_roof_type(x)},
            {"text": "Pitched Roof", "viewclass": "OneLineListItem", "on_release": lambda x="Pitched Roof": self.set_roof_type(x)},
        ]
        self.roof_type_menu = MDDropdownMenu(
            caller=self.ids.roof_type,
            items=menu_items,
            width_mult=4,
        )
        self.roof_type_menu.open()
    
    def set_roof_type(self, roof_type):
        """Set selected roof type"""
        self.ids.roof_type.text = roof_type
        self.roof_type_menu.dismiss()
    
    def calculate_system_size(self):
        """Calculate recommended system size based on energy usage"""
        try:
            energy_usage = float(self.ids.energy_usage_field.text or 0)
            # Simple calculation: 1kW system per 150 kWh monthly usage
            recommended_size = energy_usage / 150
            self.ids.system_size_field.text = f"{recommended_size:.1f}"
            
            # Estimate cost (rough calculation)
            cost_per_kw = 90000  # KES per kW
            estimated_cost = recommended_size * cost_per_kw
            self.ids.estimated_cost_field.text = f"{estimated_cost:,.0f}"
            
        except ValueError:
            pass
    
    def save_survey(self):
        """Save survey data"""
        try:
            # Ensure database is initialized
            if not self.db:
                from app.database import DatabaseManager
                self.db = DatabaseManager()
            
            # Get selected appliances
            appliances = []
            if self.ids.tv_checkbox.active:
                appliances.append("TV")
            if self.ids.refrigerator_checkbox.active:
                appliances.append("Refrigerator")
            if self.ids.ironbox_checkbox.active:
                appliances.append("Ironbox")
            if self.ids.microwave_checkbox.active:
                appliances.append("Microwave")
            if self.ids.ac_checkbox.active:
                appliances.append("Air Conditioner")
            if self.ids.washing_machine_checkbox.active:
                appliances.append("Washing Machine")
            
            # Get form data
            survey_data = {
                'client_id': self.client_id,
                'survey_date': self.ids.survey_date_field.text,
                'surveyor_name': self.ids.surveyor_name_field.text,
                'site_address': self.ids.site_address_field.text,
                'property_type': self.ids.property_type.text,
                'roof_type': self.ids.roof_type.text,
                'number_of_bedrooms': int(self.ids.number_of_bedrooms.text) if self.ids.number_of_bedrooms.text else 0,
                'number_of_lights': int(self.ids.number_of_lights.text) if self.ids.number_of_lights.text else 0,
                'appliances': str(appliances),
                'kplc_availability': self.ids.kplc_availability.text,
                'system_type': self.ids.system_type.text,
                'monthly_spending': float(self.ids.monthly_spending_field.text) if self.ids.monthly_spending_field.text else 0.0,
                'recommended_system_size': float(self.ids.system_size_field.text) if self.ids.system_size_field.text else 0.0,
                'estimated_cost': float(self.ids.estimated_cost_field.text) if self.ids.estimated_cost_field.text else 0.0,
                'notes': self.ids.notes_field.text,
                'photos': '[]'  # Empty for now
            }
            
            # Validate required fields
            if not all([survey_data['client_id'], survey_data['surveyor_name'], survey_data['site_address']]):
                self.show_error("Please fill in all required fields")
                return
            
            # Save to database
            self.db.add_site_survey(survey_data)
            
            self.show_success("Survey saved successfully!")
            self.clear_form()
            self.go_back()
            
        except Exception as e:
            self.show_error(f"Error saving survey: {str(e)}")
    
    def load_survey_data(self, survey):
        """Load existing survey data for editing"""
        try:
            self.survey_id = survey['id']
            self.client_id = survey['client_id']
            
            # Load client info
            client = self.db.get_client(self.client_id)
            if client:
                self.ids.client_name_label.text = client['name']
                self.ids.client_phone_label.text = client['phone']
            
            # Fill form fields
            self.ids.survey_date_field.text = survey.get('survey_date', '')
            self.ids.surveyor_name_field.text = survey.get('surveyor_name', '')
            self.ids.site_address_field.text = survey.get('site_address', '')
            self.ids.property_type.text = survey.get('property_type', '')
            self.ids.number_of_bedrooms.text = str(survey.get('number_of_bedrooms', ''))
            self.ids.electrical_panel_field.text = survey.get('electrical_panel_info', '')
            self.ids.energy_usage_field.text = str(survey.get('current_energy_usage', ''))
            self.ids.system_size_field.text = str(survey.get('recommended_system_size', ''))
            self.ids.estimated_cost_field.text = str(survey.get('estimated_cost', ''))
            self.ids.notes_field.text = survey.get('notes', '')
            
            # Load appliances checkboxes
            import ast
            try:
                appliances = ast.literal_eval(survey.get('appliances', '[]'))
                self.ids.tv_checkbox.active = "TV" in appliances
                self.ids.refrigerator_checkbox.active = "Refrigerator" in appliances
                self.ids.water_heater_checkbox.active = "Water Heater" in appliances
                self.ids.ac_checkbox.active = "Air Conditioner" in appliances
                self.ids.washing_machine_checkbox.active = "Washing Machine" in appliances
            except:
                pass
                
        except Exception as e:
            self.show_error(f"Error loading survey data: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.client_id = None
        self.survey_id = None
        self.selected_client = None
        fields = [
            'client_name', 'surveyor_name_field', 'survey_date_field',
            'site_address_field', 'roof_type_field', 'roof_condition_field',
            'roof_area_field', 'shading_field', 'electrical_panel_field',
            'energy_usage_field', 'system_size_field', 'estimated_cost_field',
            'notes_field'
        ]
        
        for field in fields:
            if hasattr(self.ids, field):
                self.ids[field].text = ''
    
    def show_error(self, message):
        """Show error dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def show_success(self, message):
        """Show success dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def go_back(self):
        """Go back to previous screen"""
        self.manager.current = 'home'
    
    def on_enter(self):
        """Called when screen is entered"""
        if not self.client_id:
            # Set default date to today
            self.ids.survey_date_field.text = datetime.now().strftime('%Y-%m-%d')
