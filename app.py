import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time
from streamlit_option_menu import option_menu
from database import DatabaseManager
import config

# Page configuration
st.set_page_config(
    page_title=config.STREAMLIT_CONFIG['page_title'],
    page_icon=config.STREAMLIT_CONFIG['page_icon'],
    layout=config.STREAMLIT_CONFIG['layout'],
    initial_sidebar_state=config.STREAMLIT_CONFIG['initial_sidebar_state']
)

# Initialize database
@st.cache_resource
def init_database():
    db = DatabaseManager()
    db.create_tables()
    return db

db = init_database()

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="🏥 Healthcare Dashboard",
        options=["Dashboard", "Patients", "Doctors", "Appointments", "Analytics"],
        icons=["house", "people", "person-badge", "calendar", "graph-up"],
        menu_icon="cast",
        default_index=0,
    )

# Dashboard Page
if selected == "Dashboard":
    st.title("🏥 Healthcare Dashboard")
    st.markdown("---")
    
    # Get statistics
    stats = db.get_appointment_stats()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = len(db.get_patients())
        st.metric("Total Patients", total_patients)
    
    with col2:
        total_doctors = len(db.get_doctors())
        st.metric("Total Doctors", total_doctors)
    
    with col3:
        total_appointments = len(db.get_appointments())
        st.metric("Total Appointments", total_appointments)
    
    with col4:
        scheduled_appointments = len([a for a in db.get_appointments() if a['status'] == 'Scheduled'])
        st.metric("Scheduled Appointments", scheduled_appointments)
    
    st.markdown("---")
    
    # Recent appointments
    st.subheader("📅 Recent Appointments")
    appointments = db.get_appointments()[:10]  # Get last 10 appointments
    if appointments:
        df_appointments = pd.DataFrame(appointments)
        st.dataframe(df_appointments[['patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'status']], use_container_width=True)
    else:
        st.info("No appointments found")

# Patients Page
elif selected == "Patients":
    st.title("👥 Patient Management")
    
    # Patient operations
    operation = st.selectbox("Select Operation", ["View Patients", "Add Patient", "Update Patient", "Delete Patient"])
    
    if operation == "View Patients":
        st.subheader("All Patients")
        patients = db.get_patients()
        if patients:
            df_patients = pd.DataFrame(patients)
            st.dataframe(df_patients, use_container_width=True)
        else:
            st.info("No patients found")
    
    elif operation == "Add Patient":
        st.subheader("Add New Patient")
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                age = st.number_input("Age*", min_value=0, max_value=120)
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Phone")
                address = st.text_area("Address")
                medical_history = st.text_area("Medical History")
            
            submitted = st.form_submit_button("Add Patient")
            if submitted:
                if name and age and gender:
                    if db.add_patient(name, age, gender, email, phone, address, medical_history):
                        st.success("Patient added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    elif operation == "Update Patient":
        st.subheader("Update Patient")
        patients = db.get_patients()
        if patients:
            patient_options = {f"{p['name']} (ID: {p['id']})": p['id'] for p in patients}
            selected_patient = st.selectbox("Select Patient", list(patient_options.keys()))
            
            if selected_patient:
                patient_id = patient_options[selected_patient]
                patient_data = next(p for p in patients if p['id'] == patient_id)
                
                with st.form("update_patient_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name*", value=patient_data['name'])
                        age = st.number_input("Age*", min_value=0, max_value=120, value=patient_data['age'])
                        gender = st.selectbox("Gender*", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient_data['gender']))
                        email = st.text_input("Email", value=patient_data['email'] or "")
                    with col2:
                        phone = st.text_input("Phone", value=patient_data['phone'] or "")
                        address = st.text_area("Address", value=patient_data['address'] or "")
                        medical_history = st.text_area("Medical History", value=patient_data['medical_history'] or "")
                    
                    submitted = st.form_submit_button("Update Patient")
                    if submitted:
                        if name and age and gender:
                            if db.update_patient(patient_id, name, age, gender, email, phone, address, medical_history):
                                st.success("Patient updated successfully!")
                                st.rerun()
                        else:
                                    st.error("Please fill in all required fields (*)")
        else:
            st.info("No patients found")
    
    elif operation == "Delete Patient":
        st.subheader("Delete Patient")
        patients = db.get_patients()
        if patients:
            patient_options = {f"{p['name']} (ID: {p['id']})": p['id'] for p in patients}
            selected_patient = st.selectbox("Select Patient to Delete", list(patient_options.keys()))
            
            if selected_patient:
                patient_id = patient_options[selected_patient]
                if st.button("Delete Patient", type="secondary"):
                    if db.delete_patient(patient_id):
                        st.success("Patient deleted successfully!")
                        st.rerun()
        else:
            st.info("No patients found")

# Doctors Page
elif selected == "Doctors":
    st.title("👨‍⚕️ Doctor Management")
    
    # Doctor operations
    operation = st.selectbox("Select Operation", ["View Doctors", "Add Doctor", "Update Doctor", "Delete Doctor"])
    
    if operation == "View Doctors":
        st.subheader("All Doctors")
        doctors = db.get_doctors()
        if doctors:
            df_doctors = pd.DataFrame(doctors)
            st.dataframe(df_doctors, use_container_width=True)
        else:
            st.info("No doctors found")
    
    elif operation == "Add Doctor":
        st.subheader("Add New Doctor")
        with st.form("add_doctor_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                specialization = st.text_input("Specialization*")
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Phone")
                experience_years = st.number_input("Experience (Years)*", min_value=0, max_value=50)
            
            submitted = st.form_submit_button("Add Doctor")
            if submitted:
                if name and specialization and experience_years is not None:
                    if db.add_doctor(name, specialization, email, phone, experience_years):
                        st.success("Doctor added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    elif operation == "Update Doctor":
        st.subheader("Update Doctor")
        doctors = db.get_doctors()
        if doctors:
            doctor_options = {f"{d['name']} (ID: {d['id']})": d['id'] for d in doctors}
            selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))
            
            if selected_doctor:
                doctor_id = doctor_options[selected_doctor]
                doctor_data = next(d for d in doctors if d['id'] == doctor_id)
                
                with st.form("update_doctor_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name*", value=doctor_data['name'])
                        specialization = st.text_input("Specialization*", value=doctor_data['specialization'])
                        email = st.text_input("Email", value=doctor_data['email'] or "")
                    with col2:
                        phone = st.text_input("Phone", value=doctor_data['phone'] or "")
                        experience_years = st.number_input("Experience (Years)*", min_value=0, max_value=50, value=doctor_data['experience_years'])
                    
                    submitted = st.form_submit_button("Update Doctor")
                    if submitted:
                        if name and specialization and experience_years is not None:
                            if db.update_doctor(doctor_id, name, specialization, email, phone, experience_years):
                                st.success("Doctor updated successfully!")
                                st.rerun()
                        else:
                            st.error("Please fill in all required fields (*)")
        else:
            st.info("No doctors found")
    
    elif operation == "Delete Doctor":
        st.subheader("Delete Doctor")
        doctors = db.get_doctors()
        if doctors:
            doctor_options = {f"{d['name']} (ID: {d['id']})": d['id'] for d in doctors}
            selected_doctor = st.selectbox("Select Doctor to Delete", list(doctor_options.keys()))
            
            if selected_doctor:
                doctor_id = doctor_options[selected_doctor]
                if st.button("Delete Doctor", type="secondary"):
                    if db.delete_doctor(doctor_id):
                        st.success("Doctor deleted successfully!")
                        st.rerun()
        else:
            st.info("No doctors found")

# Appointments Page
elif selected == "Appointments":
    st.title("📅 Appointment Management")
    
    # Appointment operations
    operation = st.selectbox("Select Operation", ["View Appointments", "Add Appointment", "Update Appointment", "Delete Appointment"])
    
    if operation == "View Appointments":
        st.subheader("All Appointments")
        appointments = db.get_appointments()
        if appointments:
            df_appointments = pd.DataFrame(appointments)
            st.dataframe(df_appointments, use_container_width=True)
        else:
            st.info("No appointments found")
    
    elif operation == "Add Appointment":
        st.subheader("Add New Appointment")
        with st.form("add_appointment_form"):
            col1, col2 = st.columns(2)
            with col1:
                # Get patients and doctors for selection
                patients = db.get_patients()
                doctors = db.get_doctors()
                
                if patients and doctors:
                    patient_options = {f"{p['name']} (ID: {p['id']})": p['id'] for p in patients}
                    doctor_options = {f"{d['name']} - {d['specialization']} (ID: {d['id']})": d['id'] for d in doctors}
                    
                    patient_id = st.selectbox("Select Patient*", list(patient_options.keys()))
                    doctor_id = st.selectbox("Select Doctor*", list(doctor_options.keys()))
                    
                    appointment_date = st.date_input("Appointment Date*", min_value=date.today())
                    appointment_time = st.time_input("Appointment Time*")
                else:
                    st.error("Please add patients and doctors first")
                    patient_id = doctor_id = None
                    appointment_date = appointment_time = None
            
            with col2:
                condition_description = st.text_area("Condition Description")
                notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Appointment")
            if submitted and patient_id and doctor_id and appointment_date and appointment_time:
                patient_id_val = patient_options[patient_id]
                doctor_id_val = doctor_options[doctor_id]
                
                if db.add_appointment(patient_id_val, doctor_id_val, appointment_date, appointment_time, condition_description, notes):
                    st.success("Appointment added successfully!")
                    st.rerun()
            elif submitted:
                st.error("Please fill in all required fields (*)")
    
    elif operation == "Update Appointment":
        st.subheader("Update Appointment")
        appointments = db.get_appointments()
        if appointments:
            appointment_options = {f"{a['patient_name']} with {a['doctor_name']} on {a['appointment_date']} (ID: {a['id']})": a['id'] for a in appointments}
            selected_appointment = st.selectbox("Select Appointment", list(appointment_options.keys()))
            
            if selected_appointment:
                appointment_id = appointment_options[selected_appointment]
                appointment_data = next(a for a in appointments if a['id'] == appointment_id)
                
                with st.form("update_appointment_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        # Get patients and doctors for selection
                        patients = db.get_patients()
                        doctors = db.get_doctors()
                        
                        patient_options = {f"{p['name']} (ID: {p['id']})": p['id'] for p in patients}
                        doctor_options = {f"{d['name']} - {d['specialization']} (ID: {d['id']})": d['id'] for d in doctors}
                        
                        patient_id = st.selectbox("Select Patient*", list(patient_options.keys()), 
                                                 index=list(patient_options.values()).index(appointment_data['patient_id']))
                        doctor_id = st.selectbox("Select Doctor*", list(doctor_options.keys()),
                                               index=list(doctor_options.values()).index(appointment_data['doctor_id']))
                        
                        appointment_date = st.date_input("Appointment Date*", value=appointment_data['appointment_date'])
                        appointment_time = st.time_input("Appointment Time*", value=appointment_data['appointment_time'])
                        status = st.selectbox("Status*", ["Scheduled", "Completed", "Cancelled", "No Show"], 
                                            index=["Scheduled", "Completed", "Cancelled", "No Show"].index(appointment_data['status']))
                    
                    with col2:
                        condition_description = st.text_area("Condition Description", value=appointment_data['condition_description'] or "")
                        notes = st.text_area("Notes", value=appointment_data['notes'] or "")
                    
                    submitted = st.form_submit_button("Update Appointment")
                    if submitted:
                        patient_id_val = patient_options[patient_id]
                        doctor_id_val = doctor_options[doctor_id]
                        
                        if db.update_appointment(appointment_id, patient_id_val, doctor_id_val, appointment_date, appointment_time, status, condition_description, notes):
                            st.success("Appointment updated successfully!")
                            st.rerun()
        else:
            st.info("No appointments found")
    
    elif operation == "Delete Appointment":
        st.subheader("Delete Appointment")
        appointments = db.get_appointments()
        if appointments:
            appointment_options = {f"{a['patient_name']} with {a['doctor_name']} on {a['appointment_date']} (ID: {a['id']})": a['id'] for a in appointments}
            selected_appointment = st.selectbox("Select Appointment to Delete", list(appointment_options.keys()))
            
            if selected_appointment:
                appointment_id = appointment_options[selected_appointment]
                if st.button("Delete Appointment", type="secondary"):
                    if db.delete_appointment(appointment_id):
                        st.success("Appointment deleted successfully!")
                        st.rerun()
        else:
            st.info("No appointments found")

# Analytics Page
elif selected == "Analytics":
    st.title("📊 Analytics & Insights")
    
    # Get statistics
    stats = db.get_appointment_stats()
    
    # Appointment Status Distribution
    st.subheader("📈 Appointment Status Distribution")
    if stats['by_status']:
        status_df = pd.DataFrame(stats['by_status'])
        fig_status = px.pie(status_df, values='count', names='status', title="Appointments by Status")
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("No appointment data available")
    
    # Monthly Appointment Trends
    st.subheader("📅 Monthly Appointment Trends")
    if stats['monthly']:
        monthly_df = pd.DataFrame(stats['monthly'])
        fig_monthly = px.line(monthly_df, x='month', y='count', title="Appointments Over Time")
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("No monthly data available")
    
    # Doctor Workload
    st.subheader("👨‍⚕️ Doctor Workload (Last 30 Days)")
    if stats['doctor_workload']:
        workload_df = pd.DataFrame(stats['doctor_workload'])
        fig_workload = px.bar(workload_df, x='name', y='appointment_count', 
                             title="Appointments per Doctor", 
                             labels={'appointment_count': 'Number of Appointments', 'name': 'Doctor'})
        fig_workload.update_xaxis(tickangle=45)
        st.plotly_chart(fig_workload, use_container_width=True)
    else:
        st.info("No workload data available")
    
    # Patient Conditions
    st.subheader("🩺 Common Patient Conditions")
    if stats['conditions']:
        conditions_df = pd.DataFrame(stats['conditions'])
        fig_conditions = px.bar(conditions_df, x='condition_description', y='count',
                               title="Most Common Conditions",
                               labels={'count': 'Number of Cases', 'condition_description': 'Condition'})
        fig_conditions.update_xaxis(tickangle=45)
        st.plotly_chart(fig_conditions, use_container_width=True)
    else:
        st.info("No condition data available")
    
    # Additional Analytics
    st.subheader("📋 Additional Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Patient demographics
        patients = db.get_patients()
        if patients:
            patient_df = pd.DataFrame(patients)
            
            # Age distribution
            if 'age' in patient_df.columns and patient_df['age'].notna().any():
                fig_age = px.histogram(patient_df, x='age', title="Patient Age Distribution", nbins=20)
                st.plotly_chart(fig_age, use_container_width=True)
            
            # Gender distribution
            if 'gender' in patient_df.columns:
                gender_counts = patient_df['gender'].value_counts()
                fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, title="Patient Gender Distribution")
                st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Doctor specializations
        doctors = db.get_doctors()
        if doctors:
            doctor_df = pd.DataFrame(doctors)
            if 'specialization' in doctor_df.columns:
                spec_counts = doctor_df['specialization'].value_counts()
                fig_spec = px.bar(x=spec_counts.index, y=spec_counts.values, 
                                 title="Doctor Specializations",
                                 labels={'x': 'Specialization', 'y': 'Number of Doctors'})
                fig_spec.update_xaxis(tickangle=45)
                st.plotly_chart(fig_spec, use_container_width=True)
