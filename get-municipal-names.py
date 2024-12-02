import json
import csv

# Specify the path to your JSON file
file_path = 'Municipal_Boundary_Ontario.geojson'  # Replace with your actual file path
output_csv_path = 'municipal_names.csv'  # Specify the output CSV file name

# Open the file for reading
with open(file_path, 'r') as file:
    # Load the JSON data
    data = json.load(file)

# Initialize a list to hold the municipality names
municipality_names = []

# Check if 'features' is in the dictionary
if 'features' in data:
    features = data['features']  # Access the features array

    # Loop over the features
    for feature in features:
        # Extract the municipality name (assuming it's in properties)
        municipality_name = feature['properties'].get('MUNICIPAL_NAME', 'Unnamed')
        
        # Append the municipality name to the list
        municipality_names.append([municipality_name])

# Save the municipality names to a CSV file
with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['municipality_name'])  # Write header

    # Write each municipality name to a new row
    for name in municipality_names:
        csv_writer.writerow(name)

print(f'Municipality names saved to {output_csv_path}')
