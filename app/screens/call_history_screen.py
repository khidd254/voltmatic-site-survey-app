"""
Call History screen for Voltmatic Energy Solutions Site Survey App
"""
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from app.database import DatabaseManager


class CallHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.dialog = None
        self.client_id = None
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_call_history()
    
    def set_client(self, client_id):
        """Set the client to show call history for"""
        self.client_id = client_id
        
    def load_call_history(self):
        """Load and display call history for the selected client"""
        calls_container = self.ids.calls_container
        calls_container.clear_widgets()
        
        # Update header with client name
        if self.client_id:
            client = self.db.get_client(self.client_id)
            if client:
                self.ids.header_label.title = f"Call History - {client['name']}"
        
        try:
            # Get call logs for specific client
            if self.client_id:
                calls = self.db.get_call_logs(client_id=self.client_id)
            else:
                calls = self.db.get_call_logs()
            
            if not calls:
                no_calls_label = MDLabel(
                    text="No call history found for this client" if self.client_id else "No call history found",
                    theme_text_color="Secondary",
                    halign="center",
                    size_hint_y=None,
                    height="48dp"
                )
                calls_container.add_widget(no_calls_label)
                return
            
            for call in calls:
                call_card = self.create_call_card(call)
                calls_container.add_widget(call_card)
                
        except Exception as e:
            self.show_error_dialog(f"Error loading call history: {str(e)}")
    
    def create_call_card(self, call):
        """Create a card widget for a call log"""
        card = MDCard(
            size_hint_y=None,
            height="140dp",
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
        
        # Call info
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing="5dp"
        )
        
        # Get client name if not already filtered by client
        if not self.client_id:
            client = self.db.get_client(call['client_id'])
            client_name = client['name'] if client else "Unknown Client"
            
            client_label = MDLabel(
                text=f"Client: {client_name}",
                font_style="H6",
                theme_text_color="Primary",
                size_hint_y=None,
                height="25dp"
            )
            info_layout.add_widget(client_label)
        
        # Call date and caller
        date_label = MDLabel(
            text=f"Date: {call['call_date']} | Caller: {call.get('caller_name', 'N/A')}",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(date_label)
        
        # Duration and purpose
        details_label = MDLabel(
            text=f"Duration: {call.get('call_duration', 'N/A')} | Purpose: {call.get('call_purpose', 'N/A')}",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(details_label)
        
        # Outcome
        outcome_label = MDLabel(
            text=f"Outcome: {call.get('call_outcome', 'N/A')}",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        info_layout.add_widget(outcome_label)
        
        # Follow-up indicator
        if call.get('follow_up_required'):
            follow_up_label = MDLabel(
                text=f"📅 Follow-up: {call.get('follow_up_date', 'Date not set')}",
                font_style="Caption",
                theme_text_color="Primary",
                size_hint_y=None,
                height="20dp"
            )
            info_layout.add_widget(follow_up_label)
        
        main_layout.add_widget(info_layout)
        
        # Action button
        actions_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width="50dp",
            spacing="5dp"
        )
        
        view_button = MDIconButton(
            icon="eye",
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1),
            on_release=lambda x: self.view_call_details(call)
        )
        actions_layout.add_widget(view_button)
        
        main_layout.add_widget(actions_layout)
        card.add_widget(main_layout)
        
        return card
    
    def view_call_details(self, call):
        """View detailed call information"""
        # Get client info
        client = self.db.get_client(call['client_id'])
        client_name = client['name'] if client else "Unknown Client"
        
        details_text = f"""
Call Details:

Client: {client_name}
Date & Time: {call['call_date']}
Caller: {call.get('caller_name', 'N/A')}
Duration: {call.get('call_duration', 'N/A')}

Purpose: {call.get('call_purpose', 'N/A')}

Notes:
{call.get('call_notes', 'No notes recorded')}

Outcome: {call.get('call_outcome', 'N/A')}

Follow-up Required: {'Yes' if call.get('follow_up_required') else 'No'}
{f"Follow-up Date: {call.get('follow_up_date')}" if call.get('follow_up_required') else ""}
        """
        
        self.dialog = MDDialog(
            title="Call Details",
            text=details_text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()
    
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
