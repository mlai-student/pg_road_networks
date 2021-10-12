import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
from descartes import PolygonPatch

from osmnx.distance import nearest_nodes
from osmnx.plot import get_colors


def main():
    place = 'Bonn'
    network_type = 'all'
    trip_times = [5, 10, 15, 20, 25]  # in minutes
    travel_speed = 5  # walking speed in km/hour
    # download the street network
    G = ox.graph_from_place(place, network_type=network_type)
    stats = ox.basic_stats(G)
    print(stats)

    # find the centermost node and then project the graph to UTM
    gdf_nodes = ox.graph_to_gdfs(G, edges=False)
    x, y = gdf_nodes["geometry"].unary_union.centroid.xy
    center_node = ox.distance.nearest_nodes(G, x[0], y[0])
    G = ox.project_graph(G)

    # add an edge attribute for time in minutes required to traverse each edge
    meters_per_minute = travel_speed * 1000 / 60  # km per hour to m per minute
    for _, _, _, data in G.edges(data=True, keys=True):
        data["time"] = data["length"] / meters_per_minute

    # get one color for each isochrone
    iso_colors = ox.plot.get_colors(n=len(trip_times), cmap="Reds", start=0, return_hex=True)

    def make_iso_polys(G, edge_buff=25, node_buff=50, infill=False):
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

    isochrone_polys = make_iso_polys(G, edge_buff=25, node_buff=0, infill=True)
    fig, ax = ox.plot_graph(
        G, show=False, close=False, edge_color="#999999", edge_alpha=0.2, node_size=0
    )
    for polygon, fc in zip(isochrone_polys, iso_colors):
        patch = PolygonPatch(polygon, fc=fc, ec="none", alpha=0.7, zorder=-1)
        ax.add_patch(patch)
    plt.show()


if __name__ == '__main__':
    main()
