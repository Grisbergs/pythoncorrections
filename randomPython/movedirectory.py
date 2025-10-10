import shutil
import os

# Source directory where files are currently located
source_directory = r'O:\Cancel_Test\Archive\NewProcessArch\split1'

# Destination directory where files will be moved to
destination_directory = r'C:\C#Class2'

# Ensure the destination directory exists, create it if it doesn't
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Loop through all files in the source directory
for file_name in os.listdir(source_directory):
    source_file = os.path.join(source_directory, file_name)
    destination_file = os.path.join(destination_directory, file_name)
    
    # Check if it's a file (you can modify this to include directories if needed)
    if os.path.isfile(source_file):
        # Move the file to the destination directory
        shutil.move(source_file, destination_file)
        print(f'Moved: {source_file} -> {destination_file}')