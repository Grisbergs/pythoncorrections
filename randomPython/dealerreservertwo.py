import os
import re
import csv
from pathlib import Path
import PyPDF2

# Function to get all file paths in a directory
def get_all_files(directory):
    """Recursively retrieves all file paths in the specified directory."""
    directory_path = Path(directory)
    return [str(file) for file in directory_path.rglob('*') if file.is_file()]

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ''

def scan_pdf_for_pattern(pdf_path, pattern):
    """Scans the extracted text from a PDF for a specific pattern."""
    text = extract_text_from_pdf(pdf_path)
    if text and re.search(pattern, text, re.IGNORECASE):
        return True
    return False

def process_files(directory, csv_path, pattern):
    """Process all PDF files in the directory and write results to a CSV file."""
    file_paths = get_all_files(directory)
    review_results = []

    for file_path in file_paths:
        if file_path.lower().endswith('.pdf'):  # Only process PDF files
            if scan_pdf_for_pattern(file_path, pattern):
                result = f"Found: {pattern} in {file_path}"
                review_results.append([result])
                print('Found pattern in:', file_path)
            else:
                result = f"Not Found: {pattern} in {file_path}"
                review_results.append([result])
                print('Pattern not found in:', file_path)
    
    # Write results to CSV
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Review Result'])
            writer.writerows(review_results)
        print(f"Results saved to {csv_path}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Directory and CSV file paths
directory = r'\\Qtsprodkfxstor1\Data\CANCELDOCS\AddDocuments'
csv_path = r'C:\C#Class\Files.csv'
pattern = r'dealer reserve'  # The pattern to search for in the PDF text

# Process the files
process_files(directory, csv_path, pattern)
