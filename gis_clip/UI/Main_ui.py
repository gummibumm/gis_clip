# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:25:08 2016

@author: de.student
"""

import sys
from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("./UI/main.ui")[0]                 # Load the UI
 
class Main_ui(QtGui.QMainWindow, form_class):
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
           print "choosen path: " + dlg.directory().path()
           self.clip_path.setText(dlg.directory().path())
           
    def btn_toMask_clicked(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.Directory)
		
        if dlg.exec_():
           print "choosen path: " + dlg.directory().path()
           self.mask_path.setText(dlg.directory().path())
           
    def btn_clip_clicked(self):
        NotImplemented