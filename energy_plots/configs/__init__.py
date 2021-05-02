# This app uses classes for Flask configuration:
# https://flask.palletsprojects.com/en/1.1.x/config/#development-production

class DashConfig:
    # Flask builtin configuration variables:
    # https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values
    ENV = 'development'  # Default = production
    # DEBUG = False  # Default: True if ENV is 'development', or False otherwise.
    # TESTING = False  # Default: False
    # PROPAGATE_EXCEPTIONS = False  # Default: None. If not set, this is implicitly true if TESTING or DEBUG is enabled.

    # App title (used in for example the Navbar and page title)
    TITLE = 'Energy plots'

    # Automatic routing
    ROUTES = [
        {'name': 'Electricity', 'url': '/electricity', 'layout': 'electricity_layout'},
        {'name': 'Gas', 'url': '/gas', 'layout': 'gas_layout'}
    ]

    # Dash dev tools:
    # https://dash.plotly.com/devtools
    DEV_TOOLS = True


dash_config = DashConfig
