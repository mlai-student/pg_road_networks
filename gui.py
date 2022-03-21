# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os.path
import sys
import traceback
import re
from PySide2 import QtCore, QtGui, QtWidgets

import util
from save_graph import SaveFormat

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'projektgruppe1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import graph_generator


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(482, 483)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gbDownload = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbDownload.sizePolicy().hasHeightForWidth())
        self.gbDownload.setSizePolicy(sizePolicy)
        self.gbDownload.setCheckable(True)
        self.gbDownload.setChecked(False)
        self.gbDownload.setObjectName("gbDownload")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gbDownload)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gbSave_D = QtWidgets.QGroupBox(self.gbDownload)
        self.gbSave_D.setCheckable(True)
        self.gbSave_D.setObjectName("gbSave_D")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gbSave_D)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.rdbGraphML_D = QtWidgets.QRadioButton(self.gbSave_D)
        self.rdbGraphML_D.setObjectName("rdbGraphML_D")
        self.verticalLayout_5.addWidget(self.rdbGraphML_D)
        self.rdbCSV_D = QtWidgets.QRadioButton(self.gbSave_D)
        self.rdbCSV_D.setObjectName("rdbCSV_D")
        self.verticalLayout_5.addWidget(self.rdbCSV_D)
        self.rdbPickle_D = QtWidgets.QRadioButton(self.gbSave_D)
        self.rdbPickle_D.setObjectName("rdbPickle_D")
        self.verticalLayout_5.addWidget(self.rdbPickle_D)
        self.gridLayout_5.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.gbSave_D, 6, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lblFileLocation_D = QtWidgets.QLabel(self.gbDownload)
        self.lblFileLocation_D.setObjectName("lblFileLocation_D")
        self.horizontalLayout_8.addWidget(self.lblFileLocation_D)
        self.editFileLocation_D = QtWidgets.QLineEdit(self.gbDownload)
        self.editFileLocation_D.setObjectName("editFileLocation_D")
        self.horizontalLayout_8.addWidget(self.editFileLocation_D)
        self.expFileLocation_D = QtWidgets.QToolButton(self.gbDownload)
        self.expFileLocation_D.setObjectName("expFileLocation_D")
        self.horizontalLayout_8.addWidget(self.expFileLocation_D)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 5, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lblInputCities_D = QtWidgets.QLabel(self.gbDownload)
        self.lblInputCities_D.setObjectName("lblInputCities_D")
        self.horizontalLayout_6.addWidget(self.lblInputCities_D)
        self.editInputCities_D = QtWidgets.QLineEdit(self.gbDownload)
        self.editInputCities_D.setObjectName("editInputCities_D")
        self.horizontalLayout_6.addWidget(self.editInputCities_D)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lblNumCities_D = QtWidgets.QLabel(self.gbDownload)
        self.lblNumCities_D.setObjectName("lblNumCities_D")
        self.horizontalLayout_5.addWidget(self.lblNumCities_D)
        self.editNumCities_D = QtWidgets.QSpinBox(self.gbDownload)
        self.editNumCities_D.setObjectName("editNumCities_D")
        self.horizontalLayout_5.addWidget(self.editNumCities_D)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lblMode_D = QtWidgets.QLabel(self.gbDownload)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMode_D.sizePolicy().hasHeightForWidth())
        self.lblMode_D.setSizePolicy(sizePolicy)
        self.lblMode_D.setObjectName("lblMode_D")
        self.horizontalLayout_4.addWidget(self.lblMode_D)
        self.cbMode_D = QtWidgets.QComboBox(self.gbDownload)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbMode_D.sizePolicy().hasHeightForWidth())
        self.cbMode_D.setSizePolicy(sizePolicy)
        self.cbMode_D.setEditable(False)
        self.cbMode_D.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.cbMode_D.setObjectName("cbMode_D")
        self.cbMode_D.addItem("")
        self.cbMode_D.addItem("")
        self.cbMode_D.addItem("")
        self.horizontalLayout_4.addWidget(self.cbMode_D)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 1)
        self.horizontalLayout.addWidget(self.gbDownload)
        self.gbGenerate = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbGenerate.sizePolicy().hasHeightForWidth())
        self.gbGenerate.setSizePolicy(sizePolicy)
        self.gbGenerate.setCheckable(True)
        self.gbGenerate.setChecked(False)
        self.gbGenerate.setObjectName("gbGenerate")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gbGenerate)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lblMode_G = QtWidgets.QLabel(self.gbGenerate)
        self.lblMode_G.setObjectName("lblMode_G")
        self.horizontalLayout_11.addWidget(self.lblMode_G)
        self.cbMode_G = QtWidgets.QComboBox(self.gbGenerate)
        self.cbMode_G.setObjectName("cbMode_G")
        self.cbMode_G.addItem("")
        self.cbMode_G.addItem("")
        self.cbMode_G.addItem("")
        self.cbMode_G.addItem("")
        self.horizontalLayout_11.addWidget(self.cbMode_G)
        self.gridLayout_3.addLayout(self.horizontalLayout_11, 2, 0, 1, 1)
        self.gbGraphProperties_G = QtWidgets.QGroupBox(self.gbGenerate)
        self.gbGraphProperties_G.setObjectName("gbGraphProperties_G")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.gbGraphProperties_G)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.rdbNodes_G = QtWidgets.QRadioButton(self.gbGraphProperties_G)
        self.rdbNodes_G.setObjectName("rdbNodes_G")
        self.verticalLayout_7.addWidget(self.rdbNodes_G)
        self.rdbEdges_G = QtWidgets.QRadioButton(self.gbGraphProperties_G)
        self.rdbEdges_G.setObjectName("rdbEdges_G")
        self.verticalLayout_7.addWidget(self.rdbEdges_G)
        self.boxPercentage_G = QtWidgets.QCheckBox(self.gbGraphProperties_G)
        self.boxPercentage_G.setObjectName("boxPercentage_G")
        self.verticalLayout_7.addWidget(self.boxPercentage_G)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.lblPercentage_G = QtWidgets.QLabel(self.gbGraphProperties_G)
        self.lblPercentage_G.setObjectName("lblPercentage_G")
        self.horizontalLayout_18.addWidget(self.lblPercentage_G)
        self.lblGraphSize_G = QtWidgets.QLabel(self.gbGraphProperties_G)
        self.lblGraphSize_G.setObjectName("lblGraphSize_G")
        self.horizontalLayout_18.addWidget(self.lblGraphSize_G)
        self.editGraphSize_G = QtWidgets.QSpinBox(self.gbGraphProperties_G)
        self.editGraphSize_G.setObjectName("editGraphSize_G")
        self.horizontalLayout_18.addWidget(self.editGraphSize_G)
        self.editPercentage_G = QtWidgets.QSpinBox(self.gbGraphProperties_G)
        self.editPercentage_G.setObjectName("editPercentage_G")
        self.horizontalLayout_18.addWidget(self.editPercentage_G)
        self.verticalLayout_7.addLayout(self.horizontalLayout_18)
        self.gridLayout_3.addWidget(self.gbGraphProperties_G, 5, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.lblRadius_G = QtWidgets.QLabel(self.gbGenerate)
        self.lblRadius_G.setObjectName("lblRadius_G")
        self.horizontalLayout_12.addWidget(self.lblRadius_G)
        self.editRadius_G = QtWidgets.QSpinBox(self.gbGenerate)
        self.editRadius_G.setObjectName("editRadius_G")
        self.horizontalLayout_12.addWidget(self.editRadius_G)
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 4, 0, 1, 1)
        self.gbBB_G = QtWidgets.QGroupBox(self.gbGenerate)
        self.gbBB_G.setObjectName("gbBB_G")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.gbBB_G)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.lblBBWidth_G = QtWidgets.QLabel(self.gbBB_G)
        self.lblBBWidth_G.setObjectName("lblBBWidth_G")
        self.horizontalLayout_16.addWidget(self.lblBBWidth_G)
        self.editBBWidth_G = QtWidgets.QSpinBox(self.gbBB_G)
        self.editBBWidth_G.setObjectName("editBBWidth_G")
        self.horizontalLayout_16.addWidget(self.editBBWidth_G)
        self.verticalLayout_6.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.lblBBHeight_G = QtWidgets.QLabel(self.gbBB_G)
        self.lblBBHeight_G.setObjectName("lblBBHeight_G")
        self.horizontalLayout_14.addWidget(self.lblBBHeight_G)
        self.editBBHeight_G = QtWidgets.QSpinBox(self.gbBB_G)
        self.editBBHeight_G.setObjectName("editBBHeight_G")
        self.horizontalLayout_14.addWidget(self.editBBHeight_G)
        self.verticalLayout_6.addLayout(self.horizontalLayout_14)
        self.gridLayout_6.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.gbBB_G, 5, 0, 1, 1)
        self.gbSave_G = QtWidgets.QGroupBox(self.gbGenerate)
        self.gbSave_G.setCheckable(True)
        self.gbSave_G.setObjectName("gbSave_G")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.gbSave_G)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.rdbGraphML_G = QtWidgets.QRadioButton(self.gbSave_G)
        self.rdbGraphML_G.setObjectName("rdbGraphML_G")
        self.verticalLayout_8.addWidget(self.rdbGraphML_G)
        self.rdbCSV_G = QtWidgets.QRadioButton(self.gbSave_G)
        self.rdbCSV_G.setObjectName("rdbCSV_G")
        self.verticalLayout_8.addWidget(self.rdbCSV_G)
        self.rdbPickle_G = QtWidgets.QRadioButton(self.gbSave_G)
        self.rdbPickle_G.setObjectName("rdbPickle_G")
        self.verticalLayout_8.addWidget(self.rdbPickle_G)
        self.gridLayout_3.addWidget(self.gbSave_G, 6, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lblSource_G = QtWidgets.QLabel(self.gbGenerate)
        self.lblSource_G.setObjectName("lblSource_G")
        self.horizontalLayout_10.addWidget(self.lblSource_G)
        self.editSource_G = QtWidgets.QLineEdit(self.gbGenerate)
        self.editSource_G.setObjectName("editSource_G")
        self.horizontalLayout_10.addWidget(self.editSource_G)
        self.expSource_G = QtWidgets.QToolButton(self.gbGenerate)
        self.expSource_G.setObjectName("expSource_G")
        self.horizontalLayout_10.addWidget(self.expSource_G)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        # CHanges
        self.horizontalLayoutG = QtWidgets.QHBoxLayout()
        self.horizontalLayoutG.setObjectName("horizontalLayoutG")
        self.lblCount_G = QtWidgets.QLabel(self.gbGenerate)
        self.lblCount_G.setObjectName("lblCount_G")
        self.horizontalLayoutG.addWidget(self.lblCount_G)
        self.editCount_G = QtWidgets.QSpinBox(self.gbGenerate)
        self.editCount_G.setObjectName("editCount_G")
        self.horizontalLayoutG.addWidget(self.editCount_G)
        self.gridLayout_3.addLayout(self.horizontalLayoutG, 3, 0, 1, 1)
        # Changes End
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 7, 0, 1, 1)
        self.horizontalLayout.addWidget(self.gbGenerate)
        self.gbLabel = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbLabel.sizePolicy().hasHeightForWidth())
        self.gbLabel.setSizePolicy(sizePolicy)
        self.gbLabel.setCheckable(True)
        self.gbLabel.setChecked(False)
        self.gbLabel.setObjectName("gbLabel")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gbLabel)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.lblSource_L = QtWidgets.QLabel(self.gbLabel)
        self.lblSource_L.setObjectName("lblSource_L")
        self.horizontalLayout_19.addWidget(self.lblSource_L)
        self.editSource_L = QtWidgets.QLineEdit(self.gbLabel)
        self.editSource_L.setObjectName("editSource_L")
        self.horizontalLayout_19.addWidget(self.editSource_L)
        self.expSource_L = QtWidgets.QToolButton(self.gbLabel)
        self.expSource_L.setObjectName("expSource_L")
        self.horizontalLayout_19.addWidget(self.expSource_L)
        self.verticalLayout_4.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.lblAmenities_L = QtWidgets.QLabel(self.gbLabel)
        self.lblAmenities_L.setObjectName("lblAmenities_L")
        self.horizontalLayout_20.addWidget(self.lblAmenities_L)
        self.editAmenities_L = QtWidgets.QLineEdit(self.gbLabel)
        self.editAmenities_L.setObjectName("editAmenities_L")
        self.horizontalLayout_20.addWidget(self.editAmenities_L)
        self.verticalLayout_4.addLayout(self.horizontalLayout_20)
        self.gbMetric_L = QtWidgets.QGroupBox(self.gbLabel)
        self.gbMetric_L.setObjectName("gbMetric_L")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.gbMetric_L)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.rdbEuclidean_L = QtWidgets.QRadioButton(self.gbMetric_L)
        self.rdbEuclidean_L.setObjectName("rdbEuclidean_L")
        self.verticalLayout_9.addWidget(self.rdbEuclidean_L)
        self.rdbNearestEdge_L = QtWidgets.QRadioButton(self.gbMetric_L)
        self.rdbNearestEdge_L.setObjectName("rdbNearestEdge_L")
        self.verticalLayout_9.addWidget(self.rdbNearestEdge_L)
        self.verticalLayout_4.addWidget(self.gbMetric_L)
        self.gbLabelType_L = QtWidgets.QGroupBox(self.gbLabel)
        self.gbLabelType_L.setObjectName("gbLabelType_L")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.gbLabelType_L)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.rdbCounter_L = QtWidgets.QRadioButton(self.gbLabelType_L)
        self.rdbCounter_L.setObjectName("rdbCounter_L")
        self.verticalLayout_10.addWidget(self.rdbCounter_L)
        self.rdbBinary_L = QtWidgets.QRadioButton(self.gbLabelType_L)
        self.rdbBinary_L.setObjectName("rdbBinary_L")
        self.verticalLayout_10.addWidget(self.rdbBinary_L)
        self.verticalLayout_4.addWidget(self.gbLabelType_L)
        self.gbSave_L = QtWidgets.QGroupBox(self.gbLabel)
        self.gbSave_L.setCheckable(True)
        self.gbSave_L.setObjectName("gbSave_L")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.gbSave_L)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.rdbGraphML_L = QtWidgets.QRadioButton(self.gbSave_L)
        self.rdbGraphML_L.setObjectName("rdbGraphML_L")
        self.verticalLayout_11.addWidget(self.rdbGraphML_L)
        self.rdbCSV_L = QtWidgets.QRadioButton(self.gbSave_L)
        self.rdbCSV_L.setObjectName("rdbCSV_L")
        self.verticalLayout_11.addWidget(self.rdbCSV_L)
        self.rdbPickle_L = QtWidgets.QRadioButton(self.gbSave_L)
        self.rdbPickle_L.setObjectName("rdbPickle_L")
        self.verticalLayout_11.addWidget(self.rdbPickle_L)
        self.verticalLayout_4.addWidget(self.gbSave_L)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.gbLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblSaveLocation = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSaveLocation.sizePolicy().hasHeightForWidth())
        self.lblSaveLocation.setSizePolicy(sizePolicy)
        self.lblSaveLocation.setObjectName("lblSaveLocation")
        self.horizontalLayout_2.addWidget(self.lblSaveLocation)
        self.editSaveLocation = QtWidgets.QLineEdit(self.centralwidget)
        self.editSaveLocation.setObjectName("editSaveLocation")
        self.horizontalLayout_2.addWidget(self.editSaveLocation)
        self.expSaveLocation = QtWidgets.QToolButton(self.centralwidget)
        self.expSaveLocation.setObjectName("expSaveLocation")
        self.horizontalLayout_2.addWidget(self.expSaveLocation)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.proceedButton = QtWidgets.QPushButton(self.centralwidget)
        self.proceedButton.setObjectName("proceedButton")
        self.horizontalLayout_3.addWidget(self.proceedButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lblErrorHint = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblErrorHint.sizePolicy().hasHeightForWidth())
        self.lblErrorHint.setSizePolicy(sizePolicy)
        self.lblErrorHint.setObjectName("lblErrorHint")
        self.verticalLayout.addWidget(self.lblErrorHint)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 482, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.gbDownload.toggled['bool'].connect(self.lblSource_G.setHidden)
        self.gbDownload.toggled['bool'].connect(self.editSource_G.setHidden)
        self.gbDownload.toggled['bool'].connect(self.expSource_G.setHidden)

        ###
        self.gbGenerate.toggled['bool'].connect(self.updateLabelSource)
        self.gbDownload.toggled['bool'].connect(self.updateLabelSource)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.cbMode_D.currentIndexChanged.connect(self.update_cbMode_D)

        self.cbMode_G.currentIndexChanged.connect(self.update_cbMode_G)

        self.boxPercentage_G.toggled.connect(self.updatePercentage)

        # Default-Werte für Sichtbarkeiten einzelner Elemente

        self.lblInputCities_D.setVisible(False)
        self.editInputCities_D.setVisible(False)

        self.lblFileLocation_D.setVisible(False)
        self.editFileLocation_D.setVisible(False)
        self.expFileLocation_D.setVisible(False)

        self.lblRadius_G.setVisible(False)
        self.editRadius_G.setVisible(False)

        self.gbBB_G.setVisible(False)

        self.lblPercentage_G.setVisible(False)
        self.editPercentage_G.setVisible(False)

        self.lblErrorHint.hide()

        #ErrorHint Schriftfarbe und Schriftgröße anpassen
        self.lblErrorHint.setFont(QFont('Arial', 10))
        self.lblErrorHint.setStyleSheet('color: darkRed')

        #Default-Werte für Save-Boxen
        self.gbSave_D.setChecked(False)
        self.gbSave_G.setChecked(False)
        self.gbSave_L.setChecked(False)


        #Default-Werte für Radiobuttons
        self.rdbGraphML_L.setChecked(True)
        self.rdbGraphML_G.setChecked(True)
        self.rdbGraphML_D.setChecked(True)

        self.rdbNodes_G.setChecked(True)
        self.rdbEuclidean_L.setChecked(True)
        self.rdbCounter_L.setChecked(True)

        #Valide Werte für Input-Felder
        self.editNumCities_D.setMinimum(1)
        self.editNumCities_D.setMaximum(35263)

        self.editBBWidth_G.setMinimum(1)
        self.editBBWidth_G.setMaximum(1000000)

        self.editBBHeight_G.setMinimum(1)
        self.editBBHeight_G.setMaximum(1000000)

        self.editRadius_G.setMinimum(1)
        self.editRadius_G.setMaximum(1000000)

        self.editGraphSize_G.setMinimum(1)
        self.editGraphSize_G.setMaximum(1000000)

        self.editPercentage_G.setMinimum(1)
        self.editPercentage_G.setMaximum(100)
        
        self.editCount_G.setMinimum(1)

        self.editCount_G.setMaximum(1000000)

        # File Dialog oeffnen
        self.expSaveLocation.clicked.connect(self.fileDialogSaveLocation)
        self.expSource_L.clicked.connect(self.fileDialogSource_L)
        self.expSource_G.clicked.connect(self.fileDialogSource_G)
        self.expFileLocation_D.clicked.connect(self.fileDialogSource_D)

        self.proceedButton.clicked.connect(self.proceed)

        self.worker = None


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", util.app_title()))
        self.gbDownload.setTitle(_translate("MainWindow", "Download"))
        self.gbSave_D.setTitle(_translate("MainWindow", "Save"))
        self.rdbGraphML_D.setText(_translate("MainWindow", "graphml"))
        self.rdbCSV_D.setText(_translate("MainWindow", "etgf"))
        self.rdbPickle_D.setText(_translate("MainWindow", "pickle"))
        self.lblFileLocation_D.setText(_translate("MainWindow", "File location:"))
        self.expFileLocation_D.setText(_translate("MainWindow", "..."))
        self.lblInputCities_D.setText(_translate("MainWindow", "Input cities:"))
        self.lblNumCities_D.setText(_translate("MainWindow", "Number of random cities:"))
        self.lblMode_D.setText(_translate("MainWindow", "Mode:"))
        self.cbMode_D.setItemText(0, _translate("MainWindow", "Random"))
        self.cbMode_D.setItemText(1, _translate("MainWindow", "From Text Input"))
        self.cbMode_D.setItemText(2, _translate("MainWindow", "From File"))
        self.gbGenerate.setTitle(_translate("MainWindow", "Generate"))
        self.lblMode_G.setText(_translate("MainWindow", "Mode:"))
        self.cbMode_G.setItemText(0, _translate("MainWindow", "BFS"))
        self.cbMode_G.setItemText(1, _translate("MainWindow", "Compact BFS"))
        self.cbMode_G.setItemText(2, _translate("MainWindow", "Radius"))
        self.cbMode_G.setItemText(3, _translate("MainWindow", "Bounding Box"))
        self.gbGraphProperties_G.setTitle(_translate("MainWindow", "Graph properties"))
        self.rdbNodes_G.setText(_translate("MainWindow", "By nodes"))
        self.rdbEdges_G.setText(_translate("MainWindow", "By edges"))
        self.boxPercentage_G.setText(_translate("MainWindow", "By percentage"))
        self.lblPercentage_G.setText(_translate("MainWindow", "Percentage:"))
        self.lblGraphSize_G.setText(_translate("MainWindow", "Size:"))
        self.lblRadius_G.setText(_translate("MainWindow", "Radius:"))
        self.gbBB_G.setTitle(_translate("MainWindow", "Bounding Box properties"))
        self.lblBBWidth_G.setText(_translate("MainWindow", "Width:"))
        self.lblBBHeight_G.setText(_translate("MainWindow", "Height:"))
        self.gbSave_G.setTitle(_translate("MainWindow", "Save"))
        self.rdbGraphML_G.setText(_translate("MainWindow", "graphml"))
        self.rdbCSV_G.setText(_translate("MainWindow", "etgf"))
        self.rdbPickle_G.setText(_translate("MainWindow", "pickle"))
        self.lblSource_G.setText(_translate("MainWindow", "Source:"))
        self.expSource_G.setText(_translate("MainWindow", "..."))
        self.gbLabel.setTitle(_translate("MainWindow", "Label"))
        self.lblSource_L.setText(_translate("MainWindow", "Source:"))
        self.expSource_L.setText(_translate("MainWindow", "..."))
        self.lblAmenities_L.setText(_translate("MainWindow", "Input amenities:"))
        self.gbMetric_L.setTitle(_translate("MainWindow", "Choose metric"))
        self.rdbEuclidean_L.setText(_translate("MainWindow", "Euclidean distance"))
        self.rdbNearestEdge_L.setText(_translate("MainWindow", "Nearest edge"))
        self.gbLabelType_L.setTitle(_translate("MainWindow", "Labelling type"))
        self.rdbCounter_L.setText(_translate("MainWindow", "Counter"))
        self.rdbBinary_L.setText(_translate("MainWindow", "Binary"))
        self.gbSave_L.setTitle(_translate("MainWindow", "Save"))
        self.rdbGraphML_L.setText(_translate("MainWindow", "graphml"))
        self.rdbCSV_L.setText(_translate("MainWindow", "etgf"))
        self.rdbPickle_L.setText(_translate("MainWindow", "pickle"))
        self.lblSaveLocation.setText(_translate("MainWindow", "Save location:"))
        self.expSaveLocation.setText(_translate("MainWindow", "..."))
        self.proceedButton.setText(_translate("MainWindow", "Proceed"))
        self.lblErrorHint.setText(_translate("MainWindow", "ErrorHint"))
        self.lblCount_G.setText(_translate("MainWindow", "Count:"))
        
    def input_to_save_format(self, graphml, pickle, etgf):
        if graphml: return SaveFormat.GRAPHML
        if pickle: return SaveFormat.PICKLE
        if etgf: return SaveFormat.ETGF

    def proceed(self):
        self.lblErrorHint.hide()
        save_download = self.gbSave_D.isChecked()
        save_generate = self.gbSave_G.isChecked()
        save_label = self.gbSave_L.isChecked()
        format_download = self.input_to_save_format(self.rdbGraphML_D.isChecked(), self.rdbPickle_D.isChecked(), self.rdbCSV_D.isChecked())
        format_generate = self.input_to_save_format(self.rdbGraphML_G.isChecked(), self.rdbPickle_G.isChecked(), self.rdbCSV_G.isChecked())
        format_label = self.input_to_save_format(self.rdbGraphML_L.isChecked(), self.rdbPickle_L.isChecked(), self.rdbCSV_L.isChecked())

        if not (self.gbDownload.isChecked() or self.gbGenerate.isChecked() or self.gbLabel.isChecked()):
            self.setErrorHint('Error: Nothing to be done. No tasks (Download, Generate, Label) selected.')
            return

        if self.gbDownload.isChecked():
            if self.cbMode_D.currentIndex() == 1:
                if self.editInputCities_D.text() == '':
                    self.setErrorHint("Error: Field 'Input cities' is empty, enter at least one city to proceed.")
                    return
            if self.cbMode_D.currentIndex() == 2:
                if self.editFileLocation_D.text() == '':
                    self.setErrorHint("Error: Field 'File location' is empty, enter a source folder to proceed.")
                    return
                elif not os.path.isfile(self.editFileLocation_D.text()):
                    self.setErrorHint('Error: The specified path in Download is not a file or does not exist!')
                    return
                
        elif self.gbGenerate.isChecked():
            if self.editSource_G.text() == '':
                self.setErrorHint("Error: Field 'Source' is empty, enter a source folder to proceed")
                return
        else:
            if self.editSource_L.text() == '':
                self.setErrorHint("Error: Field 'Source' is empty, enter a source folder to proceed")
                return
            
        if self.gbLabel.isChecked():
            if self.editAmenities_L.text() == '':
                self.setErrorHint("Error: List of amenities is empty, there needs to be at least one amenity if 'Label' is checked.")
                return
        if self.editSaveLocation.text() == '':
            self.setErrorHint("Error: Field 'save location' is empty.")
            return
        else:
            if not os.path.isdir(self.editSaveLocation.text()):
                self.setErrorHint("Error: The specified 'save location' path does not exist!")
                return
        
        if not self.gbSave_D.isChecked() and not self.gbSave_G.isChecked() and  not self.gbSave_L.isChecked():
            self.setErrorHint("Error: Save needs to be activated for at least one mode in order to continue.")
            return

        if self.worker is not None and self.worker.isRunning():#self.threadpool.activeThreadCount() == 1:
            self.setErrorHint("Error: The program is already running. To proceed with new configurations either wait until it has finished or restart "+util.app_title()+".")
            return

        # Pruefe, ob input cities in richtigen Format sind (stadt,land;stadt,land; ....)
        if self.cbMode_D.currentIndex() == 1 and not re.fullmatch(r"([ ]*\w(\w|[ ])*,[ ]*\w(\w|[ ])*)(;([ ]*\w(\w|[ ])*,[ ]*\w(\w|[ ])*))*", self.editInputCities_D.text().rstrip(';'), re.U):
            self.setErrorHint('Error: Cities in wrong format. Correct: city,country;city,country;...')
            return

        # Pruefe, ob amenities im richtigen Format sind (amenity1,amenity2, ...
        if self.gbLabel.isChecked() and not re.fullmatch(r"([^\d\W]+)(,|(,[^\d\W]+)*)", self.editAmenities_L.text()):
            self.setErrorHint('Error: Amenities in wrong format. Correct: amenity1,amenity2,...')
            return

        # Worker fuer Multithreading
        self.worker = Worker(graph_generator.run_program, self.gbDownload.isChecked(), self.cbMode_D.currentIndex(),
                        self.editNumCities_D.value(), self.editInputCities_D.text(), self.editFileLocation_D.text(),
                        self.gbGenerate.isChecked(), self.cbMode_G.currentIndex(), self.editSource_G.text(),
                        self.editCount_G.value(), self.editGraphSize_G.value(), self.editGraphSize_G.value(),
                        self.rdbNodes_G.isChecked(), self.editRadius_G.value(), self.editBBWidth_G.value(),
                        self.editBBHeight_G.value(), self.gbLabel.isChecked(), self.editSource_L.text(),
                        self.rdbEuclidean_L.isChecked(), self.rdbBinary_L.isChecked(), self.editAmenities_L.text(),
                        save_download, format_download, save_generate, format_generate, save_label, format_label,
                        self.editSaveLocation.text(), self.boxPercentage_G.isChecked(),
                        self.editPercentage_G.value())
        self.worker.signals.start.connect(self.thread_started)
        self.worker.signals.finished.connect(self.thread_finished)
        self.worker.signals.error.connect(self.thread_error)

        self.worker.start()


    def setErrorHint(self, text):
        self.lblErrorHint.show()
        self.lblErrorHint.setText(text)

    def update_cbMode_D(self, value):
        if value == 0:
            self.lblNumCities_D.setVisible(True)
            self.editNumCities_D.setVisible(True)

            self.lblInputCities_D.setVisible(False)
            self.editInputCities_D.setVisible(False)

            self.lblFileLocation_D.setVisible(False)
            self.editFileLocation_D.setVisible(False)
            self.expFileLocation_D.setVisible(False)

        elif value == 1:
            self.lblNumCities_D.setVisible(False)
            self.editNumCities_D.setVisible(False)

            self.lblInputCities_D.setVisible(True)
            self.editInputCities_D.setVisible(True)

            self.lblFileLocation_D.setVisible(False)
            self.editFileLocation_D.setVisible(False)
            self.expFileLocation_D.setVisible(False)

        elif value == 2:
            self.lblNumCities_D.setVisible(False)
            self.editNumCities_D.setVisible(False)

            self.lblInputCities_D.setVisible(False)
            self.editInputCities_D.setVisible(False)

            self.lblFileLocation_D.setVisible(True)
            self.editFileLocation_D.setVisible(True)
            self.expFileLocation_D.setVisible(True)

    def update_cbMode_G(self, value):
        if value <= 1:
            self.lblRadius_G.setVisible(False)
            self.editRadius_G.setVisible(False)

            self.gbBB_G.setVisible(False)

            self.gbGraphProperties_G.setVisible(True)

        elif value == 2:
            self.lblRadius_G.setVisible(True)
            self.editRadius_G.setVisible(True)

            self.gbBB_G.setVisible(False)

            self.gbGraphProperties_G.setVisible(False)

        elif value == 3:
            self.lblRadius_G.setVisible(False)
            self.editRadius_G.setVisible(False)

            self.gbBB_G.setVisible(True)

            self.gbGraphProperties_G.setVisible(False)


    def updatePercentage(self):
        if self.boxPercentage_G.isChecked():
            self.lblGraphSize_G.setVisible(False)
            self.editGraphSize_G.setVisible(False)

            self.lblPercentage_G.setVisible(True)
            self.editPercentage_G.setVisible(True)
        else:
            self.lblGraphSize_G.setVisible(True)
            self.editGraphSize_G.setVisible(True)

            self.lblPercentage_G.setVisible(False)
            self.editPercentage_G.setVisible(False)

    def updateLabelSource(self):
        if self.gbDownload.isChecked() or self.gbGenerate.isChecked():
            self.lblSource_L.setVisible(False)
            self.editSource_L.setVisible(False)
            self.expSource_L.setVisible(False)
        else:
            self.lblSource_L.setVisible(True)
            self.editSource_L.setVisible(True)
            self.expSource_L.setVisible(True)


    def fileDialogSaveLocation(self):
        dialog = QFileDialog(self.centralwidget)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dir = dialog.getExistingDirectory()
        self.editSaveLocation.setText(dir)

    def fileDialogSource_D(self):
        dialog = QFileDialog(self.centralwidget)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Text files (*.txt *.csv)")
        if dialog.exec_():
            [filename] = dialog.selectedFiles()
            self.editFileLocation_D.setText(filename)

    def fileDialogSource_G(self):
        dialog = QFileDialog(self.centralwidget)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dir = dialog.getExistingDirectory()
        self.editSource_G.setText(dir)

    def fileDialogSource_L(self):
        dialog = QFileDialog(self.centralwidget)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dir = dialog.getExistingDirectory()
        self.editSource_L.setText(dir)

    def thread_started(self):
        self.proceedButton.setText('Running...')

    def thread_finished(self):
        self.proceedButton.setText('Proceed')
        self.lblErrorHint.setText('')

    def thread_error(self, error_info):
        if error_info[0] == OSError:
            self.setErrorHint(error_info[1].args[0])

        msg = QMessageBox()
        msg.setWindowTitle("Oh no!")
        msg.setText("An unhandled exception occured!")
        msg.setIcon(QMessageBox.Critical)
        msg.setDetailedText(error_info[2])
        msg.exec_()



class WorkerSignals(QObject):
    """
    Definiert verfuegbare Signale von einem WorkerThread

    start: Thread gestartet
    finished: Thread beendet
    error : Fehler aufgetreten
        tuple (exctype, value, traceback.format_exc() )
    """

    start = QtCore.Signal()
    finished = QtCore.Signal()  # QtCore.Signal
    error = QtCore.Signal(tuple)


class Worker(QThread):
    """
    Worker thread

    :param callback: Callback function die auf dem Thread laufen soll
    :type callback: function
    :param args: Parameter fuer callback Funktion
    """

    def __init__(self, fn, *args):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    @QtCore.Slot()  # QtCore.Slot
    def run(self):
        """
        Runner initialisieren
        """

        self.signals.start.emit()
        try:
            self.fn(*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.worker.quit()
            event.accept()