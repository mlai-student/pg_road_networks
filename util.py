#!/usr/bin/env python
"""
Diverse Hilfsfunktionen
"""

from datetime import datetime
import os

# Das default working directory
default_directory = os.getcwd()
log_file_path = None

def create_timestamp():
    """Erstellt einen timestamp für die Benennung von Dateien"""
    # current date and time
    now = datetime.now().__str__()
    timestamp = now.replace(":",".").replace(" ", "_")
    return timestamp


def app_title():
    """Gibt den Namen des Programmes aus"""
    return "Graphus Generatus"

def main_directory_title():
    """Namen des neuen Verzeichnisses, in welchem Graphen generiert werden"""
    return "graphs_"

def write_log(message: str):
    """Schreibt message an das Ende der log Datei"""
    with open(log_file_path, 'a') as f:
        f.write(message)
