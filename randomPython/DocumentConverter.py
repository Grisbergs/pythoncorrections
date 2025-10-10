from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import re
from pathlib import Path
import csv
import PyPDF2
# Function to get all file paths in a directory
def get_all_files(directory):
    directory_path = Path(directory)
    # Use rglob to find all files recursively
    return [str(file) for file in directory_path.rglob('*') if file.is_file()]

#function to get all text from multi page image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    full_text = ''
    for i in range(image.n_frames):  # Iterate through each frame in the multi-page image
        image.seek(i)  # Go to the i-th frame
        text = pytesseract.image_to_string(image)
        full_text += f"Page {i+1}:\n{text}\n\n"
    
    return full_text

def extract_text_from_pdf(pdf_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        
        # Initialize a variable to store the extracted text
        text = ''
        
        # Loop through all pages in the PDF
        for page_num in range(len(reader.pages)):
            # Extract text from each page
            page = reader.pages[page_num]
            text += page.extract_text()
        
        return text

# Directory to scan
directory =r'\\Qtsprodkfxstor1\Data\CANCELDOCS\AddDocuments'
csvpath = r'C:\C#Class\Files.csv'

# Get all file paths
file_paths = get_all_files(directory)
review =[]
for file_path in file_paths:
# Path to your PDF file
    pdf_path = file_path
    output_tiff_path = 'C:\C#Class\output_multipage6.tiff'
    text = extract_text_from_pdf(pdf_path)    
    vin_pattern = r'dealer reserve'
    
    match = re.search(vin_pattern, text)
    
   
    if match:
        review.append(f"Found: {match.group()}+ {file_path}")
    else:   
        images = convert_from_path(pdf_path)
        bw_images = [image.convert('1') for image in images]  # '1' mode converts to black and white # Process each image to convert it to black and white Improves OCR
        bw_images[0].save(output_tiff_path, save_all=True, append_images=bw_images[1:], compression='tiff_deflate')# Save the images as a multi-page TIFF
        text = extract_text_from_image(output_tiff_path)#run Tesseract method  
        vin_pattern = r'dealer reserve'#Run Regex over extracted text to get vin match   
       
        match = re.search(vin_pattern, text)
     
        if match:
           review.append(f"Found: {match.group()}+ {file_path}")
        else:
           review.append(f"NotFound+ {file_path}")
    print('loop!')       
file_exists = os.path.exists(csvpath)

# Open the file in append mode
with open(csvpath, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # If the file is empty or doesn't exist, write the header
    if not file_exists:
        writer.writerow(['Review'])
    
    # Write the new rows
    writer.writerows(review)
