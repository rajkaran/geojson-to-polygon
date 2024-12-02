import json
import csv

# Specify the path to your JSON file
file_path = 'Municipal_Boundary_Ontario_small_chunk_1.json'  # Replace with your actual file path
output_csv_path = 'municipal_polygons_chunk_1.csv'  # Specify the output CSV file name

# Open the file for reading
with open(file_path, 'r') as file:
    # Load the JSON data
    data = json.load(file)

# Initialize a list to hold the municipality data and polygon data
municipal_data = []

# Check if 'features' is in the dictionary
if 'features' in data:
    features = data['features']  # Access the features array

    # Loop over the features
    for feature in features:
        # Extract fields for the CSV columns
        ogfId = feature['properties'].get('OGF_ID', None)
        municipalType = feature['properties'].get('MUNICIPAL_TYPE', '')
        municipalName = feature['properties'].get('MUNICIPAL_NAME', 'Unnamed')
        municipalAreaExtentType = feature['properties'].get('MUNICIPAL_AREA_EXTENT_TYPE', '')
        municipalNamePrefix = feature['properties'].get('MUNICIPAL_NAME_PREFIX', '')
        municipalNameShortform = feature['properties'].get('MUNICIPAL_NAME_SHORTFORM', '')
        upperTierMunicipality = feature['properties'].get('UPPER_TIER_MUNICIPALITY', '')

        # Extract geometry
        geojson_data = feature.get('geometry')

        if geojson_data is not None:
            geometry_type = geojson_data["type"]

            # Handle Polygon geometry
            if geometry_type == "Polygon":
                if geojson_data["coordinates"]:  # Check if coordinates are not empty
                    polygon_coordinates = geojson_data["coordinates"][0]  # Get the outer ring of the polygon

                    # Format coordinates into the desired string format
                    formatted_coordinates = ', '.join(f'{coord[0]} {coord[1]}' for coord in polygon_coordinates)

                    # Create the geometry string in WKT format
                    polygon_wkt = f'POLYGON (({formatted_coordinates}))'

                    # Append the row data for this municipality
                    municipal_data.append([ogfId, municipalType, municipalName, municipalAreaExtentType, 
                                           municipalNamePrefix, municipalNameShortform, upperTierMunicipality, polygon_wkt])

            # Handle MultiPolygon geometry
            elif geometry_type == "MultiPolygon":
                for polygon in geojson_data["coordinates"]:
                    if polygon:  # Check if this polygon has coordinates
                        polygon_coordinates = polygon[0]  # Get the outer ring of the polygon

                        # Format coordinates into the desired string format
                        formatted_coordinates = ', '.join(f'{coord[0]} {coord[1]}' for coord in polygon_coordinates)

                        # Create the geometry string in WKT format
                        polygon_wkt = f'POLYGON (({formatted_coordinates}))'

                        # Append the row data for this municipality
                        municipal_data.append([ogfId, municipalType, municipalName, municipalAreaExtentType, 
                                               municipalNamePrefix, municipalNameShortform, upperTierMunicipality, polygon_wkt])

# Save the municipality data to a CSV file compatible with SQLite
with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    # Write the header row
    csv_writer.writerow(['ogfId', 'municipalType', 'municipalName', 'municipalAreaExtentType', 
                         'municipalNamePrefix', 'municipalNameShortform', 'upperTierMunicipality', 'geometry'])

    # Write each row of municipality data
    for row in municipal_data:
        csv_writer.writerow(row)

print(f'Municipality data saved to {output_csv_path}')
