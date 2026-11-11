# Main Application entry point
# For the Animal Shelter Dashboard
# Connects the Database, Layout, and Callback Modules

from dash import Dash, html, Input, Output, State
from CRUD import AnimalShelter
from layout import create_layout
from login import create_login_layout
from dashboard_callbacks import register_callbacks
import pandas as pd
from app.venv.logging_config import setup_logging
import logging

logging.getLogger("werkzeug").setLevel(logging.ERROR)

# Temporary login credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

USER_USERNAME = "user"
USER_PASSWORD = "user123"

shelter = AnimalShelter()

# Load initial DB records
df = pd.DataFrame.from_records(
    shelter.getRecordCriteria({})
)

# Create Dash application
app = Dash(__name__,
    suppress_callback_exceptions=True)

# Create dashboard layout
app.layout = html.Div(
    id="page-content",
    children=create_login_layout(app)
)
@app.callback(
    Output("page-content", "children"),
    Input("login-button", "n_clicks"),
    Input("login-username", "n_submit"),
    Input("login-password", "n_submit"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(button_clicks, username_enter, password_enter,
                 username, password):

    if not username or not password:
        return create_login_layout(app, "Please enter both username and password.")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return create_layout(df)

    elif username == USER_USERNAME and password == USER_PASSWORD:
        return create_layout(df)

    else:
        return create_login_layout(app, "Invalid username or password.")


# Register dashboard callbacks
register_callbacks(app, shelter)

# Start application
if __name__ == "__main__":
   app.run(debug=False,use_reloader=False)