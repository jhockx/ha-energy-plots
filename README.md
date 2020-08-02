# Home Assistant Energy Plots
This Home Assistant addon serves plots made with InfluxDB data, Pandas and Plotly for electricity, solar and gas data. Right now, the addon only plots and serves the data of the current month and current year (see sections below). These plots can easily be added to your Lovelace UI by using an iframe card. For example, add this in the code-editor:  
```
aspect_ratio: 90%
type: iframe
url: 'http://YOUR_STATIC_IP_ADDRESS:8000/electricity-current-month-static.html'
```

And replace `YOUR_STATIC_IP` with the correct IP address. This will give you the electricity usage and solar yield (if included) for the current month.

### Requirements
- First you need to setup the [InfluxDB addon](https://github.com/hassio-addons/addon-influxdb). You can find my configuration [here](https://github.com/jhockx/ha-configuration/blob/master/Data%20storage.md). It is assumed you have setup a database called `homeassistant` with an `infinite` retention policy. You need to save your data in this database *at least* daily. On the other hand, very high resolution data can potentially slow down the addon (I currently store hourly data in this database, which is working fine on a Raspberry Pi 3B). 
- To let this addon on work, you need to fill in all the settings under the `Configuration` panel after installation.

### Exmple plots
Monthly electricity:  
![Monthly electricity](assets/example_monthly_electrcity.png "Monthly electricity")


### Development notes
- *Keep a good eye on EOL settings. This should be Linux (LF) and not Windows (CRLF)! Settings can become corrupt in Home Assistant if you use CRLF.*
