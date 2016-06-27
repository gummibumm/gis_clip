# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:05:30 2016

@author: Marcel Gangwisch, Ruben Beck
"""
from ClippingManager import ClippingManager
from VectorLayer import VectorLayer

def main():
    clippingMask_layer_files = ["../Data/Einzugsgebiete/ezg.shp"]
    toClip_layer_files = ["../Data/NatVeg/opovbona.shp"]
    
    clippingMask_layer = []
    toClip_layer = []
    
    for clippingMask_layer_file in clippingMask_layer_files:
        clippingMask_layer.append(VectorLayer(clippingMask_layer_file))
    for toClip_layer_file in toClip_layer_files:
        toClip_layer.append(VectorLayer(toClip_layer_file))
    
    
    clippingManager = ClippingManager(toClip_layer, clippingMask_layer)
    clippingManager.Clip()
    
main()
    
    