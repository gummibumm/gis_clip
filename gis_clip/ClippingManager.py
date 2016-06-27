# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:31:10 2016

@author: Ruben Beck, Marcel Gangwisch
"""
class ClippingManager:
    
    __instance = None
    clippingMask_layer = []
    toClip_layer = []

    def __new__(cls, toClip_layer, clippingMask_layer):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, toClip_layer, clippingMask_layer)
            cls.__instance.name = "The one"
        return cls.__instance
    
    def __init__(self, toClip_layer, clippingMask_layer):
        self.toClip_layer = toClip_layer
        self.clippingMask_layer = clippingMask_layer

    def Clip(self):
        for toClip in self.toClip_layer:
            for clippingMask in self.clippingMask_layer:
                # clippingMask.Filter()
                toClip.clipLayer(clippingMask)