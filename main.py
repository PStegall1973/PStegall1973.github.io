# Main Application entry point
# For the Animal Shelter Dashboard
# Connects the Database, Layout, and Callback Modules

from dash import Dash
from CRUD import AnimalShelter
from layout import create_layout
from dashboard_callbacks import register_callbacks
import pandas as pd
from logging_config import setup_logging

setup_logging()
# Database connection
username = "aacuser"
password = "abc123"

shelter = AnimalShelter(username, password)

# Load initial DB records
df = pd.DataFrame.from_records(
    shelter.getRecordCriteria({})
)

# Create Dash application
app = Dash(__name__)

# Create dashboard layout
app.layout = create_layout(df)

# Register dashboard callbacks
register_callbacks(app, shelter)

# Start application
if __name__ == "__main__":
   app.run(debug=False,use_reloader=False)