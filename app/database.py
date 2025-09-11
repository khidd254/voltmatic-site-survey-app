"""
Database manager for Voltmatic Energy Solutions Site Survey App
"""
import sqlite3
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class DatabaseManager:
    """Manages SQLite database operations for the app"""
    
    def __init__(self):
        self.db_path = os.path.join('data', 'voltmatic.db')
        self.init_database()
        self.create_sample_data()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Clients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    location_coordinates TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # Site surveys table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS site_surveys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    survey_date DATE,
                    surveyor_name TEXT,
                    site_address TEXT,
                    property_type TEXT,
                    roof_type TEXT,
                    number_of_bedrooms INTEGER,
                    number_of_lights INTEGER,
                    appliances TEXT,
                    kplc_availability TEXT,
                    system_type TEXT,
                    monthly_spending REAL,
                    recommended_system_size REAL,
                    estimated_cost REAL,
                    photos TEXT,
                    notes TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            # Site visits table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS site_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    visit_date DATE,
                    visit_time TIME,
                    purpose TEXT,
                    notes TEXT,
                    status TEXT DEFAULT 'scheduled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            # Call logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS call_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    call_date DATETIME,
                    caller_name TEXT,
                    call_duration TEXT,
                    call_purpose TEXT,
                    call_notes TEXT,
                    call_outcome TEXT,
                    follow_up_required BOOLEAN DEFAULT 0,
                    follow_up_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            conn.commit()
    
    def create_sample_data(self):
        """Create sample data if database is empty"""
        # No longer creating sample data - start with empty database
        pass
    
    def add_client(self, client_data: Dict) -> int:
        """Add a new client"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clients (name, phone, email, address, location_coordinates, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                client_data['name'],
                client_data['phone'],
                client_data['email'],
                client_data['address'],
                client_data.get('location_coordinates', ''),
                client_data.get('notes', '')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_clients(self) -> List[Dict]:
        """Get all clients"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_client(self, client_id: int) -> Optional[Dict]:
        """Get a specific client"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def delete_client(self, client_id: int) -> bool:
        """Delete a client and all their associated data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete all surveys for this client
            cursor.execute("DELETE FROM site_surveys WHERE client_id = ?", (client_id,))
            
            # Delete all call logs for this client
            cursor.execute("DELETE FROM call_logs WHERE client_id = ?", (client_id,))
            
            # Delete all site visits for this client
            cursor.execute("DELETE FROM site_visits WHERE client_id = ?", (client_id,))
            
            # Then delete the client
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def add_site_survey(self, survey_data: Dict) -> int:
        """Add a new site survey"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO site_surveys (client_id, survey_date, surveyor_name, site_address, property_type, roof_type, number_of_bedrooms, number_of_lights, appliances, kplc_availability, system_type, monthly_spending, recommended_system_size, estimated_cost, photos, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                survey_data.get('client_id'),
                survey_data.get('survey_date'),
                survey_data.get('surveyor_name'),
                survey_data.get('site_address'),
                survey_data.get('property_type'),
                survey_data.get('roof_type'),
                survey_data.get('number_of_bedrooms'),
                survey_data.get('number_of_lights'),
                survey_data.get('appliances'),
                survey_data.get('kplc_availability'),
                survey_data.get('system_type'),
                survey_data.get('monthly_spending'),
                survey_data.get('recommended_system_size'),
                survey_data.get('estimated_cost'),
                json.dumps(survey_data.get('photos', [])),
                survey_data.get('notes'),
                survey_data.get('status', 'pending')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_site_surveys(self, client_id: Optional[int] = None) -> List[Dict]:
        """Get site surveys, optionally filtered by client"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if client_id:
                cursor.execute('''
                    SELECT s.*, c.name as client_name 
                    FROM site_surveys s 
                    JOIN clients c ON s.client_id = c.id 
                    WHERE s.client_id = ? 
                    ORDER BY s.created_at DESC
                ''', (client_id,))
            else:
                cursor.execute('''
                    SELECT s.*, c.name as client_name 
                    FROM site_surveys s 
                    JOIN clients c ON s.client_id = c.id 
                    ORDER BY s.created_at DESC
                ''')
            
            surveys = []
            for row in cursor.fetchall():
                survey = dict(row)
                survey['photos'] = json.loads(survey['photos']) if survey['photos'] else []
                surveys.append(survey)
            
            return surveys
    
    def get_recent_surveys(self, limit: int = 5) -> List[Dict]:
        """Get recent site surveys"""
        surveys = self.get_site_surveys()
        return surveys[:limit]
    
    def add_call_log(self, call_data: Dict) -> int:
        """Add a new call log"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO call_logs (client_id, call_date, caller_name, call_duration, call_purpose, call_notes, call_outcome, follow_up_required, follow_up_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                call_data.get('client_id'),
                call_data.get('call_date'),
                call_data.get('caller_name'),
                call_data.get('call_duration'),
                call_data.get('call_purpose'),
                call_data.get('call_notes'),
                call_data.get('call_outcome'),
                call_data.get('follow_up_required', False),
                call_data.get('follow_up_date')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_call_logs(self, client_id: Optional[int] = None) -> List[Dict]:
        """Get call logs, optionally filtered by client"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if client_id:
                cursor.execute("SELECT * FROM call_logs WHERE client_id = ? ORDER BY call_date DESC", (client_id,))
            else:
                cursor.execute("SELECT * FROM call_logs ORDER BY call_date DESC")
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
