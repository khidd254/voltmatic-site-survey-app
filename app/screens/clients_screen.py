"""
Clients management screen for Voltmatic Energy Solutions Site Survey App
"""
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

class ClientsScreen(Screen):
    """Screen for managing clients"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.dialog = None
    
    def on_enter(self):
        """Called when screen is entered"""
        if not self.db:
            from app.database import DatabaseManager
            self.db = DatabaseManager()
        self.load_clients()
    
    def load_clients(self, dt=None):
        """Load clients from database"""
        if not hasattr(self.ids, 'clients_list'):
            print("clients_list not found in ids")
            return
            
        # Ensure database is initialized
        if not self.db:
            from app.database import DatabaseManager
            self.db = DatabaseManager()
        
        try:
            clients = self.db.get_clients()
            print(f"Found {len(clients)} clients")  # Debug print
            
            # Clear existing items
            self.ids.clients_list.clear_widgets()
            
            if not clients:
                # Show empty state
                empty_label = MDLabel(
                    text="No clients found. Add your first client!",
                    halign="center",
                    size_hint_y=None,
                    height="48dp"
                )
                self.ids.clients_list.add_widget(empty_label)
                return
            
            # Add client cards
            for client in clients:
                client_card = self.create_client_card(client)
                self.ids.clients_list.add_widget(client_card)
                
        except Exception as e:
            print(f"Error loading clients: {str(e)}")
            error_label = MDLabel(
                text=f"Error loading clients: {str(e)}",
                halign="center",
                size_hint_y=None,
                height="48dp"
            )
            self.ids.clients_list.add_widget(error_label)
    
    def create_client_card(self, client):
        """Create a client card"""
        card = MDCard(
            size_hint_y=None,
            height="120dp",
            padding="15dp",
            spacing="10dp",
            elevation=3,
            radius=[12],
            md_bg_color=(1, 1, 1, 1)
        )
        
        content = MDBoxLayout(orientation='horizontal', spacing="15dp")
        
        # Client info
        info_layout = MDBoxLayout(orientation='vertical', spacing="5dp")
        
        name_label = MDLabel(
            text=client['name'],
            font_style="H6",
            size_hint_y=None,
            height="25dp"
        )
        
        contact_label = MDLabel(
            text=f" {client['phone']} | {client['email'] or 'No email'}",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        
        address_label = MDLabel(
            text=f"📍 {client['address'][:50]}..." if len(client['address']) > 50 else f"📍 {client['address']}",
            font_style="Caption",
            size_hint_y=None,
            height="20dp"
        )
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(contact_label)
        info_layout.add_widget(address_label)
        
        # Action buttons
        actions_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            width="250dp",
            spacing="5dp"
        )
        
        call_button = MDIconButton(
            icon="phone",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.2, 1),
            on_release=lambda x: self.call_client(client['id'], client['phone'])
        )
        
        survey_button = MDIconButton(
            icon="clipboard-plus",
            on_release=lambda x: self.start_survey(client['id'])
        )
        
        view_surveys_button = MDIconButton(
            icon="eye",
            on_release=lambda x: self.view_surveys(client['id'])
        )
        
        edit_button = MDIconButton(
            icon="pencil",
            on_release=lambda x: self.edit_client(client['id'])
        )
        
        delete_button = MDIconButton(
            icon="delete",
            theme_text_color="Custom",
            text_color=(1, 0.2, 0.2, 1),
            on_release=lambda x: self.confirm_delete_client(client['id'], client['name'])
        )
        
        # Call history button
        call_history_button = MDIconButton(
            icon="history",
            theme_text_color="Custom",
            text_color=(0.6, 0.4, 1, 1),
            on_release=lambda x: self.view_call_history(client['id'])
        )
        
        actions_layout.add_widget(call_button)
        actions_layout.add_widget(call_history_button)
        actions_layout.add_widget(survey_button)
        actions_layout.add_widget(view_surveys_button)
        actions_layout.add_widget(edit_button)
        actions_layout.add_widget(delete_button)
        
        content.add_widget(info_layout)
        content.add_widget(actions_layout)
        card.add_widget(content)
        
        return card
    
    def start_survey(self, client_id):
        """Start a new survey for the client"""
        survey_screen = self.manager.get_screen('survey')
        survey_screen.set_client(client_id)
        self.manager.current = 'survey'
    
    def call_client(self, client_id, phone_number):
        """Initiate call and log it"""
        import webbrowser
        import urllib.parse
        
        # Open phone dialer (works on mobile devices)
        phone_url = f"tel:{phone_number}"
        try:
            webbrowser.open(phone_url)
        except:
            pass  # If can't open dialer, continue to log form
        
        # Show call log form
        self.show_call_log_form(client_id)
    
    def show_call_log_form(self, client_id):
        """Show form to log call details"""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.checkbox import MDCheckbox
        
        # Create form content
        content = MDBoxLayout(
            orientation='vertical',
            spacing="10dp",
            size_hint_y=None,
            height="400dp"
        )
        
        self.caller_name_field = MDTextField(
            hint_text="Your Name",
            size_hint_y=None,
            height="50dp"
        )
        
        self.call_duration_field = MDTextField(
            hint_text="Call Duration (e.g., 5 minutes)",
            size_hint_y=None,
            height="50dp"
        )
        
        self.call_purpose_field = MDTextField(
            hint_text="Call Purpose",
            size_hint_y=None,
            height="50dp"
        )
        
        self.call_notes_field = MDTextField(
            hint_text="Call Notes/Discussion",
            multiline=True,
            size_hint_y=None,
            height="100dp"
        )
        
        self.call_outcome_field = MDTextField(
            hint_text="Call Outcome",
            size_hint_y=None,
            height="50dp"
        )
        
        # Follow-up checkbox
        follow_up_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="40dp"
        )
        
        self.follow_up_checkbox = MDCheckbox(
            size_hint_x=None,
            width="40dp"
        )
        
        follow_up_label = MDLabel(
            text="Follow-up required",
            size_hint_y=None,
            height="40dp"
        )
        
        follow_up_layout.add_widget(self.follow_up_checkbox)
        follow_up_layout.add_widget(follow_up_label)
        
        self.follow_up_date_field = MDTextField(
            hint_text="Follow-up Date (YYYY-MM-DD)",
            size_hint_y=None,
            height="50dp"
        )
        
        content.add_widget(self.caller_name_field)
        content.add_widget(self.call_duration_field)
        content.add_widget(self.call_purpose_field)
        content.add_widget(self.call_notes_field)
        content.add_widget(self.call_outcome_field)
        content.add_widget(follow_up_layout)
        content.add_widget(self.follow_up_date_field)
        
        self.call_log_dialog = MDDialog(
            title="Log Call Details",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_call_log_dialog
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=lambda x: self.save_call_log(client_id)
                )
            ]
        )
        self.call_log_dialog.open()
    
    def save_call_log(self, client_id):
        """Save the call log to database"""
        from datetime import datetime
        
        try:
            call_data = {
                'client_id': client_id,
                'call_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'caller_name': self.caller_name_field.text or '',
                'call_duration': self.call_duration_field.text or '',
                'call_purpose': self.call_purpose_field.text or '',
                'call_notes': self.call_notes_field.text or '',
                'call_outcome': self.call_outcome_field.text or '',
                'follow_up_required': self.follow_up_checkbox.active,
                'follow_up_date': self.follow_up_date_field.text if self.follow_up_checkbox.active and self.follow_up_date_field.text else None
            }
            
            self.db.add_call_log(call_data)
            self.close_call_log_dialog()
            self.show_success_dialog("Call logged successfully")
        except Exception as e:
            print(f"Call log error: {str(e)}")  # Debug print
            self.close_call_log_dialog()  # Close dialog even on error
            self.show_error_dialog(f"Error saving call log: {str(e)}")
    
    def close_call_log_dialog(self, *args):
        """Close call log dialog"""
        if hasattr(self, 'call_log_dialog'):
            self.call_log_dialog.dismiss()
    
    def view_surveys(self, client_id):
        """Navigate to surveys list for specific client"""
        surveys_screen = self.manager.get_screen('surveys_list')
        surveys_screen.set_client_filter(client_id)
        self.manager.current = 'surveys_list'
    
    def view_call_history(self, client_id):
        """Navigate to call history for specific client"""
        call_history_screen = self.manager.get_screen('call_history')
        call_history_screen.set_client(client_id)
        self.manager.current = 'call_history'
    
    def edit_client(self, client_id):
        """Edit client information"""
        client_form_screen = self.manager.get_screen('client_form')
        client_form_screen.set_client_for_edit(client_id)
        self.manager.current = 'client_form'
    
    def add_client(self):
        """Navigate to add client form"""
        self.manager.current = 'client_form'
    
    def refresh_clients(self):
        """Refresh the clients list"""
        self.load_clients()
    
    def confirm_delete_client(self, client_id, client_name):
        """Show confirmation dialog before deleting client"""
        self.dialog = MDDialog(
            title="Delete Client",
            text=f"Are you sure you want to delete '{client_name}' and all their survey data?\n\nThis action cannot be undone.",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Custom",
                    text_color=(1, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_client(client_id)
                )
            ]
        )
        self.dialog.open()
    
    def delete_client(self, client_id):
        """Delete the client and all their data"""
        self.close_dialog()  # Close confirmation dialog first
        
        try:
            success = self.db.delete_client(client_id)
            if success:
                self.load_clients()  # Refresh the list
                self.show_success_dialog("Client deleted successfully")
            else:
                self.show_error_dialog("Failed to delete client")
        except Exception as e:
            self.show_error_dialog(f"Error deleting client: {str(e)}")
    
    def show_success_dialog(self, message):
        """Show success dialog"""
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
    
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
    
    def close_dialog(self, *args):
        """Close the dialog"""
        if self.dialog:
            self.dialog.dismiss()
    
    def go_back(self):
        """Go back to home screen"""
        self.manager.current = 'home'
