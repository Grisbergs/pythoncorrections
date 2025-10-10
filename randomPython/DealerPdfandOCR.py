import os
import re
import csv
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import PyPDF2

# Function to get all file paths in a directory
def get_all_files(directory):
    """Recursively retrieves all file paths in the specified directory."""
    directory_path = Path(directory)
    return [str(file) for file in directory_path.rglob('*') if file.is_file()]

# Function to extract text from an image (multi-page TIFF or single-page image)
def extract_text_from_image(image_path):
    """Extracts text from a multi-page image or single-page image."""
    image = Image.open(image_path)
    full_text = ''
    for i in range(image.n_frames):  # Iterate through each frame in the multi-page image
        image.seek(i)  # Go to the i-th frame
        text = pytesseract.image_to_string(image)
        full_text += f"Page {i+1}:\n{text}\n\n"
    return full_text

# Function to extract text from a PDF using PyPDF2 with error handling for corrupted PDFs
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""  # Handle None case
            return text
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error: Corrupted PDF {pdf_path} - {e}")
        return None
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return None

# Function to check if pattern exists in the extracted text and return the matched string
def find_pattern_in_text(text, pattern):
    """Searches for the pattern in the extracted text and returns the matched string."""
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None

# Function to process a single file (PDF or Image)
def process_file(file_path, vin_pattern, output_tiff_path):
    """Processes a single file and returns the review result, matched text, and file name."""
    file_name = os.path.basename(file_path)  # Extract the file name

    # First try extracting from PDF
    text = extract_text_from_pdf(file_path)
    if text is None:
        # Skip corrupted PDF or unreadable file
        return file_name, "Error: Corrupted or unreadable PDF", None

    matched_text = find_pattern_in_text(text, vin_pattern)

    if matched_text:
        return file_name, f"Found: {matched_text}", matched_text

    # If no match in text, try converting PDF to image and process using OCR
    images = convert_from_path(file_path)
    bw_images = [image.convert('1') for image in images]  # Convert to black and white for better OCR
    bw_images[0].save(output_tiff_path, save_all=True, append_images=bw_images[1:], compression='tiff_deflate')

    # Run OCR on the image
    text_from_image = extract_text_from_image(output_tiff_path)
    matched_text = find_pattern_in_text(text_from_image, vin_pattern)

    if matched_text:
        return file_name, f"Found: {matched_text}", matched_text

    return file_name, f"Not Found: {vin_pattern}", None

# Function to write the review results to a CSV file
def write_results_to_csv(review_results, csv_path):
    """Writes the review results to the CSV file."""
    file_exists = os.path.exists(csv_path)
    try:
        with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['File Name', 'Review', 'Matched Text'])  # Write header with 'File Name', 'Review', 'Matched Text'
            writer.writerows(review_results)
    except Exception as e:
        print(f"Error writing to CSV {csv_path}: {e}")

# Main processing function
def process_files(directory, csv_path, vin_pattern, output_tiff_path):
    """Processes all files in the specified directory and writes results to a CSV."""
    file_paths = get_all_files(directory)
    review_results = []

    for file_path in file_paths:
        if file_path.lower().endswith('.pdf'):
            file_name, result, matched_text = process_file(file_path, vin_pattern, output_tiff_path)
            review_results.append([file_name, result, matched_text if matched_text else ""])  # Append file name, result, and matched text
            print(result)

    write_results_to_csv(review_results, csv_path)

# Define paths and parameters
directory = r'\\Qtsprodkfxstor1\Data\CANCELDOCS\Current'
csv_path = r'C:\C#Class\vinfiles1.csv'
vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'
output_tiff_path = r'C:\C#Class\output_multipage6.tiff'

# Run the main process
process_files(directory, csv_path, vin_pattern, output_tiff_path)
