"""
Handle PDF reading and date extraction
"""
import re
from datetime import datetime
from PyPDF2 import PdfReader


def extract_dates_from_pdf(pdf_path):
    """
    Extract dates from PDF file
    Supports formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    """
    dates = []
    
    try:
        pdf_reader = PdfReader(pdf_path)
        
        # Extract text from all pages
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
        # Regex patterns for different date formats
        patterns = [
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        ]
        
        found_date_strings = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            found_date_strings.update(matches)
        
        # Parse dates
        for date_str in found_date_strings:
            try:
                if '/' in date_str:
                    # DD/MM/YYYY format
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                elif '-' in date_str:
                    if date_str.split('-')[0].isdigit() and len(date_str.split('-')[0]) == 4:
                        # YYYY-MM-DD format
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    else:
                        # DD-MM-YYYY format
                        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                else:
                    continue
                
                dates.append(date_obj)
            except ValueError:
                continue
        
        # Remove duplicates and sort
        dates = list(set(dates))
        dates.sort()
        
        return dates
        
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []
