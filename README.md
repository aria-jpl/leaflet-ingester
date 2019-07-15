# Leaflet Ingester

This module is designed to run as a Job in HySDS. It takes a displacement time series 
product and attempts to ingest it into the thredds server that supports Leaflet JS.


- `LEAFLET_SERVER`: the IP for the leaflet server (used for ssh)
- `LEAFLET_SERVER_DS_LOCATION`: location to place datasets on the server. Standard location is: "/data/ts/"
