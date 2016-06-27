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
        
        resultLayer = self.output_datasource.CreateLayer("clipping_result", 
                                                         srs, ogr.wkbPolygon)
        clippingMask._layer.SetAttributeFilter("NAME = 'Schwippe'")
        
        feature_defn = self._layer.GetLayerDefn()
        attr_list = [feature_defn.GetFieldDefn(i).GetName() for i in
            range(feature_defn.GetFieldCount())]
        attr_list_types = [feature_defn.GetFieldDefn(i).GetType() for i in
            range(feature_defn.GetFieldCount())]
            
        for i in range(len(attr_list)):
            field = ogr.FieldDefn(attr_list[i], attr_list_types[i])
            resultLayer.CreateField(field)
            
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
                    for attr in attr_list:
                        field = feature2.GetField(str(attr))
                        dstfeature.SetField(attr, field)
                    resultLayer.CreateFeature(dstfeature)
            
        # close and save new shapefile
        self.output_datasource.Destroy()
        
    def setSelection(self, featureName_list):
        self.featureName_list = featureName_list
        
    def applyFilter(self):
        # _layer.SetAttributeFilter("Name = 'Mississippi River'")
        NotImplemented
        
                
        
