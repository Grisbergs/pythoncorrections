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

directory =r'C:\C#Class\kofaxstuff\Training Docs'
file_paths = get_all_files(directory)
for file_path in file_paths:
# Path to your PDF file
    pdf_path = file_path
    tiffname = os.path.splitext(os.path.basename(file_path))[0]
    output_tiff_path = f'C:\C#Class\kofaxstuff\Training Docs\Tiffs\{tiffname}.tiff'
    images = convert_from_path(pdf_path)
    bw_images = [image.convert('1') for image in images]  # '1' mode converts to black and white # Process each image to convert it to black and white Improves OCR
    bw_images[0].save(output_tiff_path, save_all=True, append_images=bw_images[1:], compression='tiff_deflate')# Save the images as a multi-page TIFF