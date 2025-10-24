# 🏥 Healthcare Dashboard

A comprehensive healthcare management system built with Streamlit and MySQL that manages patients, doctors, and appointments with full CRUD functionality and data visualization.

## Features

### 📊 Dashboard
- Real-time metrics and KPIs
- Recent appointments overview
- Quick access to all system data

### 👥 Patient Management
- Add, view, update, and delete patient records
- Patient demographics and medical history tracking
- Comprehensive patient information forms

### 👨‍⚕️ Doctor Management
- Doctor registration and profile management
- Specialization tracking
- Experience and contact information

### 📅 Appointment Management
- Schedule, update, and cancel appointments
- Status tracking (Scheduled, Completed, Cancelled, No Show)
- Patient-doctor matching system

### 📈 Analytics & Insights
- Appointment status distribution
- Monthly appointment trends
- Doctor workload analysis
- Common patient conditions
- Patient demographics
- Doctor specialization distribution

## Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database:**
   - Create a MySQL database named `healthcare_dashboard`
   - Update database credentials in `config.py` or create a `.env` file:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_NAME=healthcare_dashboard
   DB_PORT=3306
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Database Schema

The application automatically creates the following tables:

### Doctors Table
- `id` (Primary Key)
- `name` (VARCHAR)
- `specialization` (VARCHAR)
- `email` (VARCHAR, Unique)
- `phone` (VARCHAR)
- `experience_years` (INT)
- `created_at` (TIMESTAMP)

### Patients Table
- `id` (Primary Key)
- `name` (VARCHAR)
- `age` (INT)
- `gender` (ENUM: Male, Female, Other)
- `email` (VARCHAR, Unique)
- `phone` (VARCHAR)
- `address` (TEXT)
- `medical_history` (TEXT)
- `created_at` (TIMESTAMP)

### Appointments Table
- `id` (Primary Key)
- `patient_id` (Foreign Key)
- `doctor_id` (Foreign Key)
- `appointment_date` (DATE)
- `appointment_time` (TIME)
- `status` (ENUM: Scheduled, Completed, Cancelled, No Show)
- `condition_description` (TEXT)
- `notes` (TEXT)
- `created_at` (TIMESTAMP)

## Usage

### Getting Started
1. **Add Doctors:** Navigate to the Doctors section and add doctor profiles
2. **Add Patients:** Navigate to the Patients section and register patients
3. **Schedule Appointments:** Use the Appointments section to book patient-doctor meetings
4. **View Analytics:** Check the Analytics section for insights and trends

### Navigation
- **Dashboard:** Overview of the system with key metrics
- **Patients:** Manage patient records and information
- **Doctors:** Manage doctor profiles and specializations
- **Appointments:** Schedule and manage appointments
- **Analytics:** View data insights and visualizations

## Features Overview

### CRUD Operations
- **Create:** Add new patients, doctors, and appointments
- **Read:** View all records with detailed information
- **Update:** Modify existing records
- **Delete:** Remove records from the system

### Data Visualization
- **Pie Charts:** Appointment status distribution
- **Line Charts:** Monthly appointment trends
- **Bar Charts:** Doctor workload and condition statistics
- **Histograms:** Patient age distribution
- **Interactive Charts:** Powered by Plotly

### Data Insights
- Appointment trends over time
- Doctor workload analysis
- Common patient conditions
- Patient demographics
- Specialization distribution

## Configuration

### Database Configuration
Update the database settings in `config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'healthcare_dashboard',
    'port': 3306
}
```

### Environment Variables
Create a `.env` file for secure configuration:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=healthcare_dashboard
DB_PORT=3306
```

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Verify MySQL server is running
   - Check database credentials
   - Ensure the database exists

2. **Import Errors:**
   - Install all required packages: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Port Already in Use:**
   - Streamlit runs on port 8501 by default
   - Use `streamlit run app.py --server.port 8502` to use a different port

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions, please create an issue in the repository or contact the development team.
