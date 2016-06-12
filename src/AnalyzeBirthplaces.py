import plotly.plotly as py
import plotly.graph_objs as go
import operator

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

state_count = {}
city_count = {}

# count the number of rappers from each state
for val in state.values():
    if state_count.has_key(val):
        state_count[val] += 1
    else:
        state_count[val] = 1

# count the number of rappers from each city
for val in city.values():
    if city_count.has_key(val):
        city_count[val] += 1
    else:
        city_count[val] = 1

# sort the state_count dictionary
sorted_states = sorted(state_count.items(), key=operator.itemgetter(1))

# sort the city_count dictionary
sorted_cities = sorted(city_count.items(), key=operator.itemgetter(1))

print sorted_states
print sorted_cities

states = []
state_counts = []
for idx in range(len(sorted_states)-1, -1, -1):
    states.append(sorted_states[idx][0])
    state_counts.append(sorted_states[idx][1])
cities = []
city_counts = []
for idx in range(len(sorted_cities)-1, -1, -1):
    cities.append(sorted_cities[idx][0])
    city_counts.append(sorted_cities[idx][1])


states_data = [go.Bar(x=states, y=state_counts)]
cities_data = [go.Bar(x=cities, y=city_counts)]

py.plot(states_data, filename='rappers_states')
py.plot(cities_data, filename='rappers_cities')