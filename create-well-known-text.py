import json
import csv
from shapely.geometry import Polygon, MultiPolygon
from shapely import wkt

# Specify the path to your JSON file
file_path = 'Municipal_Boundary_Ontario_left_over_9.json'  # Replace with your actual file path
output_csv_path = 'results/Municipal_Boundary_Ontario_residual_9.csv'  # Specify the output CSV file name
# file_path = 'pastedv3.json'  # Replace with your actual file path
# output_csv_path = 'results/pasted.csv'  # Specify the output CSV file name

# Simplification tolerance (adjust this value as needed)
simplification_tolerance = 0.001  # Higher value = more simplification

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
            polygon_wkt = ""

            # Handle Polygon geometry
            if geometry_type == "Polygon":
                if geojson_data["coordinates"]:  # Check if coordinates are not empty
                    # Create a polygon with outer and inner rings
                    rings = geojson_data["coordinates"]  # List of coordinates
                    outer_ring = rings[0]  # First is the outer ring
                    inner_rings = rings[1:] if len(rings) > 1 else []  # Remaining are inner rings

                    # Create a Shapely Polygon
                    polygon = Polygon(outer_ring, inner_rings)

                    # Simplify the polygon
                    simplified_polygon = polygon.simplify(simplification_tolerance, preserve_topology=True)
                    polygon_wkt = simplified_polygon.wkt

            # Handle MultiPolygon geometry
            elif geometry_type == "MultiPolygon":
                polygons = []
                for polygon_coords in geojson_data["coordinates"]:
                    if polygon_coords:  # Check if this polygon has coordinates
                        outer_ring = polygon_coords[0]  # Get the outer ring of the polygon
                        inner_rings = polygon_coords[1:] if len(polygon_coords) > 1 else []  # Remaining are inner rings
                        
                        # Create a Shapely Polygon for each polygon with its inner rings
                        polygon = Polygon(outer_ring, inner_rings)
                        polygons.append(polygon)

                # Create MultiPolygon
                multipolygon = MultiPolygon(polygons)
                # Simplify the MultiPolygon
                simplified_multipolygon = multipolygon.simplify(simplification_tolerance, preserve_topology=True)
                polygon_wkt = simplified_multipolygon.wkt

            # Append the row data for this municipality
            if polygon_wkt:  # Ensure there is geometry
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
