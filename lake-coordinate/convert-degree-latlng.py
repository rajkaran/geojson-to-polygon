import sqlite3
import re

# Function to convert DMS (Degrees, Minutes, Seconds) to decimal degrees
def dms_to_decimal(coord, is_longitude=False):
    # Match patterns for degrees, minutes, seconds
    pattern = r"(\d+)[°º](?:\s*(\d+)[′']?)?(?:\s*(\d+(?:\.\d+)?)[″\"]?)?\s*([NSEW]?)"
    match = re.match(pattern, coord.strip())
    if not match:
        return None  # Return None if no match

    degrees = int(match.group(1))
    minutes = int(match.group(2) or 0)
    seconds = float(match.group(3) or 0)
    direction = match.group(4).upper()

    # Default is positive for Northern latitudes and Eastern longitudes
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)

    # Adjust for South latitudes and West longitudes
    if direction == 'S' or (is_longitude and direction == 'W'):
        decimal_degrees = -decimal_degrees

    return decimal_degrees

# Connect to SQLite database
conn = sqlite3.connect('E:\\Estoure\\smart-out-db\\smartout-gmap-built.sqlite')  # Replace with your actual SQLite file path
cursor = conn.cursor()

# Fetch records with latitude and longitude in DMS format
# cursor.execute("SELECT id, lat_degree, lng_degree FROM lake_data WHERE latitude IS NULL AND longitude IS NULL and lake_name != ''")
cursor.execute("SELECT id, lat_degree, lng_degree FROM lake_data WHERE oldRecord is null and coordinate is not null ")

# Iterate through the results and convert DMS to decimal
for row in cursor.fetchall():
    record_id = row[0]
    lat_degree = row[1]
    lng_degree = row[2]

    # Convert latitude and longitude from DMS to decimal degrees
    lat_decimal = dms_to_decimal(lat_degree)  # Latitude (no need for 'is_longitude')
    lng_decimal = dms_to_decimal(lng_degree, is_longitude=True)  # Longitude (set 'is_longitude' to True)

    if lat_decimal is not None and lng_decimal is not None:
        # Update the record with decimal degrees
        cursor.execute("""
            UPDATE lake_data 
            SET latitude = ?, longitude = ? 
            WHERE id = ?
        """, (lat_decimal, lng_decimal, record_id))

# Commit changes to the database
conn.commit()

# Close the connection
conn.close()

print("Latitude and Longitude converted and updated successfully!")
