"""
This Dash application is structured by following mostly along the lines of the documentation of Dash:
https://dash.plotly.com/urls --> section: Structuring a Multi-Page App

The project is setup following that "each app is contained in a separate file". If we look at the "flat project layout"
we see that the callbacks and layouts are split, this is something that is done here as well, so we have a bit of both
setups. If the app is also small enough, it is unnecessary to have callbacks.py and layouts.py for each page and they
will be in the same files. The app.py in the documentation is moved to the __init__.py of the app folder, as this is
more logical than separating it in another file in the root. The same goes for the routing, which is moved from index.py
in the documentation to routes.py in the app folder. Lastly, there is one extra backend.py file, which is used to run
any code in the background parallel to the Dash app (usually this is useful for a continuous process).

Like the index.py in the documentation, this file is used to start the server.
"""

from threading import Thread

from app import app
from app.backend import main_thread

app.logger.info('Booting dashboard...')
server = app.server  # Necessary line for gunicorn

app.logger.info('Starting main thread...')
if app.server.config['ENV'] != 'development':
    t = Thread(target=main_thread, daemon=True)
    t.start()

app.logger.info('Starting server')
if __name__ == '__main__':
    app.logger.warning('Running debug server!')
    app.run_server(host="0.0.0.0", port=8099, debug=app.server.config['DEBUG'], dev_tools_hot_reload=False)
