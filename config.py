import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'healthcare_dashboard'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Streamlit configuration
STREAMLIT_CONFIG = {
    'page_title': 'Healthcare Dashboard',
    'page_icon': '🏥',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}
