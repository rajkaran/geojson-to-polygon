import sqlite3
import re

# Connect to SQLite database
conn = sqlite3.connect("E:\\Estoure\\smart-out-db\\smartout-gmap-built.sqlite")
cursor = conn.cursor()

# Fetch data from the database
cursor.execute("SELECT where_to_show_ping, exception_id FROM raw_pin_coordinate WHERE where_to_show_ping != ''")
rows = cursor.fetchall()
print(f"Total rows fetched: {len(rows)}")

new_rows = []
for where_to_show_ping, exception_id in rows:
    for line in where_to_show_ping.splitlines():
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        
        # Remove bullet points (•, *)
        line = re.sub(r"^[•*]\s*", "", line)
       
        new_rows.append((exception_id, line))

print(f"Total processed rows: {len(new_rows)}")

# Insert data into the new table
cursor.executemany("""
    INSERT INTO lake_data (exception_id, lake) 
    VALUES (?, ?)
""", new_rows)

# Commit changes and close connection
conn.commit()
conn.close()
print("Data successfully inserted!")
