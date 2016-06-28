# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:05:30 2016

@author: Marcel Gangwisch, Ruben Beck
"""
from ClippingManager import ClippingManager
from VectorLayer import VectorLayer
from UI import Main_ui
from PyQt4 import QtCore, QtGui, uic
import sys



def main():
    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        window = Main_ui.Main_ui()
        sys.exit(app.exec_())

@staticmethod
def startClipping(toClip_layer_files, clippingMask_layer_file, filter_string):
    toClip_layer = []
    clipMaskLayer = VectorLayer(clippingMask_layer_file)
    for toClip_layer_file in toClip_layer_files:
        toClip_layer.append(VectorLayer(toClip_layer_file))
    
    clippingManager = ClippingManager(toClip_layer, clippingMask_layer, filter_string)
    clippingManager.Clip()
    
    
main()
    
    