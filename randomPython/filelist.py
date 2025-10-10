import csv
from pathlib import Path

# Function to get all file paths in a directory
def get_all_files(directory):
    directory_path = Path(directory)
    # Use rglob to find all files recursively
    return [str(file) for file in directory_path.rglob('*') if file.is_file()]

# Directory to scan
directory =r'C:\C#Class2'

# Get all file paths
file_paths = get_all_files(directory)

# Specify the CSV file to write the paths to
csv_file = 'C:\FlowData\paths2.csv'

# Write the file paths to the CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write a header (optional)
    writer.writerow(['File Path'])
    # Write all file paths
    for file_path in file_paths:
        writer.writerow([file_path])

print(f"All file paths have been written to {csv_file}")


