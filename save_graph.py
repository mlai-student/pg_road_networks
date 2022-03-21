#!/usr/bin/env python
"""
Stellt die Funktionalitaet zum Speichern der Graphen bereit + Implementierung ETGF Format.
"""
import util
import os
import osmnx as ox
import networkx as nx
import numpy as np
import shapely
import re
import csv
import pyproj
import pickle

from io import StringIO
from enum import Enum


def get_types_etgf(d):
    """
    Bekommt ein Iterable von Dictionaries uebergeben und bestimmt zu allen Keys die Datentypen der Values.
    Die Angabe der Datentypen sind dabei: typ, list:typ oder mixed:typ, wenn die Values eines Keys sowohl einzeln und als Liste Vorhanden sind.
    :param d: Iterable von Dictionaries
    :return: Dictionary {Attribut: Datentyp}
    """
    keys_types = {}
    for entry in d:
        for key in entry.keys():
            # Pruefe, ob Schluessel schon vorhanden, sonst fuege ein
            tp = type(entry[key]).__name__
            if not key in keys_types:
                # Value ist eine Liste
                if tp == 'list':
                    if len(entry[key]) > 0:
                        elem_type = type(entry[key][0])

                        # Pruefe, ob alle Elemente in der Liste den gleichen Typ haben
                        if all(isinstance(x, elem_type) for x in entry[key]):
                            keys_types[key] = f'list:{type(entry[key][0]).__name__}'
                        else:
                            raise ValueError('Elements in list must be of same type!')
                    else:
                        # Liste ist leer, dementsprechend kann kein Datentyp angegeben werden
                        keys_types[key] = 'list:na'
                else:
                    # Elemente nicht in einer Liste
                    keys_types[key] = tp

            else:
                entry_type = keys_types[key] # Bereits vorhandener Typ
                # Schluessel schon vorhanden und Typ ist list
                if tp == 'list':
                    if len(entry[key]) > 0:
                        elem_type = type(entry[key][0])
                        if all(isinstance(x, elem_type) for x in entry[key]):

                            # Elemente von Key als Liste und nicht als Liste vorhanden
                            if entry_type == type(entry[key][0]).__name__:
                                keys_types[key] = f'mixed:{type(entry[key][0]).__name__}'

                            # Typen muessen auch bei mixed gleich sein
                            elif entry_type != f'list:{type(entry[key][0]).__name__}' and entry_type != f'mixed:{type(entry[key][0]).__name__}':
                                raise ValueError('Different types not allowed for same field!')
                        else:
                            raise ValueError('Elements in list must be of same type!')
                    elif not entry_type.startswith('list:'):
                        keys_types[key] = f'mixed:{entry_type}'

                # Schluessel schon vorhanden und Typ ist nicht list
                else:
                    if entry_type != tp and entry_type == f'list:{tp}':
                        if entry_type == f'list:{tp}':
                            keys_types[key] = f'mixed:{tp}'
                        else:
                            raise ValueError('Different types not allowed for same field!')

    return keys_types


def write_graph_as_etgf(G: nx.MultiDiGraph, filepath: str, filename: str, save_geom:bool, node_geometry: bool, edge_geometry: bool):
    """
    Schreibt den uebergebenen Graphen G im etgf Format an den uebergebenen Ort
    etgf Format:
    Graph Attribute
    Graph Attributwerte
    #
    Datentypen der Knotenattribute
    Knotenattribut Namen
    Knotenattribute im CSV Format
    #
    Datentypen der Kantenattribute
    Kantenattribut Namen
    Kantenattribute im CSV Format

    :param G: Zu speichernder Networkx MultiDiGraph
    :param filepath: Speicherort der Datei
    :param filename: Dateiname
    :param save_geom: Gibt an, ob die Geometrien gespeichert werden sollen
    :param node_geometry: Gibt an, ob fehlende Geometrien der Knoten induziert werden sollen
    :param edge_geometry: Gibt an, ob fehlende Geometrien der Kanten induziert werden sollen
    :return:
    """

    # Pruefe, ob der Graph Knoten enthaelt
    if not G.nodes:
        raise ValueError('graph contains no nodes')

    # Pruefe, ob der angegebene Dateipfad existiert
    if not filename.endswith('.etgf'):
        filename += '.etgf'
    if not os.path.isdir(filepath):
        raise IOError('Path does not exist or is not a directory')
    if os.path.exists(f'{filepath}/{filename}'):
        raise IOError('File already exists')

    with open(f'{filepath}/{filename}', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        keys_types = get_types_etgf([G.graph])
        writer.writerow(keys_types.values())
        writer.writerow(G.graph.keys())
        writer.writerow(G.graph.values())
        f.write('#\n')

        nodes, node_data = zip(*G.nodes(data=True))

        # find header
        keys_types = get_types_etgf(node_data)
        types = list(keys_types.values())
        header = list(keys_types.keys())

        if not save_geom:
            if 'geometry' in header:
                idx = header.index('geometry')
                del header[idx]
                del types[idx]

        else:
            if node_geometry:
                if not 'geometry' in header:
                    header.append('geometry')
                    types.append('Point')

                for d in node_data:
                    if not 'geometry' in d.keys():
                        d['geometry'] = f'POINT ({d["x"]} {d["y"]})'

        writer.writerow(['int'] + types)
        writer.writerow(['osmid'] + header)
        for i in range(len(G.nodes)):
            writer.writerow([nodes[i]] + [node_data[i].get(key, '') for key in header])

        f.write('#\n')

        if G.number_of_edges() > 0:
            u, v, k, edge_data = zip(*G.edges(keys=True, data=True))
            keys_types = get_types_etgf(edge_data)

            types = list(keys_types.values())
            header = list(keys_types.keys())

            if not save_geom:
                if 'geometry' in header:
                    idx = header.index('geometry')
                    del header[idx]
                    del types[idx]
            else:
                if edge_geometry:
                    if not 'geometry' in header:
                        header.append('geometry')
                        types.append('LineString')

                    for i, edge in enumerate(edge_data):
                        if 'geometry' not in edge.keys():
                            edge['geometry'] = f'LINESTRING ({G.nodes[u[i]]["x"]} {G.nodes[u[i]]["y"]}, {G.nodes[v[i]]["x"]} {G.nodes[v[i]]["y"]})'

            writer.writerow(['int', 'int', 'int'] + types)
            writer.writerow(['u', 'v', 'key'] + header)
            for i in range(len(G.edges)):
                writer.writerow([u[i], v[i], k[i]] + [edge_data[i].get(key, '') for key in header])


def cast_types_etgf(val: str, val_type: str):
    """
    Bekommt einen String, sowie den zugehoerigen Datentyp uebergeben und Typecastet diesen entsprechend.
    Unterstuetzte typen sind dabei str, int, float, bool, numpy.int64, numpy.float64 shapely.geometry.Point, shapely.geometry.Linestring
    :param val: Zu castender Wert
    :param val_type: Typ zu dem gecastet werden soll
    :return: Gecasteter Wert
    """
    # Erlaubte Typen mit entsprechender Cast Funktion
    types = {
        'str': str,
        'int': int,
        'float': float,
        'bool': lambda x: x == 'True',
        'int64': np.int64,
        'float64': np.float64,
        'Point': shapely.wkt.loads,
        'LineString': shapely.wkt.loads,
        'CRS': pyproj.crs.CRS
    }
    if val_type.startswith('mixed') or val_type.startswith('list'):
        elem_type = val_type.split(':')[1]
        if elem_type != 'na' and not elem_type in types:
            raise TypeError('Not allowed type in etgf format')

        if val[0] == '[':
            if elem_type == 'na':
                return []
            else:
                # (?=(?:[^"]|"[^"]*")*$) beachtet Kommas, die durch Anfuehrugnszeichen umgeben sind.
                # Es wir nur bei nicht von Anfuehrungszeichen umgebenen Kommas getrennt
                return [types[elem_type](x.lstrip(' ').strip("'")) for x in re.split(r',(?=(?:[^"]|"[^"]*")*$)', val.strip(']['))]
        else:
            return types[elem_type](val)
    else:
        if val_type not in types:
            raise TypeError('Not allowed type in etgf format')
        return types[val_type](val)


def graph_from_etgf(filepath: str):
    """
    Liest einen Graphen im etgf Format ein und gibt diesen aus
    :param filepath: Dateipfad
    :return: networkx.MultiDiGraph
    """

    G = nx.MultiDiGraph()

    # Pruefe, ob der angegebene Dateipfad existiert
    if not filepath.endswith('.etgf'):
        raise IOError('File must be a .etgf file.')
    if not os.path.exists(filepath):
        raise IOError(f'File not found at: {filepath}')

    try:
        with open(filepath, 'r', encoding='utf8') as f:
            lines = f.read().split('#\n')

            # Lese Graphattribute
            block = StringIO(lines[0])
            reader = csv.reader(block, quotechar='"')
            types = reader.__next__()
            attr = reader.__next__()
            val = [cast_types_etgf(v, t) for v, t in zip(reader.__next__(), types)]
            block.close()
            # Setze Graphattribute
            G.graph = dict(zip(attr, val))

            # Lese Knoten
            block = StringIO(lines[1])
            reader = csv.reader(block, quotechar='"')
            types = reader.__next__()
            attr = reader.__next__()

            for line in reader:
                # Typecaste alle Eintraege in der Zeile, wenn sie nicht der leere String sind
                val = [(a, cast_types_etgf(v, t)) for v, t, a in zip(line, types, attr) if v != '']
                # val[0][1] ist die OSMID
                G.add_node(val[0][1], **dict(val[1:]))
            block.close()

            # Lese Kanten
            block = StringIO(lines[2])
            reader = csv.reader(block, quotechar='"')
            types = reader.__next__()
            attr = reader.__next__()
            for line in reader:
                val = [(a, cast_types_etgf(v, t)) for v, t, a in zip(line, types, attr) if v != '']
                # val[0][1] u, val[1][1] v, val[2][1] key
                G.add_edge(val[0][1], val[1][1], val[2][1], **dict(val[3:]))
            block.close()
    except Exception:
        util.write_log(f'The file {filepath} could not be read!\n')
        raise IOError(f'The file {filepath} could not be read!')

    return G


def write_graph(G: nx.MultiDiGraph, filepath: str, filename: str):
    """
    Schreibt den uebergebenen networkx.MultiDiGraph in eine Datei.
    Die Methode wird dabei durch die Endung im Dateipfade bestimmt.
    Unterstuetzt sind graphml, pickle und etgf Format
    :param G:
    :param filepath:
    :param filename:
    :return:
    """

    # Pruefe ob Dateipfad existiert
    if not os.path.isdir(filepath):
        raise IOError(f'Filepath: {filepath} does not exist.')
    if os.path.exists(f'{filepath}/{filename}'):
        raise IOError(f'Filename: {filename} must not exist at {filepath}.')

    extension = os.path.splitext(filename)[1]

    if extension == '.graphml':
        ox.save_graphml(G, f'{filepath}/{filename}')
    elif extension == '.pickle':
        with open(f'{filepath}/{filename}', 'wb') as f:
            pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)
    elif extension == '.etgf':
        write_graph_as_etgf(G, filepath, filename, True, False, False)
    else:
        raise IOError(f'File extension {extension} not supported')


"""
Generiert leere Ordner zum Speichern der Graphen
Gibt den Namen des Hauptordners 
"""
def gen_save_dirs(savepath, download, save_download, generate, save_generate, label):
    dirname = util.main_directory_title()+util.create_timestamp()
    os.chdir(savepath)
    if not os.listdir().__contains__(dirname):
        os.mkdir(dirname)
    os.chdir(os.path.join(savepath, dirname))
    if download & save_download:
        os.mkdir("download")
    if generate & save_generate:
        os.mkdir("generate")
    if label:
        os.mkdir("label")
    return dirname


def try_save_graph(G, filepath, mode, format, global_count, local_count, generate):
    filepath = os.path.join(filepath, mode)
    prefix = ""
    suffix = ""

    if format == SaveFormat.GRAPHML:
        extension = ".graphml"
    elif format == SaveFormat.PICKLE:
        extension = ".pickle"
    else:
        extension = ".etgf"

    name = G.graph['graphname']
    if mode == "label":
        if generate:
            prefix = str(global_count) + "_"
            suffix = "_" + str(local_count)
    if mode == "generate":
        # counter nutzen
        prefix = str(global_count)+"_"
        suffix = "_"+str(local_count)

    filename = prefix+name+suffix+extension
    write_graph(G, filepath, filename)
    os.chdir(util.default_directory)


class SaveFormat(Enum):
    GRAPHML = 1
    PICKLE = 2
    ETGF = 3


class SaveContext(Enum):
    DOWNLOAD = 1
    GENERATE = 2
    LABEL = 3
