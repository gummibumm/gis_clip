# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:03:49 2016

@author: Marcel Gangwisch, Ruben Beck
"""
from osgeo import ogr, osr
import os
import glob

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
        
        if os.path.exists("./output.shp"):
            if hasattr(self, 'output_datasource'):
                self.output_datasource.Destroy()
            r = glob.glob("./output.*")
            for i in r:
                os.remove(i)
        
        # output files
        self.output_datasource = self.output_driver.CreateDataSource("./output.shp") #self.input_datasource.GetName())        

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(31467)
        
        #self._layer.SetSpatialRef(srs)
        #clippingMask._layer.SetSpatialRef(srs)
        print "first ref: " + str(self._layer.GetSpatialRef())
        print "second ref: " + str(clippingMask._layer.GetSpatialRef())
        
        resultLayer = self.output_datasource.CreateLayer("clipping_result", srs, ogr.wkbPolygon) # geom_type = self._layer.GetGeomType())

        clippingMask._layer.SetAttributeFilter("NAME = 'Schwippe'")
        print "mask: " + str(self._layer.GetFeatureCount())
        print "ezg: " + str(clippingMask._layer.GetFeatureCount())
        
        for feature1 in clippingMask._layer:
            geom1 = feature1.GetGeometryRef()
            for feature2 in self._layer:
                geom2 = feature2.GetGeometryRef()
                # select only the intersections
                if geom1.Intersects(geom2):
                    print "Intersected"
                    intersection = geom1.Intersection(geom2)
                    dstfeature = ogr.Feature(resultLayer.GetLayerDefn())
                    dstfeature.SetGeometry(intersection)
                    resultLayer.CreateFeature(dstfeature)
        
        
        # self._layer.Clip(clippingMask._layer, result_layer = resultLayer)
        # one.Clip(two, result_layer = resultLayer)
        # intersection = one.Intersection(two)
        
        
            
        # close and save new shapefile
        self.output_datasource.Destroy()
        
    def setSelection(self, featureName_list):
        self.featureName_list = featureName_list
        
    def applyFilter(self):
        # _layer.SetAttributeFilter("Name = 'Mississippi River'")
        NotImplemented
        
                
        
