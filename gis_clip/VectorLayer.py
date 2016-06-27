# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:03:49 2016

@author: Marcel Gangwisch
"""
from osgeo import gdal, ogr, osr
import os
import sys

class VectorLayer(object):
    
    def __init__(self, path):
        self._path = path
        
    def read():
        # shapefile to read
        shapefile = self._path
        
        # driver of the input file
        esri_shape = ogr.GetDriverByName("ESRI Shapefile")
        
        # open actual file
        datasource = esri_shape.Open(shapefile)
        
        # get the layer(s) from the datasource
        _layer = datasource.GetLayer()
        
        # get geometry type of the layer => 3 = Polygon
        _layer.GetGeomType()
        
        # amount of features in the layer
        _layer.GetFeatureCount()
        
    def write(dataType = "ESRI Shapefile"):
        # driver for output
        esri_shape = ogr.GetDriverByName(dataType)
        
        # output files
        fb_muenster = esri_shape.CreateDataSource("./FB_muenster.shp")
        fb_muenster_buffer = esri_shape.CreateDataSource("./FB_muenster_buffer.shp")
        stalls_inside = esri_shape.CreateDataSource("./marktstaende_inside.shp")
        stalls_outside = esri_shape.CreateDataSource("./marktstaende_outside.shp")
        
        # create a new layers in UTM 32N
        muenster_lyr = fb_muenster.CreateLayer("Muenster", srs_32632, geom_type=ogr.wkbPolygon)
        muenster_buffer_lyr = fb_muenster_buffer.CreateLayer("Muenster_Buffer", srs_32632, geom_type=ogr.wkbPolygon)
        stalls_inside_lyr = stalls_inside.CreateLayer("Stalls_inside", srs_32632, geom_type=ogr.wkbPoint)
        stalls_outside_lyr = stalls_outside.CreateLayer("Stalls_outside", srs_32632, geom_type=ogr.wkbPoint)
        
        
        # Format definieren: the field name is of type string
        name_field = ogr.FieldDefn("NAME", ogr.OFTString)
        distance_field = ogr.FieldDefn("DISTANCE", ogr.OFTReal)
        
        # add field to layer
        stalls_inside_lyr.CreateField(name_field)
        stalls_inside_lyr.CreateField(distance_field)
        stalls_outside_lyr.CreateField(name_field)
        stalls_outside_lyr.CreateField(distance_field)
        
        ## add a new feature to the layer:
        # layer definition for feature
        muenster_defn = muenster_lyr.GetLayerDefn()
        muenster_buffer_defn = muenster_buffer_lyr.GetLayerDefn()
        stalls_inside_defn = stalls_inside_lyr.GetLayerDefn()
        stalls_outside_defn = stalls_outside_lyr.GetLayerDefn()
        
        # loop over all stalls
        for key, value in inside.iteritems():
            # stall is inside
            if value == True:
                feature = ogr.Feature(stalls_inside_defn)
                feature.SetField("NAME", key)
                feature.SetField("DISTANCE", distance[key])
                feature.SetGeometry(stalls[key])
                # add feature to corresponding layer
                stalls_inside_lyr.CreateFeature(feature)
            # stall is outside
            else:
                feature = ogr.Feature(stalls_outside_defn)
                feature.SetField("NAME", key)
                feature.SetField("DISTANCE", distance[key])
                feature.SetGeometry(stalls[key])
                # add feature to corresponding layer
                stalls_outside_lyr.CreateFeature(feature)
                
        
        muenster_feature = ogr.Feature(muenster_defn)
        muenster_feature.SetGeometry(muenster_poly)
        # add feature to layer
        muenster_lyr.CreateFeature(muenster_feature)
        
        muenster_buffer_feature = ogr.Feature(muenster_buffer_defn)
        muenster_buffer_feature.SetGeometry(muenster_buffer_poly)
        # add feature to layer
        muenster_buffer_lyr.CreateFeature(muenster_buffer_feature)
        
        # close and save new shapefile
        fb_muenster.Destroy()
        fb_muenster_buffer.Destroy()
        stalls_inside.Destroy()
        stalls_outside.Destroy()
                
        
