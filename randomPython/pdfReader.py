import PyPDF2
import re
import csv

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


pdf_path = r'\\Qtsprodkfxstor1\Data\CANCELDOCS\Archive\312025\OK00184_7594483897319243719_provider.pdf'
text = extract_text_from_pdf(pdf_path)
vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'
vin_pattern2 = r'^[A-HJ-NPR-Za-hj-npr-z\d]{9}[A-HJ-NPR-Za-hj-npr-z\d]{3}\d{5}$'
date_pattern = r"Date(.{100})"
date_pattern2 = r"(\d{2})[-/](\d{2})[-/](\d{4})\b|\b(\d{4})[-/](\d{2})[-/](\d{2})"



match = re.search(vin_pattern, text)
match2 = re.search(vin_pattern2, text)
match3 = re.search(date_pattern,text,re.DOTALL)

if match:
    print(f"Found VIN: {match.group()}")
else:
    if match2:
        print(f"PT2 Found VIN: {match2.group()}")
    else:
        print(text)
if match3:
    print(match3.group())
    datelarge = match3.group()
    match4 = re.search(date_pattern2,datelarge)
    if match4:
        print(match4)
    else:
        print("nodate")
else:
    print(text)