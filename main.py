#!/usr/bin/env python
"""
Main
"""
import sys
from PySide2.QtWidgets import *
import gui

if __name__ == '__main__':
    app = QApplication()
    mainWin = gui.MainWindow()
    ret = app.exec_()
    sys.exit(ret)
