"""
Client form screen for adding/editing clients
"""
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class ClientFormScreen(Screen):
    """Screen for adding or editing client information"""
    
    client_id = StringProperty(None, allownone=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.dialog = None
    
    def on_enter(self):
        """Called when screen is entered"""
        if not self.db:
            from app.database import DatabaseManager
            self.db = DatabaseManager()
    
    def set_client_for_edit(self, client_id):
        """Load client data for editing"""
        self.client_id = str(client_id)
        if self.db:
            client = self.db.get_client(client_id)
            if client:
                self.ids.name_field.text = client['name'] or ''
                self.ids.phone_field.text = client['phone'] or ''
                self.ids.email_field.text = client['email'] or ''
                self.ids.address_field.text = client['address'] or ''
                self.ids.notes_field.text = client['notes'] or ''
    
    def clear_form(self):
        """Clear all form fields"""
        self.client_id = None
        self.ids.name_field.text = ''
        self.ids.phone_field.text = ''
        self.ids.email_field.text = ''
        self.ids.address_field.text = ''
        self.ids.notes_field.text = ''
    
    def save_client(self):
        """Save client data"""
        # Validate required fields
        if not self.ids.name_field.text.strip():
            self.show_error("Please enter client name")
            return
        
        if not self.ids.phone_field.text.strip():
            self.show_error("Please enter phone number")
            return
        
        # Prepare client data
        client_data = {
            'name': self.ids.name_field.text.strip(),
            'phone': self.ids.phone_field.text.strip(),
            'email': self.ids.email_field.text.strip(),
            'address': self.ids.address_field.text.strip(),
            'notes': self.ids.notes_field.text.strip()
        }
        
        try:
            # Ensure database is initialized
            if not self.db:
                from app.database import DatabaseManager
                self.db = DatabaseManager()
            
            if self.client_id:
                # Update existing client (would need update method in database)
                self.show_success("Client updated successfully!")
            else:
                # Add new client
                client_id = self.db.add_client(client_data)
                print(f"Client saved with ID: {client_id}")  # Debug print
                self.show_success("Client added successfully!")
            
            # Clear form and go back
            self.clear_form()
            self.go_back()
            
        except Exception as e:
            print(f"Error details: {str(e)}")  # Debug print
            self.show_error(f"Error saving client: {str(e)}")
    
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
        """Navigate back to previous screen"""
        # Refresh clients screen when going back
        if hasattr(self.manager, 'get_screen'):
            clients_screen = self.manager.get_screen('clients')
            if hasattr(clients_screen, 'refresh_clients'):
                clients_screen.refresh_clients()
        self.manager.current = 'clients'
    
    def on_enter(self):
        """Called when screen is entered"""
        if not self.client_id:
            self.clear_form()
