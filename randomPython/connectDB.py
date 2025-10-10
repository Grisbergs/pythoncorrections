import pyodbc

# Define connection string
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=QTSPRODKFXSSRS;'
    'DATABASE=Testing_Report;'
    'Trusted_Connection=yes;'
)

# Create a cursor
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT TOP 10 * FROM ECE_GAPVIN")

# Fetch results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()
