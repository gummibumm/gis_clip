# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:25:08 2016

@author: de.student
"""

from PyQt4 import QtCore, QtGui, uic
import glob
import os
from osgeo import osr
from ClippingManager import ClippingManager

# load style of main_ui window from a xml like file - generated with
# QtDesigner
form_class = uic.loadUiType("./UI/main.ui")[0]

# derived subclass from QtGui.QMainWindow
class Main_ui(QtGui.QMainWindow, form_class):
    
    def __init__(self, parent=None):
        """
        initialize the main_ui window
        """
        QtGui.QMainWindow.__init__(self, parent)
        # initialize ui elements
        self.setupUi(self)
        # attach button event handler
        self.layer_clip_btn.clicked.connect(self.btn_toClip_clicked)
        self.layer_mask_btn.clicked.connect(self.btn_toMask_clicked)
        self.clip_btn.clicked.connect(self.btn_clip_clicked)
        # show the whole ui
        self.show()
    
    def btn_toClip_clicked(self):
        """
        Method to handle the event if the toClip button is pressed
        """
        # open file dialog
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.Directory)
        
        # after file dialog closed set ui elements
        if dlg.exec_():
            # show the path to the toClip folder
            self.clip_path.setText(dlg.directory().path())
            # init lists for available vector data and related epsg number
            list_toClip = self.listView_toClip
            list_EPSG = self.listView_EPSG
            self.model_toClip = QtGui.QStandardItemModel(list_toClip)
            self.model_EPSG = QtGui.QStandardItemModel(list_EPSG)
            # add entries to the two lists            
            for file_name in glob.glob(dlg.directory().path() + "/*.shp"):
                item_toClip = QtGui.QStandardItem(os.path.basename(file_name))
                item_toClip.setCheckable(True)
                item_EPSG = QtGui.QStandardItem(self.getEPSG(os.path.basename(file_name)))
                item_EPSG.setEditable(True)
                item_EPSG.setBackground(QtGui.QBrush(QtGui.QColor(240, 240, 240)))
                self.model_toClip.appendRow(item_toClip)
                self.model_EPSG.appendRow(item_EPSG)
            # finalize two lists and show in ui
            list_toClip.setModel(self.model_toClip)
            list_EPSG.setModel(self.model_EPSG)
            list_toClip.show()
            list_EPSG.show()
               
    def btn_toMask_clicked(self):
        """
        Method to handle the event if the toMask button is pressed
        """
        # open file dialog
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.ExistingFile)
        # after gile dialog is closed set ui elements
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.mask_path.setText(filenames[0].encode('utf8'))
    
    def btn_clip_clicked(self):
        """
        Method to handle the event if the clip button is pressed
        """
        self.progressBar.setValue(0)
        # evaluate ui elements:
        clippingMask_layer_files = []
        clipping_epsg = []
        for row in range(self.model_toClip.rowCount()):
            item = self.model_toClip.item(row)
            # get all checked vector files and related epsg number
            if item.checkState() == QtCore.Qt.Checked:
                clippingMask_layer_files.append(
                    self.clip_path.text().encode('utf8') + "/" +
                    item.text().encode('utf8'))
                clipping_epsg.append(int(self.model_EPSG.item(row).text().encode('utf8')))
        # get the mask layer and filter on this layer
        mask_layer_file = self.mask_path.text().encode('utf8')
        filter_string = self.filter_textEdit.toPlainText()
        # get the epsg number for the mask -> epsg gets main epsg for all results
        mask_epsg = int(self.textEdit_maskEPSG.toPlainText())
        # now start the clipping procedure
        ClippingManager.startClipping(clippingMask_layer_files, mask_layer_file, 
                                      filter_string, clipping_epsg, mask_epsg, self.progressBar)
        
    def getEPSG(self, file_name):
        """
        Method to get the epsg number from the prj file
        Input: filename
        Return: epsg number if available, 
                unknown if prj is available but now epsg authority,
                null if now prf is available
        """
        full_path = self.clip_path.text().encode('utf8') + "/" + file_name.split(".")[0] + ".prj"
        if os.path.exists(full_path):
            source = osr.SpatialReference()
            with open(full_path, "r") as fs:
                source.ImportFromWkt(fs.read())
                fs.close()
            epsg = source.GetAttrValue("AUTHORITY", 1)
            if epsg == "":
                return "Unknown"
            return epsg
        return "NaN"