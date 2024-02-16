# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "crawling data bhumi atrbpn"
        self.description = "- testing1 (on_progress)"

    def getParameterInfo(self):
        """Define the tool parameters."""
        params = [
            arcpy.Parameter(displayName="Folder json output crawling",
                            name="output_json_folder",
                            datatype="DEFolder",
                            parameterType="Required",
                            direction="Input"),
            
            arcpy.Parameter(displayName="Folder Shapefile Convert json",
                            name="folder_shp",
                            datatype="DEFolder",
                            parameterType="Required",
                            direction="Input"),
            
            arcpy.Parameter(displayName="Output Clean Data",
                            name="output_folder",
                            datatype="DEFolder",
                            parameterType="Required",
                            direction="Input"),
            
            arcpy.Parameter(displayName="Name Output Shapefile",
                            name="name_file_cleaned",
                            datatype="GPString",
                            parameterType="Required",
                            direction="Input"),
        ]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        output_json_folder = parameters[0].valueAsText
        folder_shp = parameters[1].valueAsText
        arcpy.env.workspace = output_json_folder
        output_folder = parameters[2].valueAsText
        name_file_cleaned = parameters[3].valueAsText
        
        for req1 in range(20, 200, 10):
            for req2 in range(30, 300, 10):
                url = f'https://bhumi.atrbpn.go.id/bhumigs/umum/wms?version=1.1.1&request=GetFeatureInfo&info_format=application/json&layers=umum:ZNTRANGE&CRS=EPSG:4326&width=1920&height=719&x={req1}&y={req2}&bbox=106.7944325208885,-6.2716550023889965,106.83795382073515,-6.255454471281453&query_layers=umum:ZNTRANGE&srs=EPSG:4326'
                
                try :
                    time.sleep(1)
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        output_json = response.json()

                        # Create a unique file name based on req1 and req2
                        output_file_path = f"{output_json_folder}\\req1_{req1}_req2_{req2}.json"

                        # Write the formatted JSON to the file
                        with open(output_file_path, 'w') as output_file:
                            json.dump(output_json, output_file, indent=2)

                        print(f"JSON response for req1={req1}, req2={req2} written to {output_file_path}")
                        arcpy.AddMessage("JSON response for req1={req1}, req2={req2} written to {output_file_path}")
                        time.sleep(1)
                    else:
                        print(f"Failed to fetch data for req1={req1}, req2={req2}. Status code: {response.status_code}")
                        arcpy.AddMessage("Failed to fetch data for req1={req1}, req2={req2}. Status code: {response.status_code}")
                except Exception as e :
                    print("Error/Bugs/MissingXYpixel")
                    
        time.sleep(5)
        
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
            arcpy.AddMessage("processing . . . JSON to Features")
            arcpy.conversion.JSONToFeatures(in_json_file=jsons, out_features=output_convtjson)
            
            # Add the converted feature class to the list
            converted_features.append(output_convtjson)
            arcpy.AddMessage("JSON to Features Done !!!")
            
        # Merge the converted JSON features into a single feature class
        output_merge = os.path.join(output_json_folder, "merged_output")
        arcpy.AddMessage('processing . . . Merged Raw Features')
        arcpy.management.Merge(inputs=converted_features, output=output_merge)
        arcpy.AddMessage('Merge Data Done !!!')
        
        arcpy.AddMessage('processing . . . Delete Identical/Duplicate')
        # Delete identical features based on the specified field
        arcpy.management.DeleteIdentical(in_dataset=output_merge, fields=["ZONANILAIT"])
        arcpy.AddMessage('Deleted Duplicated Data Done !!!')
            
            
        # Save the cleaned data to the output folder
        cleaned_output = os.path.join(output_folder, str(name_file_cleaned)) #name_file_cleaned = string
        arcpy.AddMessage('Saving Data . . . .')
        arcpy.management.CopyFeatures(in_features=output_merge, out_feature_class=cleaned_output)
            
        # Clean up intermediate data
        arcpy.management.Delete(output_merge)

        print("Script execution completed.")
        arcpy.AddMessage("Script execution completed.")            
                    
        #return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
