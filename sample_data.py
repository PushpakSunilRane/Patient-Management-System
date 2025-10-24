"""
Sample data script to populate the healthcare dashboard with test data.
Run this script after setting up the database to add sample patients, doctors, and appointments.
"""

from database import DatabaseManager
from datetime import datetime, date, time, timedelta
import random

def add_sample_data():
    """Add sample data to the database"""
    db = DatabaseManager()
    
    # Sample doctors
    doctors_data = [
        ("Dr. Sarah Johnson", "Cardiology", "sarah.johnson@hospital.com", "555-0101", 15),
        ("Dr. Michael Chen", "Neurology", "michael.chen@hospital.com", "555-0102", 12),
        ("Dr. Emily Rodriguez", "Pediatrics", "emily.rodriguez@hospital.com", "555-0103", 8),
        ("Dr. David Wilson", "Orthopedics", "david.wilson@hospital.com", "555-0104", 20),
        ("Dr. Lisa Anderson", "Dermatology", "lisa.anderson@hospital.com", "555-0105", 10),
        ("Dr. James Brown", "Internal Medicine", "james.brown@hospital.com", "555-0106", 18),
        ("Dr. Maria Garcia", "Oncology", "maria.garcia@hospital.com", "555-0107", 14),
        ("Dr. Robert Taylor", "Psychiatry", "robert.taylor@hospital.com", "555-0108", 16)
    ]
    
    print("Adding sample doctors...")
    for doctor in doctors_data:
        db.add_doctor(*doctor)
    
    # Sample patients
    patients_data = [
        ("John Smith", 45, "Male", "john.smith@email.com", "555-1001", "123 Main St, City", "Hypertension, Diabetes"),
        ("Jane Doe", 32, "Female", "jane.doe@email.com", "555-1002", "456 Oak Ave, City", "Allergies"),
        ("Bob Johnson", 67, "Male", "bob.johnson@email.com", "555-1003", "789 Pine St, City", "Arthritis, Heart condition"),
        ("Alice Brown", 28, "Female", "alice.brown@email.com", "555-1004", "321 Elm St, City", "None"),
        ("Charlie Wilson", 55, "Male", "charlie.wilson@email.com", "555-1005", "654 Maple Dr, City", "High cholesterol"),
        ("Diana Lee", 41, "Female", "diana.lee@email.com", "555-1006", "987 Cedar Ln, City", "Migraines"),
        ("Frank Miller", 73, "Male", "frank.miller@email.com", "555-1007", "147 Birch St, City", "Parkinson's, Diabetes"),
        ("Grace Taylor", 29, "Female", "grace.taylor@email.com", "555-1008", "258 Spruce Ave, City", "Anxiety"),
        ("Henry Davis", 52, "Male", "henry.davis@email.com", "555-1009", "369 Willow Way, City", "Back pain"),
        ("Ivy Martinez", 36, "Female", "ivy.martinez@email.com", "555-1010", "741 Ash Blvd, City", "Asthma"),
        ("Jack Thompson", 61, "Male", "jack.thompson@email.com", "555-1011", "852 Poplar Pl, City", "Prostate issues"),
        ("Kelly White", 44, "Female", "kelly.white@email.com", "555-1012", "963 Hickory Hwy, City", "Thyroid condition"),
        ("Larry Green", 38, "Male", "larry.green@email.com", "555-1013", "159 Dogwood Dr, City", "Sleep apnea"),
        ("Megan Clark", 26, "Female", "megan.clark@email.com", "555-1014", "357 Sycamore St, City", "None"),
        ("Nick Adams", 49, "Male", "nick.adams@email.com", "555-1015", "468 Magnolia Ave, City", "Depression")
    ]
    
    print("Adding sample patients...")
    for patient in patients_data:
        db.add_patient(*patient)
    
    # Sample appointments
    print("Adding sample appointments...")
    
    # Get doctor and patient IDs
    doctors = db.get_doctors()
    patients = db.get_patients()
    
    if not doctors or not patients:
        print("Error: No doctors or patients found. Please add them first.")
        return
    
    # Common conditions
    conditions = [
        "Routine checkup",
        "Chest pain",
        "Headache",
        "Back pain",
        "High blood pressure",
        "Diabetes management",
        "Annual physical",
        "Skin rash",
        "Joint pain",
        "Anxiety consultation",
        "Follow-up visit",
        "Vaccination",
        "Blood test results",
        "X-ray review",
        "Medication adjustment"
    ]
    
    # Generate appointments for the next 30 days
    base_date = date.today()
    appointment_times = [
        time(9, 0), time(9, 30), time(10, 0), time(10, 30),
        time(11, 0), time(11, 30), time(14, 0), time(14, 30),
        time(15, 0), time(15, 30), time(16, 0), time(16, 30)
    ]
    
    statuses = ["Scheduled", "Completed", "Cancelled", "No Show"]
    status_weights = [0.6, 0.3, 0.05, 0.05]  # 60% scheduled, 30% completed, 5% each for cancelled/no show
    
    for i in range(50):  # Create 50 sample appointments
        # Random date within next 30 days
        appointment_date = base_date + timedelta(days=random.randint(0, 30))
        
        # Random time
        appointment_time = random.choice(appointment_times)
        
        # Random patient and doctor
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        
        # Random condition
        condition = random.choice(conditions)
        
        # Random status with weights
        status = random.choices(statuses, weights=status_weights)[0]
        
        # Random notes
        notes = f"Patient reported {condition.lower()}. Follow-up scheduled if needed."
        
        db.add_appointment(
            patient['id'],
            doctor['id'],
            appointment_date,
            appointment_time,
            condition,
            notes
        )
    
    print("Sample data added successfully!")
    print(f"Added {len(doctors_data)} doctors")
    print(f"Added {len(patients_data)} patients")
    print("Added 50 sample appointments")
    
    db.disconnect()

if __name__ == "__main__":
    add_sample_data()
