from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def upload_resume(request):
    # return render(request, 'upload.html')
    if request.method == 'POST':
        uploaded_file = request.FILES['resume']
        # For now, I will just return a dummy JSON response
        # return JsonResponse({'message': 'File uploaded successfully'})

        extracted_info = extract_info_from_pdf(uploaded_file)
        print("Extracted info:", extracted_info)  # <-- Add this for debugging

        return JsonResponse(extracted_info)

    return render(request, 'upload.html')


import re
import fitz  # PyMuPDF

def extract_info_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Read PDF
    text = ""
    for page in doc:  # Extraction of text from each page
        text += page.get_text()

    # Use regex to find specific information
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.search(r'\+?\d[\d -]{8,}\d', text)  # A simple regex for phone numbers
    # For future updates, I will add other extractions like age, profession, etc.

    # Return extracted data as a dictionary
    return {
        'email': email.group(0) if email else None,
        'phone': phone.group(0) if phone else None,
        'raw_text': text[:500]  # Optionally include a preview of the resume text
    }