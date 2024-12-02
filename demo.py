import json

# Load your GeoJSON file
with open('Municipal_Boundary_Ontario_small_chunk_1.json', 'r') as f:
    geojson_data = json.load(f)

# Process each feature in the GeoJSON
for feature in geojson_data['features']:
    # Extract the coordinates (assuming we're dealing with polygons)
    polygon_coordinates = feature['geojson_data']['coordinates'][0]  # Adjust as needed for your GeoJSON structure

    # Unpack the coordinates, but only use the first two values (lon, lat)
    formatted_coordinates = ', '.join(f'{coord[0]} {coord[1]}' for coord in polygon_coordinates)

    # Continue processing your data as needed
    print(f"Formatted Coordinates for Feature: {formatted_coordinates}")
