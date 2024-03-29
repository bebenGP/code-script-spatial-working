# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2024-01-26 16:31:32
"""
import arcpy
def #  NOT  IMPLEMENTED# Function Body not implemented

def Model():  # Model
    
    data_json = arcpy.ListFiles("*.json")

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    data = "C:\\Users\\bputra\\OneDrive - ESRI Indonesia\\PT ESRI Indonesia\\Research\\code-script\\16_bhumi_atrbpn\\data"

    for File_json, Name in #  NOT  IMPLEMENTED(data, "*", "json", "NOT_RECURSIVE"):

        # Process: JSON To Features (JSON To Features) (conversion)
        output_req1_10_JSONToFeature_shp = "C:\\Users\\bputra\\OneDrive - ESRI Indonesia\\PT ESRI Indonesia\\Research\\code-script\\16_bhumi_atrbpn\\data\\output_req1_10_JSONToFeature.shp"
        arcpy.conversion.JSONToFeatures(in_json_file=File_json, out_features=output_req1_10_JSONToFeature_shp)

        # Process: Merge (Merge) (management)
        Output_Dataset = "C:\\Users\\bputra\\AppData\\Local\\Temp\\ArcGISProTemp22392\\Untitled\\Default.gdb\\Merge"
        arcpy.management.Merge(inputs=[output_req1_10_JSONToFeature_shp], output=Output_Dataset)

        # Process: Delete Identical (Delete Identical) (management)
        Merge_2_ = arcpy.management.DeleteIdentical(in_dataset=Output_Dataset, fields=["ZONANILAITANAHID"])[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\bputra\\AppData\\Local\\Temp\\ArcGISProTemp22392\\Untitled\\Default.gdb", workspace="C:\\Users\\bputra\\AppData\\Local\\Temp\\ArcGISProTemp22392\\Untitled\\Default.gdb"):
        Model()
