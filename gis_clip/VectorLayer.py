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
        self.output_dir = "../result/"
        if os.path.isdir(self.output_dir) != True:
            os.mkdir(self.output_dir)
        self.fr_point = ogr.CreateGeometryFromWkt("POINT(3414520.733 5319001.954)")        
        
    def read(self, dataType = "ESRI Shapefile"):
        """
        Read vector layer
        """
        # shapefile to read
        shapefile = self._path
        
        # driver of the input file
        self.input_driver = ogr.GetDriverByName(dataType)
        
        # open actual file
        self.input_datasource = self.input_driver.Open(shapefile)
        
        # get the layer(s) from the datasource
        self._layer = self.input_datasource.GetLayer()
        self.name = os.path.basename(self._path)
        
    def prepareOutput(self, filter_name, mask_epsg, dataType = "ESRI Shapefile"):
        """
        Prepare output layer
        """
        
        # driver for output
        self.output_driver = ogr.GetDriverByName(dataType)
        # set output file name
        filename, file_extension = os.path.splitext(self._path)
        new_filename =  self.output_dir + self.name.split(".")[0] + "_clipped"
        new_filename += "_" + ''.join([i for i in filter_name if i.isalpha()])
        print new_filename
        print self.output_dir
        # delete file if it already exists
        if os.path.exists(self.output_dir):
            r = glob.glob(new_filename + "*.*")
            for i in r:
                print "removed: ", i
                os.remove(i)
        
        # create output vector file, combine file name with filter
        self.output_datasource = self.output_driver.CreateDataSource(new_filename + 
            file_extension) #self.input_datasource.GetName())        
        
        # set spatial reference of output equal to the mask layer
        self.output_srs = osr.SpatialReference()
        self.output_srs.ImportFromEPSG(mask_epsg)
        self.resultLayer = self.output_datasource.CreateLayer("clipping_result", 
                                                         self.output_srs, ogr.wkbPolygon)
        
        # pass the attribute fields from the clipping layer to the output
        feature_defn = self._layer.GetLayerDefn()
        # get the names of the attributes
        self.attr_list = [feature_defn.GetFieldDefn(i).GetName() for i in
            range(feature_defn.GetFieldCount())]
        # get the types of the attributes
        self.attr_list_types = [feature_defn.GetFieldDefn(i).GetType() for i in
            range(feature_defn.GetFieldCount())]
        # add the attributes to the layer
        for i in range(len(self.attr_list)):
            field = ogr.FieldDefn(self.attr_list[i], self.attr_list_types[i])
            self.resultLayer.CreateField(field)

        # add the required extra fields        
        area_field = ogr.FieldDefn("AREA", ogr.OFTReal)
        self.resultLayer.CreateField(area_field)
        distance_field = ogr.FieldDefn("DISTANCE", ogr.OFTReal)
        self.resultLayer.CreateField(distance_field)
        
    def finalClip(self, clippingMask, toClip_transform):
        """
        actual clipping
        """
        # reset reading to avoid python crash and to reset pointer!
        clippingMask._layer.ResetReading()
        self._layer.ResetReading()
        # iterate over features of filtered mask layer
        for feature1 in clippingMask._layer:
            self._layer.ResetReading()
            geom1 = feature1.GetGeometryRef()
            # iterate over toClip features
            for feature2 in self._layer:
                geom2 = feature2.GetGeometryRef()
                geom2.Transform(toClip_transform)
                
                # compute intersection only if geometries intersect
                if geom2.Intersects(geom1):
                    print "Intersected"
                    intersection = geom2.Intersection(geom1)
                    # for each feature fill all attributes
                    dstfeature = ogr.Feature(self.resultLayer.GetLayerDefn())
                    dstfeature.SetGeometry(intersection)
                    for attr in self.attr_list:
                        field = feature2.GetField(str(attr))
                        dstfeature.SetField(attr, field)
                    dstfeature.SetField("AREA", intersection.Area())
                    
                    point_srs = osr.SpatialReference()
                    point_srs.ImportFromEPSG(31467)
                    point_transform = osr.CoordinateTransformation(point_srs, self.output_srs)
                    self.fr_point.Transform(point_transform)
                    dstfeature.SetField("DISTANCE", intersection.Distance(self.fr_point))
                    self.resultLayer.CreateFeature(dstfeature.Clone())
            
        # close and save new shapefile
        self.output_datasource.Destroy()
        
    def clipLayer(self, clippingMask, filter_name, mask_epsg, toClip_transform,
                  dataType = "ESRI Shapefile"):
        """
        procedure for layer clipping on the output layer
        """
        self.prepareOutput(filter_name, mask_epsg, dataType)
        self.finalClip(clippingMask, toClip_transform)