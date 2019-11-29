import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import requests


date1 = input('Enter date (YYYY-MM-DD) :: ')
url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={date1}'
r = requests.get(url)
print(f"Status Code {r.status_code}")
if(r.status_code == 200):
    response_dict = r.json()
    print(response_dict['metadata']['count'])

    all_eq_data = response_dict['features']

    mags, lons, lats, hover_texts = [], [], [], []
    for i in range(len(all_eq_data)):
        mag = all_eq_data[i]['properties']['mag']
        lon = all_eq_data[i]['geometry']['coordinates'][0]
        lat = all_eq_data[i]['geometry']['coordinates'][1]
        title = all_eq_data[i]['properties']['title']
        lons.append(lon)
        lats.append(lat)
        hover_texts.append(title)
        if(mag>0):
            mags.append(mag)

    print(len(mags))
    #Map The Earthquake in Graph
    data = [{
        'type': 'scattergeo',
        'lon': lons,
        'lat': lats,
        'text': hover_texts,
        'marker': {
            'size': [5*mag for mag in mags],
            'color': mags,
            'colorscale': 'Viridis',
            'reversescale': True,
            'colorbar': {'title': 'Magnitude'}
            },
        }]
    my_layout = Layout(title=f'Global Earthquakes {date1}')

    fig = {'data':data,'layout':my_layout}
    offline.plot(fig, filename="//10.212.30.30/Share Folder/Ramnish/Phython/Data Visualization/Downloading Data/earthquake.html")
else:
    print('Error No data is avilable')
