print('Start influx script')

import plotly.graph_objs as go
from influxdb import DataFrameClient

# Influxdb settings
host = ''
port = 8086
username = ''
password = ''

# Pandas DataFrame results
client = DataFrameClient(host=host, port=port, username=username, password=password)

result = client.query('SELECT * FROM "homeassistant"."infinite"."kWh"')
df = result['kWh']
total_yield = df[df['entity_id'] == 'total_yield'].sort_index()

# Build traces
trace1 = go.Scatter(y=total_yield['value'])

# Plotly build figure
data = [trace1]
layout = {"margin": dict(l=0, r=0, t=0, b=0)}
fig = go.Figure(data=data, layout=layout)
fig.write_html("./test.html", config={'staticPlot': True})

print('End influx script')
