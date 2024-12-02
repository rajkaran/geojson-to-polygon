import json

# Function to read the list from the text file
def read_municipality_list(file_path):
    with open(file_path, 'r') as file:
        municipality_list = [line.strip() for line in file]
    return municipality_list

# Function to split the large GeoJSON into smaller chunks
def split_geojson(input_file, output_prefix, municipality_list, chunk_size=50):
    # Load the entire GeoJSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Check if 'features' exist in the data
    if 'features' not in data:
        print("No 'features' found in the GeoJSON.")
        return

    # Access all features from the GeoJSON
    features = data['features']
    
    # Filter features based on the municipality_name list
    filtered_features = []
    for feature in features:
        municipality_name = feature['properties'].get('MUNICIPAL_NAME', 'Unnamed')
        if municipality_name in municipality_list:
            filtered_features.append(feature)

    # Split the filtered features list into smaller chunks
    for i in range(0, len(filtered_features), chunk_size):
        # Get the chunk of features
        chunk = filtered_features[i:i + chunk_size]
        
        # Prepare the output structure for each chunk, preserving original structure
        small_geojson = {
            "type": "FeatureCollection",
            "features": chunk  # Use the entire original feature object
        }
        
        # Define the output file name
        output_file = f'{output_prefix}_chunk_{i//chunk_size + 1}.json'
        
        # Write the small GeoJSON chunk to a new file
        with open(output_file, 'w') as out_file:
            json.dump(small_geojson, out_file, indent=2)
        
        print(f'Saved {output_file}')

# Specify the input GeoJSON file path, the municipality list file, and output prefix for the chunk files
input_geojson = 'Municipal_Boundary_Ontario.geojson'  # Replace with your actual GeoJSON file path
municipality_list_file = 'sgh_municipality_list.txt'  # Replace with your actual text file path
output_prefix = 'Municipal_Boundary_Ontario_small'    # Output file prefix

# Read the municipality list from the file
municipality_list = read_municipality_list(municipality_list_file)

# Call the function to filter and split the GeoJSON file into chunks of 50 records
split_geojson(input_geojson, output_prefix, municipality_list, chunk_size=10)
