import arcpy
import os

# Set the workspace to the folder containing JSON files
folder = r"C:\Users\bputra\OneDrive - ESRI Indonesia\PT ESRI Indonesia\Research\code-script\16_bhumi_atrbpn\data"
folder_shp = r"C:\Users\bputra\OneDrive - ESRI Indonesia\PT ESRI Indonesia\Research\code-script\16_bhumi_atrbpn\data_shp"
arcpy.env.workspace = folder

# Define output folder
output_folder = r"C:\Users\bputra\OneDrive - ESRI Indonesia\PT ESRI Indonesia\Research\code-script\16_bhumi_atrbpn\output"

# Create a scratch geodatabase for temporary storage
#scratch_gdb = arcpy.env.scratchGDB

arcpy.env.overwriteOutput = True  # Enable overwrite outputs

# Get a list of JSON files in the folder
data_json = arcpy.ListFiles("*.json")
print(data_json)

# List to store the converted feature classes
converted_features = []

# Loop through each JSON file
for jsons in data_json:
    
    # Convert JSON to feature class
    output_name = os.path.splitext(jsons)[0] + ".shp"
    output_convtjson = os.path.join(folder_shp, output_name)
    
    # Check if the output feature class already exists, and delete it
    if arcpy.Exists(output_convtjson):
        arcpy.management.Delete(output_convtjson)
    
    arcpy.conversion.JSONToFeatures(in_json_file=jsons, out_features=output_convtjson)
    
    # Add the converted feature class to the list
    converted_features.append(output_convtjson)
    
# Merge the converted JSON features into a single feature class
output_merge = os.path.join(folder, "merged_output")
arcpy.management.Merge(inputs=converted_features, output=output_merge)
    
# Delete identical features based on the specified field
arcpy.management.DeleteIdentical(in_dataset=output_merge, fields=["ZONANILAIT"])
    
# Save the cleaned data to the output folder
cleaned_output = os.path.join(output_folder, "clean_data_testing2.shp")
arcpy.management.CopyFeatures(in_features=output_merge, out_feature_class=cleaned_output)
    
# Clean up intermediate data
arcpy.management.Delete(output_merge)

print("Script execution completed.")

