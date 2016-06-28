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
        #self._path is the absolute path
        self._path = path
        self.read()
        self.output_dir = "../result"
        if os.path.isdir(self.output_dir) != True:
            os.mkdir(self.output_dir)
        self.fr_point = ogr.CreateGeometryFromWkt("POINT(3414520.733 5319001.954)")        
        
    def read(self, dataType = "ESRI Shapefile"):
        # shapefile to read
        shapefile = self._path
        
        # driver of the input file
        self.input_driver = ogr.GetDriverByName(dataType)
        
        # open actual file
        self.input_datasource = self.input_driver.Open(shapefile)
        
        # get the layer(s) from the datasource
        self._layer = self.input_datasource.GetLayer()
        self.name = os.path.basename(self._path)
        
        
    def write(outputFilename, dataType = "ESRI Shapefile"):
        NotImplemented
        
    def clipLayer(self, clippingMask, filter_name, mask_epsg, toClip_transform,
                  dataType = "ESRI Shapefile"):
        ##
        ## Prepare out
        ##
        # driver for output
        self.output_driver = ogr.GetDriverByName(dataType)
        filename, file_extension = os.path.splitext(self._path)
        new_filename =  self.output_dir + "/" + self.name.split(".")[0] + "_clipped"
        if os.path.exists(new_filename + file_extension):
            if hasattr(self, 'output_datasource'):
                self.output_datasource.Destroy()
            r = glob.glob("./" + new_filename + ".*")
            for i in r:
                os.remove(i)
        
        # output files
        self.output_datasource = self.output_driver.CreateDataSource(new_filename + 
            "_" + ''.join([i for i in filter_name if i.isalpha()]) + file_extension) #self.input_datasource.GetName())        
        
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(mask_epsg)
        resultLayer = self.output_datasource.CreateLayer("clipping_result", 
                                                         srs, ogr.wkbPolygon)
        
        feature_defn = self._layer.GetLayerDefn()
        attr_list = [feature_defn.GetFieldDefn(i).GetName() for i in
            range(feature_defn.GetFieldCount())]
        attr_list_types = [feature_defn.GetFieldDefn(i).GetType() for i in
            range(feature_defn.GetFieldCount())]
            
        for i in range(len(attr_list)):
            field = ogr.FieldDefn(attr_list[i], attr_list_types[i])
            resultLayer.CreateField(field)
        area_field = ogr.FieldDefn("AREA", ogr.OFTReal)
        resultLayer.CreateField(area_field)
        distance_field = ogr.FieldDefn("DISTANCE", ogr.OFTReal)
        resultLayer.CreateField(distance_field)

        ##
        ## actual clipping
        ##
        clippingMask._layer.ResetReading()
        for feature1 in clippingMask._layer:
            self._layer.ResetReading()
            # print len(clippingMask._layer)
            geom1 = feature1.GetGeometryRef()
            # print "Clippingmask: ", clippingMask._layer.GetFeatureCount()
            # print "toclip: ", self._layer.GetFeatureCount()
            
            for feature2 in self._layer:
                geom2 = feature2.GetGeometryRef()
                geom2.Transform(toClip_transform)
                
                # select only the intersections
                if geom2.Intersects(geom1):
                    print "Intersected"
                    intersection = geom2.Intersection(geom1)
                    dstfeature = ogr.Feature(resultLayer.GetLayerDefn())
                    dstfeature.SetGeometry(intersection)
                    for attr in attr_list:
                        field = feature2.GetField(str(attr))
                        dstfeature.SetField(attr, field)
                    dstfeature.SetField("AREA", intersection.Area())
                    
                    point_srs = osr.SpatialReference()
                    point_srs.ImportFromEPSG(31467)
                    point_transform = osr.CoordinateTransformation(point_srs, srs)
                    self.fr_point.Transform(point_transform)
                    dstfeature.SetField("DISTANCE", intersection.Distance(self.fr_point))
                    resultLayer.CreateFeature(dstfeature.Clone())
            
        # close and save new shapefile
        self.output_datasource.Destroy()
        
    def setSelection(self, featureName_list):
        self.featureName_list = featureName_list
        
                
        
