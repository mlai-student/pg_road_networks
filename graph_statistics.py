#!/usr/bin/env python
"""
Stellt die Funktionalitaet zum Berechnen der Statistiken bereit.
"""

import collections
import csv

import osmnx as ox
import networkx as nx
import numpy as np
import math
from typing import List, Dict

stat_names = ['name', 'num_nodes', 'num_edges_loops', 'num_edges', 'num_edges_multi', 'density', 'out_deg_hist', 'avg_deg', 'std_deg', 'max_deg', 'min_deg', 'mode_deg', 'out_deg_hist_multi', 'avg_deg_multi',
            'std_deg_multi', 'max_deg_multi', 'min_deg_multi', 'mode_deg_multi', 'label_hist', 'avg_lbl', 'std_lbl', 'max_lbl', 'min_lbl', 'mode_lbl', 'total_edge_length', 'total_edge_length_multi', 'total_edge_length_by_type', 'graph_label']

avg_stat_names = ['name',
'sum_num_nodes', 'avg_num_nodes', 'std_num_nodes',
'sum_num_edges_loops', 'avg_num_edges_loops', 'std_num_edges_loops',
'sum_num_edges', 'avg_num_edges', 'std_num_edges',
'sum_num_edges_multi', 'avg_num_edges_multi','std_num_edges_multi',
'density', 'avg_density', 'std_density', 'out_deg_hist', 'sum_deg', 'avg_deg', 'std_deg', 'max_deg','min_deg', 'mode_deg','out_deg_hist_multi',
'sum_deg_multi', 'avg_deg_multi', 'std_deg_multi', 'max_deg_multi', 'min_deg_multi', 'mode_deg_multi',
'label_hist', 'sum_lbl', 'avg_lbl', 'std_lbl', 'max_lbl', 'min_lbl', 'mode_lbl',
'sum_total_edge_length', 'avg_total_edge_length', 'std_total_edge_length',
'sum_total_edge_length_multi', 'avg_total_edge_length_multi', 'std_total_edge_length_multi',
'sum_total_edge_length_by_type', 'avg_total_edge_length_by_type', 'std_total_edge_length_by_type']


def get_out_degree(G: nx.MultiDiGraph, multi_edges: bool = False):
    """
    Histogramm mit Ausgangsgraden der Knoten. Wenn Multiedges False, dann werden nur Kanten mit key=0 betrachtet
    :param G:
    :param multi_edges: Gibt an ob Multikanten betrachtet werden. Default: False
    :return: np.array
    """
    if multi_edges:
        counts = collections.Counter(G.out_degree[node] for node in G.nodes)
    else:
        counts = collections.Counter(len(G[node]) for node in G.nodes)

    return np.array([counts.get(i, 0) for i in range(max(counts) + 1)])


def get_label_hist(G: nx.MultiDiGraph, namenities: int):
    """
    Gibt ein Histogramm {0:{hist}, 1:{hist},...} wieder
    :param G:
    :param namenities: Anzahl der Amenities (laenge der Label im Graphen
    :return: 2-Dimensionales np.array
    """
    hist = {x: {} for x in range(namenities)}
    # Erzeuge Histogramm als dict-von-dicts
    for osmid, label in G.nodes(data='label_vec'):
        for i in range(namenities):
            if not label[i] in hist[i]:
                hist[i][label[i]] = 1
            else:
                hist[i][label[i]] += 1

    # Fuelle fehlende Schluessel (haeufigkeiten auf)
    for key in hist.keys():
        for i in range(max(hist[key].keys())+1):
            if not i in hist[key].keys():
                hist[key][i] = 0

    # Sortieren und gleich lang machen
    max_k = 0
    for key in hist.keys():
        if len(hist[key]) > max_k:
            max_k = len(hist[key])
        hist[key] = dict(sorted(hist[key].items()))

    # 2-Dimensionales np.array erstellen
    return np.array([list(d.values())+[0]*(max_k-len(d)) for d in hist.values()])


def get_length_by_type(G: nx.MultiDiGraph, undirected=True):
    """
    Gibt ein Histogramm der Strassenlaengen im Graphen nach Type wieder. Der Type ist dabei der Wert
    des OpenStreetMaps Attribut 'highway'
    :param G:
    :param undirected: Gibt an, ob der Graph als ungerichteter Graph betrachtet werden soll
    :return: Histogramm als Python dict
    """

    hist = {}
    if G.number_of_edges() > 0:
        G_u = ox.get_undirected(G) if undirected else G
        for u, v, k in G_u.edges:
            highway = G_u[u][v][k]['highway']
            # Attributwert zu Liste, da manchmal schon Listen als Attribut Wert gespeichert sind
            if not type(highway) == list:
                highway = [highway]

            for entry in highway:
                if not entry in hist:
                    hist[entry] = G_u[u][v][k]['length']
                else:
                    hist[entry] += G_u[u][v][k]['length']

    return hist


def accumulate_total_edge_length_by_type(dicts: List[Dict]):
    """
    Berechnet die Durchnschnitt und die Standardabweichung ueber alle dictionaries in der Liste
    fuer jeden einzelnen Key
    :param dicts: Liste von dictionaries mit Zahlenwerten
    :return: Tuple (sum, average, standard deviation)
    """
    # Finde alle keys
    all_keys = set().union(*(d.keys() for d in dicts))
    keys_idx = dict(zip(all_keys, range(len(all_keys))))

    # Summiere die Laenge der Straßentypen auf
    counts = np.zeros(len(all_keys))
    for d in dicts:
        for key in d.keys():
            counts[keys_idx[key]] += d[key]

    average = counts/len(dicts)

    # Berechne die Standardabweichung
    std_dev = np.zeros(len(all_keys))
    for d in dicts:
        for key in d.keys():
            std_dev[keys_idx[key]] += (d[key]-average[keys_idx[key]])**2

    std_dev = np.sqrt(std_dev/len(dicts))

    sum_dict = dict(zip(all_keys, [counts[i] for i in range(counts.size)]))
    average_dict = dict(zip(all_keys, [average[i] for i in range(average.size)]))
    std_dev_dict = dict(zip(all_keys, [std_dev[i] for i in range(std_dev.size)]))
    return sum_dict, average_dict, std_dev_dict


def calculate_stats(G: nx.MultiDiGraph, name:str, nAmenities: int):
    # Knoten
    num_nodes = G.number_of_nodes()
    # Kanten
    num_edges_loops = len([x for x in G.edges if x[2] == 0])                      # keine Mehrfachkanten mit Schleifen
    num_edges = len([x for x in G.edges if x[2] == 0 and x[0] != x[1]])           # keine Mehrfachkanten ohne Schleifen
    num_edges_multi = G.number_of_edges()                                         # mit Mehrfachkanten und Schleifen
    # Dichte d=m/(n*(n-1)) ohne Schleifen, 0 wenn Graph nur einen Knoten enthaelt
    density = float(num_edges)/(num_nodes*(num_nodes-1)) if num_nodes > 1 else 0
    # Ausgangsgrad ohne Mehrfachkanten
    out_deg_hist = get_out_degree(G, False)
    # Durchschnittlicher Ausgangsgrad
    avg_deg = np.sum(out_deg_hist*np.arange(out_deg_hist.size))/num_nodes
    # Standardabweichung
    std_dev_deg = np.sqrt(np.sum((((np.arange(out_deg_hist.size)-avg_deg)**2)*out_deg_hist))/num_nodes)
    max_deg = out_deg_hist.size - 1
    min_deg = np.argmax(out_deg_hist > 0)
    mode_deg = np.argmax(out_deg_hist)
    # Ausgangsgrad mit Mehrfachkanten
    out_deg_hist_multi = get_out_degree(G, True)
    avg_deg_multi = np.sum(out_deg_hist_multi*np.arange(out_deg_hist_multi.size))/num_nodes
    std_dev_deg_multi = np.sqrt(np.sum((((np.arange(out_deg_hist_multi.size)-avg_deg_multi)**2)*out_deg_hist_multi))/num_nodes)
    max_deg_multi = out_deg_hist_multi.size - 1
    min_deg_multi = np.argmax(out_deg_hist_multi > 0)
    mode_deg_multi = np.argmax(out_deg_hist_multi)
    # Knotenlabel
    if nAmenities > 0:
        label_hist = get_label_hist(G, nAmenities)
        avg_lbl = np.sum(label_hist*np.arange(label_hist.shape[1]), axis=1)/num_nodes
        # sqrt(sum(index-avg)**2*haeufigkeit[i])/n)
        std_dev_lbl = np.sqrt(np.sum((((np.tile(np.arange(label_hist.shape[1]), (label_hist.shape[0],1))-np.array([avg_lbl]).T)**2)*label_hist),axis=1)/num_nodes)
        max_lbl = np.apply_along_axis(lambda arr: arr.size - np.argmax(np.flip(arr>0)) - 1, 1, label_hist)
        min_lbl = np.argmax(label_hist > 0)
        mode_lbl = np.argmax(label_hist)
    else:
        label_hist = None
        avg_lbl = None
        std_dev_lbl = None
        max_lbl =  None
        min_lbl = None
        mode_lbl = None
    # Kantenlaenge
    # ohne Mehrfachkanten
    total_edge_length = sum(G[u][v][k]['length'] for u, v, k in G.edges if k == 0) if G.number_of_edges() > 0 else 0
    # mit Mehrfachkanten
    total_edge_length_multi = ox.stats.edge_length_total(G)
    # Kantenlaenge nach Typ gerichtet
    total_edge_length_by_type = get_length_by_type(G, False)
    # Graph label
    graph_label = G.graph['graph_label']

    values = [name, num_nodes, num_edges_loops, num_edges, num_edges_multi, density, out_deg_hist, avg_deg, std_dev_deg,
              max_deg, min_deg, mode_deg, out_deg_hist_multi, avg_deg_multi,
              std_dev_deg_multi, max_deg_multi, min_deg_multi, mode_deg_multi, label_hist, avg_lbl, std_dev_lbl,
              max_lbl, min_lbl, mode_lbl, total_edge_length, total_edge_length_multi,
              total_edge_length_by_type, graph_label]
    return dict(zip(stat_names, values))


def write_stats(list_of_stats, filepath, nAmenities):
    with open(filepath + "/"+ "statistics.txt", "w", encoding='utf8') as csvfile:

        csvfile.write("----------------------------------------------------------------------------------------------------------\n")
        csvfile.write("-------------------------------------Individual statistics for each graph---------------------------------\n")
        csvfile.write("----------------------------------------------------------------------------------------------------------\n")
        csvfile.write("\n")

        writer = csv.DictWriter(csvfile, fieldnames=stat_names)
        writer.writeheader()

        for graph_stats in list_of_stats[0]:
            writer.writerow(graph_stats)

        if len(list_of_stats[1]) > 0:
            csvfile.write("----------------------------------------------------------------------------------------------------------\n")
            csvfile.write("-------------------------------------Average statistics for each city-------------------------------------\n")
            csvfile.write("----------------------------------------------------------------------------------------------------------\n")
            csvfile.write("\n")
            writer = csv.DictWriter(csvfile, fieldnames=avg_stat_names)
            writer.writeheader()
            for city in list_of_stats[1]:
                writer.writerow(city.get_accumulated_stats())

        csvfile.write("----------------------------------------------------------------------------------------------------------\n")
        csvfile.write("-------------------------------------Average statistics of all graphs-------------------------------------\n")
        csvfile.write("----------------------------------------------------------------------------------------------------------\n")
        csvfile.write("\n")
        writer = csv.DictWriter(csvfile, fieldnames=avg_stat_names)
        writer.writeheader()
        writer.writerow(list_of_stats[2][0].get_accumulated_stats())


def calc_avg_stats(list_of_stats, name):

    # Initialisiere values mit dem Graphnamen(da über diesen kein Durchschnitt berechnet wird).
    values = ["average_"+name]
    n = len(list_of_stats)

    # Iteriere über alle Statistiken
    for i in range(len(stat_names)):

        # Fuer nicht gelabelte Graphen existieren einige Statistiken nicht, diese werden übersprungen.
        if list_of_stats[0].get(stat_names[i]) is None:
            values.append(None)
            continue

        # Fuer Statistiken mit eindeutigem Zahlenwert kann der Mittelwert durch aufsummieren und durch n teilen gebildet werden.
        if stat_names[i] not in ['name', 'out_deg_hist', 'out_deg_hist_multi', 'label_hist', 'avg_lbl', 'std_lbl',
                                 'graph_label', 'total_edge_length_by_type', 'total_edge_un', 'avg_deg', 'std_deg', 'avg_deg_multi', 'std_deg_multi']:

            # Average fuer nicht Histogramm Statistiken
            value = 0
            for j in range(n):
                value = value + list_of_stats[j].get(stat_names[i])

            # Die Gesamtdensity muss neu berechnet werden, da man die Dichten nicht einfach aufsummeren kann
            if stat_names[i] not in ['density', 'max_lbl', 'min_lbl', 'mode_lbl',
                                     'max_deg', 'min_deg', 'mode_deg', 'max_deg_multi', 'min_deg_multi', 'mode_deg_multi']:
                values.append(value)  # summe der einfachen Statistiken

            elif stat_names[i] == 'density':
                density = float(values[7]) / (values[1] * (values[1] - 1)) if values[1] > 1 else 0
                values.append(density)

            avg = value/n
            values.append(avg)
            # Standardardabweichung fuer nicht histogramm statistiken
            value = 0
            for j in range(n):
                value += (list_of_stats[j].get(stat_names[i])-avg)**2
            std = np.sqrt(value / n)
            values.append(std)

        elif stat_names[i] in ['total_edge_length_by_type', 'total_edge_length_by_type_undirected']:
            dict_list = []
            for j in range(n):
                dict_list.append(list_of_stats[j].get(stat_names[i]))

            sum_dict, average_dict, std_dev_dict = accumulate_total_edge_length_by_type(dict_list)

            values.append(sum_dict) # Gesamtsumme aller Strassenlaengen nach type
            values.append(average_dict)
            values.append(std_dev_dict)

        elif stat_names[i] in ['out_deg_hist', 'out_deg_hist_multi']:
            accu_hist = np.zeros(list_of_stats[0].get(stat_names[i]).shape).astype(np.float64)
            for j in range(n):
                value = list_of_stats[j].get(stat_names[i]).astype(np.float64)
                if accu_hist.size <= value.size:
                    accu_hist, value = value, accu_hist
                accu_hist[:value.size] += value

            sum_deg = np.sum(accu_hist * np.arange(accu_hist.size)) # Summe aller Knotegrade
            avg_deg = sum_deg / np.sum(accu_hist)                  # Durchschnittlicher Knotengrad
            std_dev_deg = np.sqrt(np.sum((((np.arange(accu_hist.size) - avg_deg) ** 2) * accu_hist)) / np.sum(accu_hist))
            avg = accu_hist/n # ???
            max_deg = accu_hist.size - 1
            min_deg = np.argmax(accu_hist > 0)
            mode_deg = np.argmax(accu_hist)

            values.append(accu_hist)
            values.append(sum_deg)
            values.append(avg_deg)
            values.append(std_dev_deg)
            values.append(max_deg)
            values.append(min_deg)
            values.append(mode_deg)
        elif stat_names[i] in ['label_hist']:
            curr = np.zeros(list_of_stats[0].get(stat_names[i]).shape).astype(np.float64)
            for j in range(n):
                arr = list_of_stats[j].get(stat_names[i]).astype(np.float64)
                if curr.shape[1] <= arr.shape[1]:
                    curr, arr = arr, curr
                curr[:, :arr.shape[1]] += arr

            sum_lbl = np.sum(curr*np.arange(curr.shape[1]), axis=1)
            avg_lbl = sum_lbl/np.sum(curr,axis=1)
            std_dev_lbl = np.sqrt(np.sum((((np.tile(np.arange(curr.shape[1]), (curr.shape[0], 1))
                                            - np.array([avg_lbl]).T) ** 2) * curr), axis=1) / np.sum(curr, axis=1))
            max_lbl = np.apply_along_axis(lambda arr: arr.size - np.argmax(np.flip(arr > 0)) - 1, 1, curr)
            min_lbl = np.argmax(curr > 0)
            mode_lbl = np.argmax(curr)

            values.append(curr)
            values.append(sum_lbl)
            values.append(avg_lbl)
            values.append(std_dev_lbl)
            values.append(max_lbl)
            values.append(min_lbl)
            values.append(mode_lbl)

    print(dict(zip(avg_stat_names, values)))
    return dict(zip(avg_stat_names, values))


class StatAccumulator:

    def __init__(self, name, n_amenities):
        self.name = name
        self.num_nodes = []
        self.num_edges = []
        self.num_edges_loops = []
        self.num_edges_multi = []
        self.density = []
        self.out_deg_hist = np.zeros((1,))
        self.out_deg_hist_multi = np.zeros((1,))
        self.label_hist = np.zeros((n_amenities, 1)) if n_amenities > 0 else None
        self.total_edge_length = []
        self.total_edge_length_multi = []
        self.total_edge_length_by_type = {}
        self.num_graphs = 0

    def increment_stats(self, to_add: dict):

        # Fuege Anzahl Knoten in Liste ein
        self.num_nodes.append(to_add['num_nodes'])

        # Fuege Kanten ohne Mehrfachkanten in Liste ein
        self.num_edges.append(to_add['num_edges'])

        # Fuege Kanten mit Schlaufen ohne Mehrfachkanten in Liste ein
        self.num_edges_loops.append(to_add['num_edges_loops'])

        # Fuege Kanten mit Schlaufen und Mehrfachkanten in Liste ein
        self.num_edges_multi.append(to_add['num_edges_multi'])

        # Fuege density Werte hinzu
        self.density.append(to_add['density'])

        # Inkrementiere Ausgangsgrad ohne Mehrfachkanten Histogramm
        to_add_hist = to_add['out_deg_hist'].copy().astype(self.out_deg_hist.dtype)
        if self.out_deg_hist.size < to_add_hist.size:
            self.out_deg_hist, to_add_hist = to_add_hist, self.out_deg_hist
        self.out_deg_hist[:to_add_hist.size] += to_add_hist

        # Inkrementiere Ausgangsgrad mit Mehrfachkanten Histogramm
        to_add_hist = to_add['out_deg_hist_multi'].copy().astype(self.out_deg_hist_multi.dtype)
        if self.out_deg_hist_multi.size < to_add_hist.size:
            self.out_deg_hist_multi, to_add_hist = to_add_hist, self.out_deg_hist_multi
        self.out_deg_hist_multi[:to_add_hist.size] += to_add_hist

        # Inkrementiere Label Histogramm
        if self.label_hist is not None:
            to_add_label_hist = to_add['label_hist'].copy().astype(self.label_hist.dtype)
            if self.label_hist.shape[1] < to_add_label_hist.shape[1]:
                self.label_hist, to_add_label_hist = to_add_label_hist, self.label_hist
            self.label_hist[:, :to_add_label_hist.shape[1]] += to_add_label_hist

        # Fuege Gesamtkantenlaenge ohne Mehrfachkanten in Liste ein
        self.total_edge_length.append(to_add['total_edge_length'])

        # Fuege Gesamtkantenlaenge mit Mehrfachkanten in Liste ein
        self.total_edge_length_multi.append(to_add['total_edge_length_multi'])

        # Inkrementiere Gesamtkantenlaenge nach Typ
        for key, val in list(to_add['total_edge_length_by_type'].items()):
            if key not in self.total_edge_length_by_type:
                self.total_edge_length_by_type[key] = [val]
            else:
                self.total_edge_length_by_type[key].append(val)

        # Inkrementiere Anzahl der Graphen die bis jetzt in die Akkumulierte Statistik reinzaehlen
        self.num_graphs += 1

    def get_stats_list_1D(self, values: list):
        if len(values) == 0:
            raise ValueError('List must not be empty!')

        sum_values = sum(values)
        avg_values = float(sum_values)/len(values)
        std_values = math.sqrt(float(sum([(x-avg_values)**2 for x in values])/len(values)))

        return [sum_values, avg_values, std_values, max(values), min(values), max(set(values), key=values.count)]

    def get_stats_hist_1D(self, hist: np.array):
        if hist.size == 0:
            raise ValueError('Array must not be empty!')

        sum_hist = np.sum(hist * np.arange(hist.size))
        avg_hist = sum_hist / np.sum(hist) if sum_hist > 0 else 0
        std_hist = np.sqrt(np.sum((((np.arange(hist.size) - avg_hist) ** 2) * hist)) / np.sum(hist)) if sum_hist > 0 else 0
        max_hist = hist.size - 1
        min_hist = np.argmax(hist > 0)
        mode_hist = np.argmax(hist)

        return [sum_hist, avg_hist, std_hist, max_hist, min_hist, mode_hist]


    def get_stats_hist_2D(self, hist: np.array):
        sum_hist = np.sum(hist * np.arange(hist.shape[1]), axis=1)
        avg_hist = sum_hist / np.sum(hist, axis=1)
        std_hist = np.sqrt(np.sum((((np.tile(np.arange(hist.shape[1]), (hist.shape[0], 1)) - np.array([avg_hist]).T) ** 2) * hist), axis=1) / np.sum(hist, axis=1))
        max_hist = np.apply_along_axis(lambda arr: arr.size - np.argmax(np.flip(arr > 0)) - 1, 1, hist)
        min_hist = np.argmax(hist > 0, axis=1)
        mode_hist = np.argmax(hist, axis=1)

        return [sum_hist, avg_hist, std_hist, max_hist, min_hist, mode_hist]

    def get_stats_hist_dict(self, hist: Dict):
        sum_hist = {}
        average_hist = {}
        std_hist = {}

        for key in hist.keys():
            sum_ = sum(hist[key])
            sum_hist[key] = sum_
            average = float(sum_)/len(hist[key]) if sum_ > 0 else 0
            average_hist[key] = average
            std_hist[key] = math.sqrt(float(sum([(x-average)**2 for x in hist[key]])/len(hist[key]))) if sum_ > 0 else 0

        return [sum_hist, average_hist, std_hist]


    def get_accumulated_stats(self):
        stats = {}

        stats['name'] = self.name
        keys = ['sum_num_nodes', 'avg_num_nodes', 'std_num_nodes']
        values = self.get_stats_list_1D(self.num_nodes)[:3]
        stats.update(dict(zip(keys, values)))

        keys = ['sum_num_edges_loops', 'avg_num_edges_loops', 'std_num_edges_loops']
        values = self.get_stats_list_1D(self.num_edges_loops)[:3]
        stats.update(dict(zip(keys, values)))

        keys = ['sum_num_edges', 'avg_num_edges', 'std_num_edges']
        values = self.get_stats_list_1D(self.num_edges)[:3]
        stats.update(dict(zip(keys, values)))

        keys = ['sum_num_edges_multi', 'avg_num_edges_multi', 'std_num_edges_multi']
        values = self.get_stats_list_1D(self.num_edges_multi)[:3]
        stats.update(dict(zip(keys, values)))

        keys = ['density', 'avg_density', 'std_density']
        density = 0
        if stats['sum_num_nodes'] > 1:
            density = float(stats['sum_num_edges'])/(stats['sum_num_nodes']*(stats['sum_num_nodes']-1))

        values = [density] + self.get_stats_list_1D(self.density)[1:3]
        stats.update(dict(zip(keys, values)))

        keys = ['out_deg_hist', 'sum_deg', 'avg_deg', 'std_deg', 'max_deg','min_deg', 'mode_deg']
        values = [self.out_deg_hist] + self.get_stats_hist_1D(self.out_deg_hist)
        stats.update(dict(zip(keys, values)))

        keys = ['out_deg_hist_multi', 'sum_deg_multi', 'avg_deg_multi', 'std_deg_multi', 'max_deg_multi', 'min_deg_multi', 'mode_deg_multi']
        values = [self.out_deg_hist_multi] + self.get_stats_hist_1D(self.out_deg_hist_multi)
        stats.update(dict(zip(keys, values)))

        keys = ['label_hist', 'sum_lbl', 'avg_lbl', 'std_lbl', 'max_lbl', 'min_lbl', 'mode_lbl']
        if self.label_hist is not None:
            values = [self.label_hist] + self.get_stats_hist_2D(self.label_hist)
        else:
            values = [None, None, None, None, None, None, None]
        stats.update(dict(zip(keys, values)))

        keys = ['sum_total_edge_length', 'avg_total_edge_length', 'std_total_edge_length']
        values = self.get_stats_list_1D(self.total_edge_length)[:3]
        stats.update(dict(zip(keys, values)))

        keys = ['sum_total_edge_length_multi', 'avg_total_edge_length_multi', 'std_total_edge_length_multi']
        values = self.get_stats_list_1D(self.total_edge_length_multi)[:3]
        stats.update(dict(zip(keys, values)))

        keys = ['sum_total_edge_length_by_type', 'avg_total_edge_length_by_type', 'std_total_edge_length_by_type']
        values = self.get_stats_hist_dict(self.total_edge_length_by_type)
        stats.update(dict(zip(keys, values)))

        return stats

