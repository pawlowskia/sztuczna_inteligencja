import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

file_paths = ['dijkstra_coords.csv', 'astar_coords.csv', 'astar_manhattan_coords.csv', 'astar_least_lines_0_1_coords.csv', 'astar_least_lines_coords.csv']
dataframes = [pd.read_csv(file) for file in file_paths]

plt.figure(figsize=(10, 8))
# m = Basemap(projection='merc', llcrnrlat=50, urcrnrlat=52, llcrnrlon=16, urcrnrlon=18, resolution='h')
m = Basemap(projection='merc', llcrnrlat=51.00, urcrnrlat=51.20, llcrnrlon=16.90, urcrnrlon=17.20, resolution='h')


colors = ['r', 'g', 'b', 'c', 'm']
for i, df in enumerate(dataframes):
    lats = df['lat'].values
    lons = df['lon'].values
    x, y = m(lons, lats)
    name = file_paths[i]
    m.plot(x, y, color=colors[i], linewidth=2, label=f'Route {name}')

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='white', lake_color='lightblue')

plt.legend()

plt.title('Routes')
plt.show()
