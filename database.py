import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import DB_CONFIG
import streamlit as st

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
        except Error as e:
            st.error(f"Error connecting to MySQL: {e}")
            self.connection = None
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute SQL query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            st.error(f"Database error: {e}")
            return None
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        tables = {
            'doctors': """
                CREATE TABLE IF NOT EXISTS doctors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    specialization VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    phone VARCHAR(20),
                    experience_years INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'patients': """
                CREATE TABLE IF NOT EXISTS patients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT,
                    gender ENUM('Male', 'Female', 'Other'),
                    email VARCHAR(100) UNIQUE,
                    phone VARCHAR(20),
                    address TEXT,
                    medical_history TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'appointments': """
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT,
                    doctor_id INT,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status ENUM('Scheduled', 'Completed', 'Cancelled', 'No Show') DEFAULT 'Scheduled',
                    condition_description TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
                )
            """
        }
        
        for table_name, query in tables.items():
            self.execute_query(query, fetch=False)
            print(f"Table {table_name} created/verified successfully")
    
    def get_doctors(self):
        """Get all doctors"""
        return self.execute_query("SELECT * FROM doctors ORDER BY name")
    
    def get_patients(self):
        """Get all patients"""
        return self.execute_query("SELECT * FROM patients ORDER BY name")
    
    def get_appointments(self):
        """Get all appointments with patient and doctor details"""
        query = """
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        return self.execute_query(query)
    
    def add_doctor(self, name, specialization, email, phone, experience_years):
        """Add new doctor"""
        query = """
            INSERT INTO doctors (name, specialization, email, phone, experience_years)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (name, specialization, email, phone, experience_years), fetch=False)
    
    def add_patient(self, name, age, gender, email, phone, address, medical_history):
        """Add new patient"""
        query = """
            INSERT INTO patients (name, age, gender, email, phone, address, medical_history)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (name, age, gender, email, phone, address, medical_history), fetch=False)
    
    def add_appointment(self, patient_id, doctor_id, appointment_date, appointment_time, condition_description, notes):
        """Add new appointment"""
        query = """
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, condition_description, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (patient_id, doctor_id, appointment_date, appointment_time, condition_description, notes), fetch=False)
    
    def update_doctor(self, doctor_id, name, specialization, email, phone, experience_years):
        """Update doctor information"""
        query = """
            UPDATE doctors 
            SET name=%s, specialization=%s, email=%s, phone=%s, experience_years=%s
            WHERE id=%s
        """
        return self.execute_query(query, (name, specialization, email, phone, experience_years, doctor_id), fetch=False)
    
    def update_patient(self, patient_id, name, age, gender, email, phone, address, medical_history):
        """Update patient information"""
        query = """
            UPDATE patients 
            SET name=%s, age=%s, gender=%s, email=%s, phone=%s, address=%s, medical_history=%s
            WHERE id=%s
        """
        return self.execute_query(query, (name, age, gender, email, phone, address, medical_history, patient_id), fetch=False)
    
    def update_appointment(self, appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status, condition_description, notes):
        """Update appointment information"""
        query = """
            UPDATE appointments 
            SET patient_id=%s, doctor_id=%s, appointment_date=%s, appointment_time=%s, status=%s, condition_description=%s, notes=%s
            WHERE id=%s
        """
        return self.execute_query(query, (patient_id, doctor_id, appointment_date, appointment_time, status, condition_description, notes, appointment_id), fetch=False)
    
    def delete_doctor(self, doctor_id):
        """Delete doctor"""
        query = "DELETE FROM doctors WHERE id=%s"
        return self.execute_query(query, (doctor_id,), fetch=False)
    
    def delete_patient(self, patient_id):
        """Delete patient"""
        query = "DELETE FROM patients WHERE id=%s"
        return self.execute_query(query, (patient_id,), fetch=False)
    
    def delete_appointment(self, appointment_id):
        """Delete appointment"""
        query = "DELETE FROM appointments WHERE id=%s"
        return self.execute_query(query, (appointment_id,), fetch=False)
    
    def get_appointment_stats(self):
        """Get appointment statistics for dashboard"""
        stats = {}
        
        # Total appointments by status
        status_query = """
            SELECT status, COUNT(*) as count 
            FROM appointments 
            GROUP BY status
        """
        stats['by_status'] = self.execute_query(status_query)
        
        # Appointments by month
        monthly_query = """
            SELECT DATE_FORMAT(appointment_date, '%Y-%m') as month, COUNT(*) as count
            FROM appointments 
            WHERE appointment_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            GROUP BY month
            ORDER BY month
        """
        stats['monthly'] = self.execute_query(monthly_query)
        
        # Doctor workload
        doctor_workload_query = """
            SELECT d.name, d.specialization, COUNT(a.id) as appointment_count
            FROM doctors d
            LEFT JOIN appointments a ON d.id = a.doctor_id
            WHERE a.appointment_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY d.id, d.name, d.specialization
            ORDER BY appointment_count DESC
        """
        stats['doctor_workload'] = self.execute_query(doctor_workload_query)
        
        # Patient conditions
        conditions_query = """
            SELECT condition_description, COUNT(*) as count
            FROM appointments 
            WHERE condition_description IS NOT NULL AND condition_description != ''
            GROUP BY condition_description
            ORDER BY count DESC
            LIMIT 10
        """
        stats['conditions'] = self.execute_query(conditions_query)
        
        return stats
