import plotly.plotly as py
import plotly.graph_objs as go
import operator

# read in birthplaces text file and input information into birthplace dictionary
birthplace = {}

with open("birthplaces_final.txt") as f:
    idx = 0
    artist = ''
    for line in f:
        if idx % 2 == 0:
            artist = line[:len(line)-1]
        else:
            birthplace[artist] = line[:len(line)-1].split(',')
        idx += 1

# set up state and city dictionaries (keys are rapper names)
state = {}
city = {}
for key in birthplace.keys():
    loc = birthplace[key]
    state[key] = loc[len(loc) - 2]
    if state[key][0] == ' ':
        state[key] = state[key][1:len(state[key])]
    city[key] = loc[len(loc) - 3]
    if city[key][0] == ' ':
        city[key] = city[key][1:len(city[key])]

# count the number of rappers from each state
state_count = {}

for val in state.values():
    if state_count.has_key(val):
        state_count[val] += 1
    else:
        state_count[val] = 1

# count the number of rappers from each city
city_count = {}

for val in city.values():
    if city_count.has_key(val):
        city_count[val] += 1
    else:
        city_count[val] = 1

# dictionary of rappers by city
rappers_by_city = {}
for key in city.keys():
    fixed_key = key
    if key[len(key)-9:] == ' (rapper)':
        fixed_key = key[:len(key)-9]
    if rappers_by_city.has_key(city[key]):
        rappers_by_city[city[key]].append(fixed_key)
    else:
        rappers_by_city[city[key]] = [fixed_key]

# sort the state_count dictionary
sorted_states = sorted(state_count.items(), key=operator.itemgetter(1))

# sort the city_count dictionary
sorted_cities = sorted(city_count.items(), key=operator.itemgetter(1))

# set up sorted state and city lists
sorted_states = []
state_sorted_counts = []
for idx in range(len(sorted_states)-1, -1, -1):
    sorted_states.append(sorted_states[idx][0])
    state_sorted_counts.append(sorted_states[idx][1])
sorted_cities = []
city_sorted_counts = []
for idx in range(len(sorted_cities)-1, -1, -1):
    sorted_cities.append(sorted_cities[idx][0])
    city_sorted_counts.append(sorted_cities[idx][1])

# plot bar graphs of number of rappers per state/city
states_data = [go.Bar(x=sorted_states, y=state_sorted_counts)]
cities_data = [go.Bar(x=sorted_cities, y=city_sorted_counts)]

# py.plot(states_data, filename='rappers_states')
# py.plot(cities_data, filename='rappers_cities')

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/ap

import plotly.plotly as py
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
df.head()
name = []
num = []
lat = []
lon = []
rappers_list = []

for idx in range(0, len(df['name'])):
    city_name = df['name'][idx]
    city_name = city_name[:len(city_name) - 1]
    if city_name == 'New York':
        city_name = 'New York City'
    if city_name in city_count:
        name.append(df['name'][idx])
        num.append(city_count[city_name])
        lat.append(df['lat'][idx])
        lon.append(df['lon'][idx])
        rappers_string = ''
        count = 0
        for rapper in rappers_by_city[city_name]:
            count += 1
            if count % 5 == 0:
                rappers_string += '<br>'
            rappers_string = rappers_string + ', ' + rapper
        rappers_string = rappers_string[2:]
        rappers_list.append(rappers_string)

df_new = pd.DataFrame({'name': name, 'num': num, 'lat': lat, 'lon': lon, 'rappers_list': rappers_list})

print df_new.head()

df_new['text'] = df_new['name'] + '<br><b>Count:</b> ' + df_new['num'].astype(str) + '<br>' + df_new['rappers_list'].astype(str)
limits = [(0,2),(3,10),(11,50),(51,100),(101,200)]
# limits = [(10,20),(5,10),(3,5),(2,3),(0,1)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
cities = []
scale = 0.005

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df_new[lim[0]:lim[1]]
    city = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['num']/scale,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]) )
    cities.append(city)

layout = dict(
        title = 'Origins of Top 200 Rappers<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=cities, layout=layout )
url = py.plot( fig, validate=False, filename='d3-bubble-map-populations' )