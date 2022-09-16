# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
import time
import requests
from flask import Flask,render_template
import folium
from folium.plugins import HeatMap
import json
from branca.colormap import LinearColormap

URL_API = ""

TYPE_MAP="Stamen Terrain"

# Flask constructor takes the name of
app = Flask(__name__)

@app.route('/')
def initial():
    points = []
    
    # Get Data from API
    #data = requests.get(URL_API)
    #messages = json.loads(data.text)
    
    # Get Data from API
    with open('testjson/data.json', 'r') as file:
        messages = json.load(file)
        print(messages)
        
    for message in messages["Items"]:
        device_id = message["payload"]["output"]["end_device_ids"]["device_id"]
        latitude = message["payload"]["output"]["payloadDecoded"]["latitude"]
        longitude = message["payload"]["output"]["payloadDecoded"]["longitude"]
        val_rssi = remap(message["payload"]["output"]["payloadDecoded"]["rssi"],-130,0,0,100)
        len_data = message["payload"]["output"]["payloadDecoded"]["leng_hexmessage"]
        # print(device_id)
        # print(latitude)
        # print(longitude)
        # print(val_rssi)
        # print(len_data)
        last_latitude = latitude
        last_longitude = longitude
        points.append([latitude,longitude,val_rssi])
    
    # Init Map
    mapObj = folium.Map(location=[last_latitude,last_longitude],zoom_start=13,tiles=TYPE_MAP, control_scale=True, prefer_canvas=True)
    
    # Add heat points
    mapData= [[x[0],x[1], (x[2])] for x in points]
    HeatMap(mapData,gradient={
        0.1: 'cyan',
        0.5: 'blue',
        0.6: 'yellow',
        1.0: 'red'
    }).add_to(mapObj)
    
    colormap = LinearColormap(["cyan", "blue", "yellow", "red"], index=[-130, -90, -60, 0], vmin=-130, vmax=0)
    # [0, 1, 2, 3] = log10([1, 10, 100, 1000])
    colormap.add_to(mapObj)

    # Finish
    mapObj.save('templates/map.html')
    return render_template('map.html')

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# main driver function
if __name__ == '__main__':
    # Clear terminal
    clear = lambda: os.system('clear')
    clear()
    
    # Init 
    app.run(debug = True,host='0.0.0.0', port=8080)

