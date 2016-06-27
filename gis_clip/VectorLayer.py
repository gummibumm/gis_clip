# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:03:49 2016

@author: Marcel Gangwisch, Ruben Beck
"""
from osgeo import ogr, osr

class VectorLayer(object):
    
    def __init__(self, path):
        self._path = path
        self.read()
        
    def read(self, dataType = "ESRI Shapefile"):
        # shapefile to read
        shapefile = self._path
        
        # driver of the input file
        self.input_driver = ogr.GetDriverByName(dataType)
        
        # open actual file
        self.input_datasource = self.input_driver.Open(shapefile)
        
        # get the layer(s) from the datasource
        self._layer = self.input_datasource.GetLayer()
        
        
    def write(outputFilename, dataType = "ESRI Shapefile"):
        NotImplemented
        
    def clipLayer(self, clippingMask, dataType = "ESRI Shapefile"):
        # driver for output
        self.output_driver = ogr.GetDriverByName(dataType)
        
        # output files
        self.output_datasource = self.output_driver.CreateDataSource("./output.shp") #self.input_datasource.GetName())        

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(31467)
        
        resultLayer = self.output_datasource.CreateLayer("clipping_result", srs, geom_type = self._layer.GetGeomType())
        self._layer.Clip(clippingMask, resultLayer)
        
        # close and save new shapefile
        self.output_datasource.Destroy()
        
    def setSelection(self, featureName_list):
        self.featureName_list = featureName_list
        
    def applyFilter(self):
        # _layer.SetAttributeFilter("Name = 'Mississippi River'")
        NotImplemented
        
                
        
