# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:25:08 2016

@author: de.student
"""

import sys
from PyQt4 import QtCore, QtGui, uic
import glob
import os

 
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
           list = self.listView_toClip
           model = QtGui.QStandardItemModel(list)
           for file in glob.glob(dlg.directory().path() + "/*.shp"):
               item = QtGui.QStandardItem(os.path.basename(file))
               item.setCheckable(True)
               model.appendRow(item)
           list.setModel(model)
           list.show()
               
           
    def btn_toMask_clicked(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.ExistingFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.mask_path.setText(filenames[0].encode('utf8'))
           
    def btn_clip_clicked(self):
        clippingMask_layer_files = []
        for row in range(self.listView_toClip.model.rowCount()):
            item = self.listView_toClip.model.item(row)
            print item.text.encode('utf8')
            if item.checkState() == QtCore.Qt.Checked:
                clippingMask_layer_files.append(item.text)
                
                
        print str(clippingMask_layer_files)
                