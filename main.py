import time

import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
from descartes import PolygonPatch

from osmnx.distance import nearest_nodes
from osmnx.plot import get_colors


def make_iso_polys(G, trip_times, center_node, edge_buff=25, node_buff=50, infill=False):
    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance="time")

        node_points = [Point((data["x"], data["y"])) for node, data in subgraph.nodes(data=True)]
        nodes_gdf = gpd.GeoDataFrame({"id": list(subgraph.nodes)}, geometry=node_points)
        nodes_gdf = nodes_gdf.set_index("id")

        edge_lines = []
        for n_fr, n_to in subgraph.edges():
            f = nodes_gdf.loc[n_fr].geometry
            t = nodes_gdf.loc[n_to].geometry
            edge_lookup = G.get_edge_data(n_fr, n_to)[0].get("geometry", LineString([f, t]))
            edge_lines.append(edge_lookup)

        n = nodes_gdf.buffer(node_buff).geometry
        e = gpd.GeoSeries(edge_lines).buffer(edge_buff).geometry
        all_gs = list(n) + list(e)
        new_iso = gpd.GeoSeries(all_gs).unary_union

        # try to fill in surrounded areas so shapes will appear solid and
        # blocks without white space inside them
        if infill:
            new_iso = Polygon(new_iso.exterior)
        isochrone_polys.append(new_iso)
    return isochrone_polys


def main():
    place = 'Bonn'
    network_type = 'drive'
    time_bounds = (2, 40, 2)  # min, max, step
    travel_speed = 20  # walking speed in km/hour
    trip_times = [x / 100 for x in
                  range(int(time_bounds[0] * 100), int(time_bounds[1] * 100) + int(time_bounds[2] * 100),
                        int(time_bounds[2] * 100))]  # in minutes
    # download the street network
    start = time.time()
    G = ox.graph_from_place(place, network_type=network_type)
    print(f'Load graph: {time.time() - start}s')
    stats = ox.basic_stats(G)
    print(stats)

    # find the centermost node and then project the graph to UTM
    start = time.time()
    gdf_nodes = ox.graph_to_gdfs(G, edges=False)
    x, y = gdf_nodes["geometry"].unary_union.centroid.xy
    center_node = ox.distance.nearest_nodes(G, x[0], y[0])
    G = ox.project_graph(G)
    print(f'\tGet center: {time.time() - start}s')

    # add an edge attribute for time in minutes required to traverse each edge
    meters_per_minute = travel_speed * 1000 / 60  # km per hour to m per minute
    for _, _, _, data in G.edges(data=True, keys=True):
        data["time"] = data["length"] / meters_per_minute
    print(f'\tGet edge length data: {time.time() - start}s')

    start = time.time()
    # get one color for each isochrone
    iso_colors = ox.plot.get_colors(n=len(trip_times), cmap="YlOrRd", start=0, return_hex=True)
    print(f'\tGet Iso colors: {time.time() - start}s')
    sub = time.time()
    fig, ax = ox.plot_graph(G, bgcolor="#ffffff", show=False, close=False, edge_color="#000000", edge_alpha=0.5,
                            node_size=0)
    print(f'\tPlot graph: {time.time() - sub}s')
    sub = time.time()
    isochrone_polys = make_iso_polys(G, trip_times=trip_times, center_node=center_node, edge_buff=25, node_buff=0,
                                     infill=True)
    print(f'\tGet iso polys: {time.time() - sub}s')
    sub = time.time()
    for polygon, fc in zip(isochrone_polys, iso_colors):
        patch = PolygonPatch(polygon, fc=fc, ec="none", alpha=0.7, zorder=-1)
        ax.add_patch(patch)
    print(f'\tGet polygons: {time.time() - sub}s')
    plt.show()
    print(f'Draw graph: {time.time() - start}s')


if __name__ == '__main__':
    main()
