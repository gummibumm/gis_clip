# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:31:10 2016

@author: Ruben Beck, Marcel Gangwisch
"""
#from ClippingManager import ClippingManager
from VectorLayer import VectorLayer
from osgeo import osr

# class to manage the whole clipping process: provides vector layers, epsg numbers, ...
class ClippingManager:
    
    # Singleton instance -> only one instanced object of this class
    __instance = None

    def __new__(cls, toClip_layer, clippingMask_layer, filter_string,
                layer_transformations, mask_epsg):
        """
        Singleton Constructor for the clipping manager:
        if object is available return this object, else construct new object, 
        save as instance and return it
        """
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, toClip_layer, clippingMask_layer, 
                                            filter_string, layer_transformations,
                                            mask_epsg)
            cls.__instance.name = "The one"
        return cls.__instance
    
    def __init__(self, toClip_layer, clippingMask_layer, filter_string,
                 layer_transformations, mask_epsg):
        """
        initialize object with member variables
        """
        # list with all layers to clip
        self.toClip_layer = toClip_layer
        # the mask layer
        self.clippingMask_layer = clippingMask_layer
        # the filter string for the mask layer
        self.filter_string = filter_string
        # all layer transformations from the toClip epsgs to the mask epsg
        self.layer_transformations = layer_transformations
        # the actual mask epsg number
        self.mask_epsg = mask_epsg

    def Clip(self):
        # handle filter string
        # each line corresponds to a new filter
        filter_lines = self.filter_string.split('\n')
        for filter_line in filter_lines:
            print "Trying to apply filter: " + filter_line
            # apply filter
            self.clippingMask_layer._layer.ResetReading()
            self.clippingMask_layer._layer.SetAttributeFilter(str(filter_line))
            transform_counter = 0
            # start clipping for each 
            for toClip in self.toClip_layer:
                toClip.clipLayer(self.clippingMask_layer, str(filter_line), 
                                 self.mask_epsg, self.layer_transformations[transform_counter])
                transform_counter += 1
                
    @staticmethod
    def startClipping(toClip_layer_files, clippingMask_layer_file, filter_string, 
                      clipping_epsg, mask_epsg, progressBar):
        """
        Callable static method with now object required 
        interpret all string from the ui and generate objects
        finally constructs ClippingManager
        """
        # container lists for objects
        toClip_layer = []
        layer_transformations = []
        
        # handle mask layer
        clippingMask_layer = VectorLayer(clippingMask_layer_file)
        project_srs = osr.SpatialReference()
        project_srs.ImportFromEPSG(mask_epsg)

        # handle toClip layers
        layer_counter = 0        
        for toClip_layer_file in toClip_layer_files:
            currentLayer = VectorLayer(toClip_layer_file)
            current_srs = osr.SpatialReference()
            current_srs.ImportFromEPSG(clipping_epsg[layer_counter])
            current_transform = osr.CoordinateTransformation(current_srs, project_srs)
            layer_transformations.append(current_transform)
            toClip_layer.append(currentLayer)
            layer_counter += 1
            progressBar.setValue((layer_counter / len(toClip_layer_files)) * 100)
        
        # construct instance of clipping manager
        clippingManager = ClippingManager(toClip_layer, clippingMask_layer, 
                                          filter_string, layer_transformations,
                                          mask_epsg)
                                          
        # continue with the clipping procedure                                          
        clippingManager.Clip()
                