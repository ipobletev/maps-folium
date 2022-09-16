## HEAT MAP
import folium
from folium.plugins import HeatMap
import webbrowser

TYPE_MAP="Stamen Terrain"

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

mapObj = folium.Map(location=[24.2170111233401,81.0791015625000],zoom_start=6,tiles=TYPE_MAP,control_scale=False,zoom_control =False)

data = [
    [24.399,80.142,remap(-130,-130,0,0,100)],
    [22.252,80.885,remap(-50,-130,0,0,100)],
    [23.751,79.995,remap(0,-130,0,0,100)]
]

mapData= [[x[0],x[1], (x[2])] for x in data]

#HeatMap(mapData).add_to(mapObj)
HeatMap(data=mapData,max_zoom=10,radius=10,blur=2,overlay=False,control=False,show=False,use_local_extrema=False,
    gradient={
        0.1: 'cyan',
        0.5: 'blue',
        0.6: 'yellow',
        1.0: 'red'
}).add_to(mapObj)

mapObj.save("templates/map.html")
webbrowser.open("templates/map.html")