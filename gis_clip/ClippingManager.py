# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:31:10 2016

@author: Ruben Beck, Marcel Gangwisch
"""
#from ClippingManager import ClippingManager
from VectorLayer import VectorLayer

class ClippingManager:
    
    __instance = None

    def __new__(cls, toClip_layer, clippingMask_layer, filter_string):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, toClip_layer, clippingMask_layer, filter_string)
            cls.__instance.name = "The one"
        return cls.__instance
    
    def __init__(self, toClip_layer, clippingMask_layer, filter_string):
        self.toClip_layer = toClip_layer
        self.clippingMask_layer = clippingMask_layer
        self.filter_string = filter_string

    def Clip(self):
        filter_lines = self.filter_string.split('\n')
        for filter_line in filter_lines:
            print "Trying to apply filter: " + filter_line
            self.clippingMask_layer._layer.SetAttributeFilter(str(filter_line))
            for toClip in self.toClip_layer:
                toClip.clipLayer(self.clippingMask_layer)
                
    @staticmethod
    def startClipping(toClip_layer_files, clippingMask_layer_file, filter_string):
        toClip_layer = []
        clippingMask_layer = VectorLayer(clippingMask_layer_file)
        print str(toClip_layer_files)
        for toClip_layer_file in toClip_layer_files:
            toClip_layer.append(VectorLayer(toClip_layer_file))
        
        clippingManager = ClippingManager(toClip_layer, clippingMask_layer, filter_string)
        clippingManager.Clip()
                