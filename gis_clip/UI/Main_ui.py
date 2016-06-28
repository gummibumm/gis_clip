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

 
form_class = uic.loadUiType("./UI/main.ui")[0]                 # Load the UI
 
class Main_ui(QtGui.QMainWindow, form_class):
    model = QtGui.QStandardItemModel()
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.layer_clip_btn.clicked.connect(self.btn_toClip_clicked)
        self.layer_mask_btn.clicked.connect(self.btn_toMask_clicked)
        self.clip_btn.clicked.connect(self.btn_clip_clicked)
        self.show()
        
    def btn_toClip_clicked(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.Directory)
		
        if dlg.exec_():           
           self.clip_path.setText(dlg.directory().path())
           list_toClip = self.listView_toClip
           list_EPSG = self.listView_EPSG
           self.model_toClip = QtGui.QStandardItemModel(list_toClip)
           self.model_EPSG = QtGui.QStandardItemModel(list_EPSG)
           for file_name in glob.glob(dlg.directory().path() + "/*.shp"):
               item_toClip = QtGui.QStandardItem(os.path.basename(file_name))
               item_toClip.setCheckable(True)
               item_EPSG = QtGui.QStandardItem(self.getEPSG(os.path.basename(file_name)))
               item_EPSG.setEditable(True)
               item_EPSG.setBackground(QtGui.QBrush(QtGui.QColor(240, 240, 240)))
               self.model_toClip.appendRow(item_toClip)
               self.model_EPSG.appendRow(item_EPSG)
           list_toClip.setModel(self.model_toClip)
           list_EPSG.setModel(self.model_EPSG)
           list_toClip.show()
           list_EPSG.show()
               
           
    def btn_toMask_clicked(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.ExistingFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.mask_path.setText(filenames[0].encode('utf8'))
           
    def btn_clip_clicked(self):
        self.progressBar.setValue(0)
        clippingMask_layer_files = []
        clipping_epsg = []
        for row in range(self.model_toClip.rowCount()):
            item = self.model_toClip.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                clippingMask_layer_files.append(
                    self.clip_path.text().encode('utf8') + "/" +
                    item.text().encode('utf8'))
                clipping_epsg.append(int(self.model_EPSG.item(row).text().encode('utf8')))
        mask_layer_file = self.mask_path.text().encode('utf8')
        filter_string = self.filter_textEdit.toPlainText()
        mask_epsg = int(self.textEdit_maskEPSG.toPlainText())
        ClippingManager.startClipping(clippingMask_layer_files, mask_layer_file, 
                                      filter_string, clipping_epsg, mask_epsg, self.progressBar)
        
    def getEPSG(self, file_name):
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