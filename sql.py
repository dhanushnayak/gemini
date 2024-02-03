import sqlite3

conn = sqlite3.connect('mydb.db')

cursor = conn.cursor()

# Define the SQL query to create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS data(
    NAME VARCHAR(23),
    CLASS VARCHAR(23),
    SECTION VARCHAR(25),
    MARKS INT
);
"""

# Execute the create table query
cursor.execute(create_table_query)

# Define the data to be inserted
data_to_insert = [
    ('John', 'A', 'Section 1', 85),
    ('Alice', 'B', 'Section 2', 90),
    ('Bob', 'A', 'Section 1', 78)
]

# Define the SQL query to insert multiple data points
insert_query = "INSERT INTO data (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)"

# Execute the insert query for each data point
cursor.executemany(insert_query, data_to_insert)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
