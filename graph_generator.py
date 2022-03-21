#!/usr/bin/env python
"""
Stellt die Funktionalitaet zum Herunterladen, Generieren und Labeln der Graphen bereit.
"""

import os
import re
import time
from random import randint
from typing import List, Tuple
from pathlib import Path
import networkx as nx
import osmnx as ox
import pandas as pd
import geopandas as gp
import numpy as np
import queue
import pickle

import graph_statistics
import save_graph
import save_graph as sg

import util

ox.config(use_cache=True, log_console=True)


def yield_from_download(places):
    for i in range(len(places)):
        city, country = places[i]
        try:
            G = ox.graph_from_place(f'{city}, {country}', network_type='all')

            # Setze Graph Attribute
            G.graph['graph_label'] = [city, country]
            # G.graph['country'] = country
            # G.graph['city'] = city
            G.graph['graphname'] = city.strip().replace(" ", "-")+"_"+country.strip().replace(" ", "-")
            yield G
        except ValueError:
            util.write_log(f'Graph from {city}, {country} could not be downloaded.')
            yield None


def stringified_to_list_int(x: str):
    """
    Stringified array zu Liste von int
    :param label_vec:
    :return:
    """
    return [int(val) for val in x.replace("'", '').replace('[', '')
            .replace(']', '').replace('"', '').strip().split(',')]


def yield_from_generate(files, genSource):
    for f in files:
        G = None
        try:
            extension = f.split(".")[-1]
            name = f.split(".")[0]

            if extension == 'graphml':
                G = ox.load_graphml(f'{genSource}/{f}', node_dtypes={'label_vec':lambda x: stringified_to_list_int(x)})

                # 'Stringified' Attribute muessen zurueck konvertiert werden, falls graph_label vorhanden
                if 'graph_label' in G.graph:
                    label_vec_strings = G.graph['graph_label'].replace('[', "").replace(']', "").replace("'", "").replace('"', "").split(',')
                    G.graph['graph_label'] = [label_vec_strings[0].strip(), label_vec_strings[1].strip()]

            elif extension == 'pickle' :
                with open(f'{genSource}/{f}', 'rb') as gfile:
                    G = pickle.load(gfile)
            elif extension == 'etgf':
                G = sg.graph_from_etgf(f'{genSource}/{f}')
            else:
                util.write_log(f'Unsuppported file format {extension}. File: {name}.{extension}.\n')

            # Attribut graph_label muss in den Attributen vorhanden sein
            if G is not None and 'graph_label' not in G.graph:
                G = None
                util.write_log(f"Graph in File {name}.{extension} is missing attribute: 'graph_label'\n")

            if G is not None:
                G.graph['graphname'] = name

            yield G

        except IOError:
            yield G


def run_program(download, download_mode, num_cities, input_cities, download_file, generate, gen_mode, gen_source,  num_graphs, num_edges, num_nodes,
                gen_by_nodes, radius, bbwidth, bbheight, label, label_source, label_euclidean, label_binary, input_amenities, save_download, format_download,
                save_generate, format_generate, save_label, format_label, save_path, use_percentage, percentage):

    # Liste mit amenities, wird nachher gefuellt
    amenities = []

    # Noetige Ordner für das Speichern erstellen
    main_directory = save_graph.gen_save_dirs(save_path, download, save_download, generate, save_generate, label)
    main_path = os.path.join(save_path, main_directory)
    util.log_file_path = main_path + '/log.txt'

    # Amenities vorbereiten
    if label:
        # Alle Whitespaces aus den eingegeben Amenities entfernen+Mögliches Komma am Ende entfernen
        input_amenities = input_amenities.replace(" ", "").rstrip(',')
        if re.fullmatch(r"([^\d\W]+)(,|(,[^\d\W]+)*)", input_amenities):
            amenities = input_amenities.split(',')
        else:
            raise ValueError('Amenities in wrong format. Correct: amenity1,amenity2,...')
        # Label-Modus in validen Input für label_graph() konvertieren
        if label_euclidean:
            label_mode = "euclidian_dist"
        else:
            label_mode = "nearest_edge"

    # Speichert die Berechneten Statistiken [einzeln, pro Stadt, insgesamt] zwischen
    list_of_stats = [[], [], []]
    stats_total = graph_statistics.StatAccumulator('average_all', len(amenities))

    # Download
    if download:
        # Bei downloadMode = 0 werden zufällige Städte verwendet.
        if download_mode == 0:
            places = random_places(num_cities)
        # Bei downloadMode = 1 werden Städtenamen aus dem Input-Textfeld in der GUI erstellt.
        elif download_mode == 1:
            input_cities = input_cities.rstrip(";")
            if re.fullmatch(r"([ ]*\w(\w|[ ])*,[ ]*\w(\w|[ ])*)(;([ ]*\w(\w|[ ])*,[ ]*\w(\w|[ ])*))*", input_cities, re.U):
                s = input_cities.split(";")
                places = [tuple(x.split(',')) for x in s]
                # Leerzeichen am Rand entfernen
                for i in range(len(places)):
                    places[i] = (places[i][0].strip(), places[i][1].strip())
            else:
                raise ValueError('Cities in wrong format. Correct: city,country;city,country;...')
        # Bei downloadMode = 2 werden Städte aus einer Datei eingelesen.
        elif download_mode == 2:
            places = parse_places(download_file)
        # Duplikate entfernen(Zweimal dieselbe Stadt herunterzuladen ist unsinnig)
        places = list(dict.fromkeys(places))

        graph_provider = yield_from_download(places)
    # Kein Download
    elif generate:
        os.chdir(gen_source)
        files = []
        for f in os.listdir():
            if not os.path.isdir(gen_source+"/"+f):
                files.append(f)
        graph_provider = yield_from_generate(files, gen_source)
    # Nur Labeln
    elif label:
        os.chdir(label_source)
        files = []
        for f in os.listdir():
            if not os.path.isdir(label_source + "/" + f):
                files.append(f)
        graph_provider = yield_from_generate(files, label_source)

        global_count = 0
        for G in graph_provider:
            if G is None:
                continue

            stats_city = graph_statistics.StatAccumulator('average_'+G.graph['graphname'], len(amenities))

            # Falls der eingegebene Graph projiziert ist, projiziere ihn erst zurueck um die Amenities runterladen zu koennen
            if ox.projection.is_projected(G.graph['crs']):
                G_unproj = ox.project_graph(G, 'epsg:4326')
                G.graph['bbox_before_projected'] = bounding_box_from_graph(G_unproj)
                amenities_result = download_amenities(G_unproj, amenities)
            else:
                amenities_result = download_amenities(G, amenities)

            label_graph(G, amenities, amenities_result, 100, label_mode, label_binary)

            # Entferne hinzugefuegtes Attribut
            if 'bbox_before_projected' in G.graph:
                del G.graph['bbox_before_projected']

            if save_label:
                save_graph.try_save_graph(G, main_path, "label", format_label, 0, 0, generate)

                current_stats = graph_statistics.calculate_stats(G, G.graph['graphname'], len(amenities))
                stats_city.increment_stats(current_stats)
                stats_total.increment_stats(current_stats)
                list_of_stats[0].append(current_stats)

            global_count = global_count+1
            list_of_stats[1].append(stats_city)

        list_of_stats[2].append(stats_total)
        graph_statistics.write_stats(list_of_stats, main_path, len(amenities))
        return


    global_count = 0
    for G in graph_provider:
        if G is None:
            continue

        stats_city = graph_statistics.StatAccumulator('average_'+G.graph['graphname'], len(amenities))

        local_count = 0

        # Versuche, den aktuell heruntergeladenen Graphen zu speichern
        if download & save_download:

            save_graph.try_save_graph(G, main_path, "download", format_download, 0, 0, generate)
            if not (generate or label):
                current_stats = graph_statistics.calculate_stats(G, G.graph['graphname'], 0)
                stats_city.increment_stats(current_stats)
                stats_total.increment_stats(current_stats)
                list_of_stats[0].append(current_stats)



        # Projiziere Graph nur, falls noch nicht projiziert
        if not ox.projection.is_projected(G.graph['crs']):
            G_proj = ox.project_graph(G)
        else:
            G_proj = G


        if label:
            # Projiziere Graph nur, falls noch nicht projiziert
            if ox.projection.is_projected(G.graph['crs']):
                G_unproj = ox.project_graph(G, 'epsg:4326')
            else:
                G_unproj = G
            amenities_result = download_amenities(G_unproj, amenities)



        # Download->Label
        if not generate:
            if label:
                points = map_node_coords(G_unproj, G)
                G.graph['bbox_before_projected'] = bounding_box_from_points(points=points)

                label_graph(G, amenities, amenities_result, 100, label_mode, label_binary)
                if save_label:
                    # Entferne hinzugefuegtes Attribut
                    del G.graph['bbox_before_projected']

                    # Versuche, den gelabelten Graphen zu speichern
                    save_graph.try_save_graph(G, main_path, "label", format_label, 0, 0, generate)
                    current_stats = graph_statistics.calculate_stats(G, G.graph['graphname'], len(amenities))
                    stats_city.increment_stats(current_stats)
                    stats_total.increment_stats(current_stats)
                    list_of_stats[0].append(current_stats)
        # Generate
        else:

            for i in range(num_graphs):
                # Wird für Modi 0 und 1 benötigt, damit entweder nodes oder edges der limitierende Parameter bei
                # der Graph-Generierung ist.
                if gen_by_nodes:
                    num_edges = len(G.edges)
                    if use_percentage:
                        num_nodes = int((float(percentage)/100.0)*float(len(G.nodes)))

                else:
                    num_nodes = len(G.nodes)
                    if use_percentage:
                        num_edges = int((float(percentage)/100.0)*float(len(G.edges)))

                # Generiere einen neuen Graph im ausgewählten Modus
                if gen_mode == 0:
                    generated_graph = generate_graph(G_proj, num_nodes, num_edges)
                elif gen_mode == 1:
                    generated_graph = generate_graph_compact(G_proj, num_nodes, num_edges)
                elif gen_mode == 2:
                    generated_graph = generate_graph_radius(G_proj, len(G.nodes), len(G.edges), radius)
                else:
                    generated_graph = generate_graph_bbox(G_proj, len(G.nodes), len(G.edges), bbwidth, bbheight)
                if save_generate:
                    save_graph.try_save_graph(generated_graph, main_path, "generate", format_generate, global_count, local_count, generate)
                    if not label:
                        current_stats = graph_statistics.calculate_stats(generated_graph, str(global_count)+"_"+generated_graph.graph['graphname']+"_"+str(local_count), 0)
                        stats_city.increment_stats(current_stats)
                        stats_total.increment_stats(current_stats)
                        list_of_stats[0].append(current_stats)

                # Generate->Label
                if label:
                    points = map_node_coords(G_unproj, generated_graph)
                    generated_graph.graph['bbox_before_projected'] = bounding_box_from_points(
                        points=points)
                    label_graph(generated_graph, amenities, amenities_result, 100, label_mode, label_binary)
                    if save_label:
                        # Entferne hinzugefuegtes Attribut
                        del generated_graph.graph['bbox_before_projected']

                        save_graph.try_save_graph(generated_graph, main_path, "label", format_label,global_count,local_count,generate)

                        # Berechne Statistiken und inkrementiere die Durchschnittlichen
                        current_stats = graph_statistics.calculate_stats(generated_graph, str(global_count)+"_"+generated_graph.graph['graphname']+"_"+str(local_count), len(amenities))
                        stats_city.increment_stats(current_stats)
                        stats_total.increment_stats(current_stats)
                        list_of_stats[0].append(current_stats)

                local_count=local_count+1
                global_count=global_count+1

            list_of_stats[1].append(stats_city)


        if len(list_of_stats[0]) != 0:
            list_of_stats[2].append(stats_total)

    if len(list_of_stats[0]) != 0:
        graph_statistics.write_stats(list_of_stats, main_path, len(amenities))
    else:
        with open(f'{main_path}/statistics.txt', 'w') as f:
            f.write('No statistics were calculated. This may be because all downloads failed! Sorry :(')


def map_node_coords(G_to: nx.MultiDiGraph, G_from: nx.MultiGraph):
    """
    Mapt die Knoten von G_from zu G_to und gibt die zu G_to gehoerenden Koordinaten wieder.
    Achtung, wenn die Knoten der Graphen nicht uebereinstimmen, gibt es einen Fehler.
    :param G_to:
    :param G_from:
    :return:
    """
    points = []
    for node in G_from.nodes:
        points.append((G_to.nodes[node]['x'], G_to.nodes[node]['y']))
    return points


def download_amenities(G: nx.MultiDiGraph, amenities):
    """
    Laedt alle Punkte, innerhalb der BoundingBox um G, dessen amenity Attribut in amenities enthalten ist herunter
    :param G:
    :param amenities:
    :return:
    """

    bbox = bounding_box_from_graph(G)
    result_graph_complete = ox.geometries_from_bbox(bbox[2], bbox[0], bbox[3], bbox[1], tags={'amenity': amenities})
    result_graph_complete.reset_index(inplace=True)
    # Falls keine 'element_type' Spalte vorhanden, gib leeren Dataframe zurueck
    if 'element_type' not in result_graph_complete:
        return gp.GeoDataFrame(data=None, columns=['element_type', 'amenity'])

    # Filter alle Spalten, die als 'element_type' node als Eintrag haben
    mask = result_graph_complete['element_type'] == 'node'
    pos = np.flatnonzero(mask)
    result_graph_complete = result_graph_complete.iloc[pos]
    return result_graph_complete

def parse_places(filename: str):
    """
    Reads a csvfile of places and saves the entries in a dictionary which holds a list of entries(cities)
    for each country
    :param filename: input file path
    :return:
    """
    with open(filename, encoding="utf8") as csvfile:
        pattern = re.compile(r"[ ]*\w(\w|[ ])*(,[ ]*\w(\w|[ ])*)", re.U)
        lines = csvfile.readlines()
    places = []
    for line in lines:
        line = line.strip('\n')

        if not re.fullmatch(pattern, line):
            util.write_log(f'Malformed line in cities input file {filename}: {line}     Continuing with next line.\n')
        else:
            [city, country] = line.split(',')
            places.append((city, country))
    return places


def download_graphs_random(num_cities: int, num_graphs: int, num_nodes: int = -1, num_edges: int = -1):
    """
    Lost uniform zufaellig num_cities viele Staedte aus. Diese werden dann heruntergeladen und fuer jede Stadt werden
    num_graphs viele Graphen erzeugt. Die einzelnen Graphen werden im GraphML Format abgespeichert.
    :param num_cities (int):    Anzahl zufaellig ausgewaehlter Staedte
    :param num_graphs (int):    Anzahl pro Stadt generierter Graphen
    :param places:              Datenstruktur mit Laendern und Staedten aus denen ausgewaehlt wird
    :return:
    """
    cities_cleaned = pd.read_csv("cities_cleaned.csv").to_dict('records')

    for i in range(num_cities):
        G = None
        while not G:
            # Lose Stadt zufaellig aus
            sample = cities_cleaned[randint(0, len(cities_cleaned()))]

            # Versuche Graph herunterzuladen
            try :
                G = ox.graph_from_place(f'{sample["city_ascii"]}, {sample["iso2"]}')

                # Setze Graph Attribute
                G.graph['graph_label'] = [sample['city'], sample['country']]

                # Generiere num_graphs viele Graphen aus G
                for j in range(num_graphs):
                    num_nodes = G.number_of_nodes() if num_nodes == -1 else num_nodes
                    num_edges = len(G.edges()) if num_edges == -1 else num_edges

                    new_graph = generate_graph(G, num_nodes, num_edges)
                    ox.save_graphml(new_graph, f'graphs/{sample["country"]}_{sample["city_ascii"]}_{j}.graphml', encoding='utf8')

            except ValueError:
                print(f'Das Sample {sample} konnte nicht heruntergeladen werden. Wähle neues Sample aus.')


def generate_graph(G: nx.MultiDiGraph, num_nodes: int, num_edges: int):
    """
    Generiert einen neuen networkx.MultiDiGraph auf Grundlage eines gegebenen networkx.MultiDiGraph.
    Dabei wird an einem zufaelligen Knoten angefangen und durch Breitensuche der neuen Graph erweitert, solange,
    bis entweder alle Knoten im neuen Graphen enthalten sind, oder min{num_nodes, num_edges} erreicht wurde.

    :param G (networkx.Multidigraph):      Graph, aus welchem der neue Graph erzeugt werden soll
    :param num_nodes (int):                Maximale Anzahl an Knoten im neuen Graph
    :param num_edges (int):                Maximale Anzahl an Kanten im neuen Graph
    :return networkx.MultiDiGraph:         Generierter Graph
    """

    if G.number_of_nodes() == 0:
        raise ValueError('G has no nodes.')

    if num_nodes == 0:
        return nx.MultiDiGraph()

    # Setze alle Knoten auf nicht markiert
    status = dict.fromkeys(G.nodes, 0)

    # Erstelle leeren Graphen
    new_graph = nx.MultiDiGraph(**G.graph)

    q = queue.SimpleQueue()
    count_nodes = 1
    count_edges = 0

    start = list(G.nodes)[randint(0, G.number_of_nodes()-1)]
    q.put(start)
    status[start] = 1

    new_graph.add_node(start, **G.nodes[start])

    while not q.empty():
        current = q.get()

        # Betrachte alle aus-/eingehenden Kanten
        for neighbor in set(nx.all_neighbors(G, current)):

            # Nachbar noch nicht betrachtet und die Anzahl an Knoten wurde noch nicht erreicht
            if status[neighbor] == 0 and count_nodes < num_nodes:
                q.put(neighbor)
                count_nodes += 1

                new_graph.add_node(neighbor, **G.nodes[neighbor])

                # Knoten in Queue aber noch nicht komplett abgearbeitet
                status[neighbor] = 1

            # Nachbar abgearbeitet oder Anzahl an Knoten erreicht
            if not status[neighbor] == 1:
                continue

            # Fuege alle Kanten zwischen current und neighbor in den Graph ein
            from_node = current
            to_node = neighbor

            for i in range(2):
                if G.has_successor(from_node, to_node):
                    # Schleife fuer Mehrfachkanten
                    for j in range(len(G[from_node][to_node])):
                        new_graph.add_edge(from_node, to_node, **G[from_node][to_node][j])
                        count_edges += 1

                        if count_edges == num_edges:
                            return new_graph

                if from_node == to_node:
                    break

                # Wechsle zu eingehenden Kanten
                from_node, to_node = to_node, from_node

        # Kanten abgearbeitet
        status[current] = 2

    return new_graph


def generate_graph_compact(G: nx.MultiDiGraph, num_nodes: int, num_edges: int):
    """
    Generiert einen neuen networkx.MultiDiGraph auf Grundlage eines gegebenen networkx.MultiDiGraph.
    Dabei wird an einem zufaelligen Knoten angefangen und durch Breitensuche der neuen Graph erweitert, solange,
    bis entweder alle Knoten im neuen Graphen enthalten sind, oder min{num_nodes, num_edges} erreicht wurde.

    Zusaetzlich wird der Graph möglichst Kompakt um den zufällig ausgewählten Knoten erstellt.
    Kompakt bedeutet hier, dass immer der Knoten aus der Priority Queue mit der kleinsten euklidischen
    Distanz zum Startpunkt expandiert wird.

    :param G (networkx.Multidigraph):      Graph, aus welchem der neue Graph erzeugt werden soll
    :param num_nodes (int):                Maximale Anzahl an Knoten im neuen Graph
    :param num_edges (int):                Maximale Anzahl an Kanten im neuen Graph
    :return networkx.MultiDiGraph:         Generierter Graph
    """

    if G.number_of_nodes() == 0:
        raise ValueError('G has no nodes.')

    if num_nodes == 0:
        return nx.MultiDiGraph()

    # Setze alle Knoten auf nicht markiert
    status = dict.fromkeys(G.nodes, 0)

    # Erstelle leeren Graphen
    new_graph = nx.MultiDiGraph(**G.graph)

    q = queue.PriorityQueue()
    count_nodes = 1
    count_edges = 0

    start = list(G.nodes)[randint(0, G.number_of_nodes()-1)]
    q.put((0, start))
    status[start] = 1

    center = (G.nodes[start]['x'], G.nodes[start]['y'])

    new_graph.add_node(start, **G.nodes[start])

    while not q.empty():
        current = q.get()

        # Betrachte alle aus-/eingehenden Kanten
        for neighbor in set(nx.all_neighbors(G, current[1])):

            # Nachbar noch nicht betrachtet und die Anzahl an Knoten wurde noch nicht erreicht
            if status[neighbor] == 0 and count_nodes < num_nodes:
                # Euklidische Distanz zu center berechnen und als Prioritaet für die Priority Queue verwenden
                dist = (G.nodes[neighbor]['x']-center[0])**2+(G.nodes[neighbor]['y']-center[1])**2
                q.put((dist, neighbor))

                new_graph.add_node(neighbor, **G.nodes[neighbor])

                # Knoten in Queue aber noch nicht komplett abgearbeitet
                status[neighbor] = 1
                count_nodes += 1

            # Nachbar abgearbeitet oder Anzahl an Knoten erreicht
            if not status[neighbor] == 1:
                continue

            # Fuege alle Kanten zwischen current und neighbor in den Graph ein
            from_node = current[1]
            to_node = neighbor

            for i in range(2):
                if G.has_successor(from_node, to_node):
                    # Schleife fuer Mehrfachkanten
                    for j in range(len(G[from_node][to_node])):
                        new_graph.add_edge(from_node, to_node, **G[from_node][to_node][j])
                        count_edges += 1

                        if count_edges == num_edges:
                            return new_graph

                if from_node == to_node:
                    break

                # Wechsle zu eingehenden Kanten
                from_node, to_node = to_node, from_node

        # Kanten abgearbeitet
        status[current[1]] = 2

    return new_graph


def generate_graph_radius(G: nx.MultiDiGraph, num_nodes: int, num_edges: int, radius:int):
    """
    Generiert einen neuen networkx.MultiDiGraph auf Grundlage eines gegebenen networkx.MultiDiGraph.
    Dabei wird an einem zufaelligen Knoten angefangen und durch Breitensuche der neuen Graph erweitert, solange,
    bis entweder alle Knoten im Radius um den Startknoten im neuen Graphen enthalten sind,
    oder min{num_nodes, num_edges} erreicht wurde.

    Es werden nur Knoten innerhalb das Radius vom Startknoten expandiert.

    :param G (networkx.Multidigraph):      Graph, aus welchem der neue Graph erzeugt werden soll
    :param num_nodes (int):                Maximale Anzahl an Knoten im neuen Graph
    :param num_edges (int):                Maximale Anzahl an Kanten im neuen Graph
    :return networkx.MultiDiGraph:         Generierter Graph
    """

    if G.number_of_nodes() == 0:
        raise ValueError('G has no nodes.')

    if num_nodes == 0 or radius == 0:
        return nx.MultiDiGraph()

    # Setze alle Knoten auf nicht markiert
    status = dict.fromkeys(G.nodes, 0)

    # Erstelle leeren Graphen
    new_graph = nx.MultiDiGraph(**G.graph)

    q = queue.SimpleQueue()
    count_nodes = 1
    count_edges = 0

    start = list(G.nodes)[randint(0, G.number_of_nodes()-1)]
    q.put(start)
    status[start] = 1

    center = (G.nodes[start]['x'], G.nodes[start]['y'])

    new_graph.add_node(start, **G.nodes[start])

    while not q.empty():
        current = q.get()

        # Betrachte alle aus-/eingehenden Kanten
        for neighbor in set(nx.all_neighbors(G, current)):

            # Euklidische Distanz zu center berechnen
            dist = (G.nodes[neighbor]['x']-center[0])**2+(G.nodes[neighbor]['y']-center[1])**2
            if dist > radius**2:
                continue

            # Nachbar noch nicht betrachtet und die Anzahl an Knoten wurde noch nicht erreicht
            if status[neighbor] == 0 and count_nodes < num_nodes:
                q.put(neighbor)

                new_graph.add_node(neighbor, **G.nodes[neighbor])

                # Knoten in Queue aber noch nicht komplett abgearbeitet
                status[neighbor] = 1
                count_nodes += 1

            # Nachbar abgearbeitet oder Anzahl an Knoten erreicht
            if not status[neighbor] == 1:
                continue

            # Fuege alle Kanten zwischen current und neighbor in den Graph ein
            from_node = current
            to_node = neighbor

            for i in range(2):
                if G.has_successor(from_node, to_node):
                    # Schleife fuer Mehrfachkanten
                    for j in range(len(G[from_node][to_node])):
                        new_graph.add_edge(from_node, to_node, **G[from_node][to_node][j])
                        count_edges += 1

                        if count_edges == num_edges:
                            return new_graph

                if from_node == to_node:
                    break

                # Wechsle zu eingehenden Kanten
                from_node, to_node = to_node, from_node

        # Kanten abgearbeitet
        status[current] = 2

    return new_graph


def generate_graph_bbox(G: nx.MultiDiGraph, num_nodes: int, num_edges: int, width: int, height: int):
    """
    Generiert einen neuen networkx.MultiDiGraph auf Grundlage eines gegebenen networkx.MultiDiGraph.
    Dabei wird an einem zufaelligen Knoten angefangen und durch Breitensuche der neuen Graph erweitert, solange,
    bis entweder alle Knoten innerhalb der BoundingBox um den Startknoten im neuen Graphen enthalten sind,
    oder min{num_nodes, num_edges} erreicht wurde.

    Es werden nur Knoten innerhalb der BoundingBox um den Startknoten expandiert.

    :param G (networkx.Multidigraph):      Graph, aus welchem der neue Graph erzeugt werden soll
    :param num_nodes (int):                Maximale Anzahl an Knoten im neuen Graph
    :param num_edges (int):                Maximale Anzahl an Kanten im neuen Graph
    :return networkx.MultiDiGraph:         Generierter Graph
    """

    if G.number_of_nodes() == 0:
        raise ValueError('G has no nodes.')

    if num_nodes == 0 or width == 0 or height == 0:
        return nx.MultiDiGraph()

    # Setze alle Knoten auf nicht markiert
    status = dict.fromkeys(G.nodes, 0)

    # Erstelle leeren Graphen
    new_graph = nx.MultiDiGraph(**G.graph)

    q = queue.SimpleQueue()
    count_nodes = 1
    count_edges = 0

    start = list(G.nodes)[randint(0, G.number_of_nodes()-1)]
    q.put(start)
    status[start] = 1

    center = (G.nodes[start]['x'], G.nodes[start]['y'])

    new_graph.add_node(start, **G.nodes[start])

    while not q.empty():
        current = q.get()

        # Betrachte alle aus-/eingehenden Kanten
        for neighbor in set(nx.all_neighbors(G, current)):

            if not (center[0]-width/2 <= G.nodes[neighbor]['x'] <= center[0]+width/2 and center[1]-height/2 <= G.nodes[neighbor]['y'] <= center[1]+height/2):
                continue

            # Nachbar noch nicht betrachtet und die Anzahl an Knoten wurde noch nicht erreicht
            if status[neighbor] == 0 and count_nodes < num_nodes:
                q.put(neighbor)

                new_graph.add_node(neighbor, **G.nodes[neighbor])

                # Knoten in Queue aber noch nicht komplett abgearbeitet
                status[neighbor] = 1
                count_nodes += 1

            # Nachbar abgearbeitet oder Anzahl an Knoten erreicht
            if not status[neighbor] == 1:
                continue

            # Fuege alle Kanten zwischen current und neighbor in den Graph ein
            from_node = current
            to_node = neighbor

            for i in range(2):
                if G.has_successor(from_node, to_node):
                    # Schleife fuer Mehrfachkanten
                    for j in range(len(G[from_node][to_node])):
                        new_graph.add_edge(from_node, to_node, **G[from_node][to_node][j])
                        count_edges += 1

                        if count_edges == num_edges:
                            return new_graph

                if from_node == to_node:
                    break

                # Wechsle zu eingehenden Kanten
                from_node, to_node = to_node, from_node

        # Kanten abgearbeitet
        status[current] = 2

    return new_graph


def bounding_box_from_graph(G: nx.MultiDiGraph):
    """
    Generiert eine Bounding Box aus G. Dabei werden die min/max lat/lng Werte gesucht.
    :param G: Eingabe Graph
    :return:  [lat_south, lng_west, lat_north, long_east]
    """
    if G.number_of_nodes() == 0:
        raise ValueError('Graph contains no nodes.')

    node = list(G.nodes(data=True))[0]
    min_lat = node[1]['y']
    max_lat = node[1]['y']
    min_lng = node[1]['x']
    max_lng = node[1]['x']

    for node in G.nodes(data=True):
        lat = node[1]['y']
        lng = node[1]['x']

        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

        if lng < min_lng:
            min_lng = lng
        if lng > max_lng:
            max_lng = lng

    return [min_lat, min_lng, max_lat, max_lng]


def bounding_box_from_points(points: List[Tuple[str, str]]):
    """
    Generiert eine Bounding Box von den gegebenen Punkten. Dabei werden die min/max lat/lng Werte gesucht.
    :param G: Eingabe Graph
    :return:  [lat_south, lng_west, lat_north, long_east]
    """
    if len(points) == 0:
        raise ValueError('No Points given.')

    min_lat = points[0][1]
    max_lat = points[0][1]
    min_lng = points[0][0]
    max_lng = points[0][0]

    for point in points:
        lat = point[1]
        lng = point[0]

        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

        if lng < min_lng:
            min_lng = lng
        if lng > max_lng:
            max_lng = lng

    return [min_lat, min_lng, max_lat, max_lng]

def nearest_neighbours_euclidian_dist(projected: nx.MultiDiGraph, projected_gdf: gp.GeoDataFrame, points_projected: gp.geoseries, max_distance: int):
    """
    Berechnet die naechsten Nachbarn von jedem Punkt in points_projected zu den Knoten aus dem Graphen projected.
    :param projected: Projizierter Graph
    :param projected_gdf: Knoten des projizierten Graph als Geodataframe
    :param points_projected: Projizierte Punkte
    :param max_distance: Maximale Distanz, die ein Punkt zum naechsten Knoten im Graph entfernt sein darf
    :return:
    """

    # Bestimme fuer jeden Punkt in der Eingabe die naechste Kante
    nearest_nodes_idx = projected_gdf.geometry.sindex.nearest(points_projected, max_distance=max_distance, return_all=True,
                                                          return_distance=False)

    # Entferne Duplikate, falls Ergebnis nicht leer (Code aus Geopandas.sindex.py)
    if nearest_nodes_idx.shape[1] > 0:
        # first subarray of geometry indices is sorted, so we can use this
        # trick to get the first of each index value
        mask = np.diff(nearest_nodes_idx[0, :]).astype("bool")
        # always select the first element
        mask = np.insert(mask, 0, True)

        nearest_nodes_idx = nearest_nodes_idx[:, mask]

    # Bestimme fuer jeden Punkt den naechsten Endpunkt auf der naechsten Kante
    nearest_nodes = []
    nodes = list(projected.nodes)
    for idx in nearest_nodes_idx[1]:
        nearest_nodes.append(nodes[idx])

    return nearest_nodes


def nearest_neighbours_edge_dist(projected: nx.MultiDiGraph, projected_gdf: gp.GeoDataFrame, points_projected: gp.geoseries, max_distance: int):
    """
    Berechnet die naechsten Nachbarn von jedem Punkt in points_projected zu den Knoten aus dem Graphen projected.
    Der naechste Knoten ist derjenige, der am naechsten entlang der naechsten Kante liegt.
    :param projected: Projizierter Graph
    :param projected_gdf: Kanten des projizierten Graphen
    :param points_projected: Projizierte Punkte
    :param max_distance: Maximale Distanz, die ein Punkt zur naechsten Kante im Graph entfernt sein darf
    :return:
    """

    # Bestimme fuer jeden Punkt in der Eingabe die naechste Kante
    nearest_edges = projected_gdf.sindex.nearest(points_projected, max_distance=max_distance, return_all=True,
                                                 return_distance=False)

    # Entferne Duplikate, falls Ergebnis nicht leer (Code aus Geopandas.sindex.py)
    if nearest_edges.shape[1] > 0:
        # first subarray of geometry indices is sorted, so we can use this
        # trick to get the first of each index value
        mask = np.diff(nearest_edges[0, :]).astype("bool")
        # always select the first element
        mask = np.insert(mask, 0, True)

        nearest_edges = nearest_edges[:, mask]

    # Bestimme fuer jeden Punkt den naeheren Endpunkt entlang der naechsten Kante
    nearest_nodes = []
    edges = list(projected.edges)
    for j in range(len(nearest_edges[0])):
        line = projected_gdf['geometry'].iloc[nearest_edges[1][j]]
        point = points_projected.iloc[nearest_edges[0][j]]
        # Finde naeheren der beiden Endknoten entlang der Kante
        if line.project(point) <= line.length / 2:
            nearest_nodes.append(edges[nearest_edges[1][j]][0])
        else:
            nearest_nodes.append(edges[nearest_edges[1][j]][1])

    return nearest_nodes


def label_graph(G: nx.MultiDiGraph, amenity_list: List[str], result_amenities_complete: gp.GeoDataFrame, max_distance: int, mode: str, binary_label: bool = False):
    """
    Jeder Knoten im Graphen bekommt einen Labelvektor [amenity_1, amenity_2, ...].
    In diesem Labelvektor wird gespeichert, wie wie oft der jeweilige Knoten der naechste Knoten von einer dieser amenities ist.
    Modi:
        -> euclidian_dist: Der naechste Knoten nach euklidischer Distanz
        -> nearest_edge: Der naehere Endknoten entlang der naechsten Kante

    Wenn der uebergebene Graph bereits projiziert ist, muss er das Attribut 'bbox_before_projected' haben, welches
    die Bounding Box des Graphen im Koordinatenreferenzsystem epsg:4326 ist.

    :param G: Graph, welcher gelabelt wird
    :param amenity_list: Liste von Amenities, nach denen gelabelt wird
    :param result_amenities_complete: Alle Amenities, von denen aus die naechsten Nachbarn bestimmt werden.
                                      Diese werden zunaechst nach der Bounding Box des Graphen gefiltert
    :param max_distance: Maximale Distanz, die ein Knoten von einer Kante entfernt sein darf
    :param mode: euclidian_dist, nearest_edge
    :param binary_label: Falls True, speichere binaere Labelvektoren, sonst Zaehler, wie oft naechster Nachbar
    :return:
    """

    if max_distance <= 0:
        raise ValueError('Parameter max_distance must be greater than 0.')
    if mode not in ['nearest_edge', 'euclidian_dist']:
        raise ValueError('Unknown mode, only "nearest_edge" and "euclidian_dist" allowed.')

    # Jedem Knoten einen Label Vektor hinzufuegen
    for node in list(G.nodes):
        G.nodes[node]['label_vec'] = [0]*len(amenity_list)

    # Falls der Graph keine Knoten hat oder result_amenities_complete leer ist
    if G.number_of_nodes() == 0 or G.number_of_edges() == 0 or len(result_amenities_complete) == 0:
        return

    # Falls Graph nicht projiziert, projiziere ihn und berechne bbox
    if not ox.projection.is_projected(G.graph['crs']):
        projected = ox.project_graph(G)
        bbox = bounding_box_from_graph(G)
    else:
        # Graph berteits projiziert -> bbox aus bbox_before_projected attribut
        projected = G
        if 'bbox_before_projected' not in G.graph:
            raise AttributeError('Graph projected but bbox_before_projected not in attributes.')
        bbox = G.graph['bbox_before_projected']

    nodes_proj_gdf, edges_proj_gdf = ox.graph_to_gdfs(projected, nodes=True, edges=True)

    # Anfrage: Alle POI die in der Bounding Box des Graphen liegen
    result = result_amenities_complete.cx[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # Anfrage erfolglos
    if len(result) == 0:
        return

    # Projiziere die Punkte des Ergebnis der Anfrage in das gleiche Koordinatensystem wie projected
    result = result.to_crs(projected.graph['crs'])

    # Berechne fuer jeden Amenity Tag die naechsten Nachbarn
    for i, amenity in enumerate(amenity_list):

        # Alle Spalten mit gewuenschter Amenity rausfiltern
        mask = result['amenity'] == amenity
        pos = np.flatnonzero(mask)
        points_projected = result.iloc[pos]

        # Keine Ergebnisse gefunden
        if len(points_projected) == 0:
            continue

        if mode == 'nearest_edge':
            nearest_nodes = nearest_neighbours_edge_dist(projected, edges_proj_gdf, points_projected['geometry'], max_distance)
        elif mode == 'euclidian_dist':
            nearest_nodes = nearest_neighbours_euclidian_dist(projected, nodes_proj_gdf, points_projected['geometry'], max_distance)

        # Falls binary_label, kommt jeder Knoten hoechstens einmal als naechster Nachbar vor -> binaere Label
        if binary_label:
            nearest_nodes = set(nearest_nodes)

        # Setze Label Vektor auf die Anzahl der jeweils naechsten Nachbarn
        for id in nearest_nodes:
            G.nodes[id]['label_vec'][i] += 1


def random_places(n: int):
    os.chdir(util.default_directory)
    cities_cleaned = pd.read_csv("cities_cleaned.csv").to_dict('records')
    places = []

    for i in range(n):
        # Lose Stadt zufaellig aus
        rand_num = randint(0, len(cities_cleaned)-1)
        sample = cities_cleaned[rand_num]
        del cities_cleaned[rand_num]
        places.append((sample['city'], sample['country']))

        if len(cities_cleaned) == 0:
            util.log_file_path(f'All possible cities ({i}) were chosen. No cities left.')
            break

    return places
