import webbrowser
import geopandas as gpd
from pyproj import CRS
import requests
import geojson
import folium

# # Specify the url for web feature service
# URL_API = "https://rcg9tjimie.execute-api.us-west-2.amazonaws.com/items"

# url = URL_API

# # Specify parameters (read data in json format).
# # Available feature types in this particular data source: http://geo.stat.fi/geoserver/vaestoruutu/wfs?service=wfs&version=2.0.0&request=describeFeatureType
# params = dict(service='WFS',
#               version='2.0.0',
#               request='GetFeature',
#               typeName='asuminen_ja_maankaytto:Vaestotietoruudukko_2020',
#               outputFormat='json')

# # Fetch data from WFS using requests
# r = requests.get(url, params=params)
# print(r.content)
# Create GeoDataFrame from geojson
asdas = '''
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Point",
        "coordinates": [
          -70.83984375,
          -28.270520445825404
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -70.8453369140625,
              -28.022287762597117
            ],
            [
              -70.83572387695312,
              -28.022287762597117
            ],
            [
              -70.83572387695312,
              -28.017438480944215
            ],
            [
              -70.8453369140625,
              -28.017438480944215
            ],
            [
              -70.8453369140625,
              -28.022287762597117
            ]
          ]
        ]
      }
    }
  ]
}
'''
data = gpd.GeoDataFrame.from_features(geojson.loads(asdas))
# Clean overall cell
data = data[data['index'] != 27699]
# Check the data
data.head()

# Create a Map instance
m = folium.Map(location=[60.25, 24.8], tiles = 'cartodbpositron', zoom_start=10, control_scale=True)

# Plot a choropleth map
# Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
folium.Choropleth(
    geo_data=data,
    name='Population in 2020',
    data=data,
    columns=['geoid', 'pop20'],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    line_color='white', 
    line_weight=0,
    highlight=False, 
    smooth_factor=1.0,
    #threshold_scale=[100, 250, 500, 1000, 2000],
    legend_name= 'Population in Helsinki').add_to(m)

m.save("src/templates/map.html")
webbrowser.open("src/templates/map.html")