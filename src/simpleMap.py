import folium
import webbrowser
COORDS = [-23.670707290132345, -70.40797805575579]


# Types of visual maps
# "Stamen Terrain", "Stamen Toner"
TYPE_MAP="Stamen Terrain"

class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
    
    def showMap(self):
        #Create the map
        my_map = folium.Map(location = self.center, zoom_start = self.zoom_start,tiles=TYPE_MAP)
        
        #Add a marker
        tooltip = "Click me!"
        folium.Marker(
            COORDS, popup="<b>Timberline Lodge</b>", tooltip=tooltip
        ).add_to(my_map)
        
        #Display the map
        my_map.save("src/templates/map.html")
        webbrowser.open("src/templates/map.html")

#Define coordinates of where we want to center our map
map = Map(center = COORDS, zoom_start = 15)
map.showMap()