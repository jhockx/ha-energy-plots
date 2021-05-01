import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask

from app import layouts
from configs import dash_config

# Use existing Flask server:
# https://dash.plotly.com/reference under dash.Dash server
server = Flask(__name__)
# Load from object:
# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Config.from_object
server.config.from_object(dash_config)

# Initialize dashboard:
# https://dash.plotly.com/reference under dash.Dash
app = Dash(
    name='app',
    server=server,
    external_stylesheets=[
        # Material design bootstrap theme:
        # https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
        # Example:
        # https://bootswatch.com/materia/
        dbc.themes.MATERIA,
        # Material design icons:
        # https://fonts.google.com/icons
        'https://fonts.googleapis.com/icon?family=Material+Icons'
    ]
)

# Dash dev tools:
# https://dash.plotly.com/devtools
app.enable_dev_tools(
    debug=app.server.config['DEV_TOOLS']
)

# Set title and layout
app.title = app.server.config['TITLE']
app.layout = layouts.skeleton_layout

# Import the rest after initialization of app to prevent circular imports
from app import backend, callbacks, routes
