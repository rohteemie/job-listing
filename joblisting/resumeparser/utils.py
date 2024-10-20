import re
import fitz  # PyMuPDF

def extract_info_from_pdf(pdf_file):
    # Open the PDF file
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""

    # Extract text from all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    # Extract email using regex
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = email_match.group(0) if email_match else None

    # Extract phone number using regex (basic international format)
    phone_match = re.search(r'\+?\d[\d\s-]{8,}\d', text)
    phone = phone_match.group(0) if phone_match else None

    # Return the extracted info
    return {
        'email': email,
        'phone': phone,
        'raw_text': text
    }
