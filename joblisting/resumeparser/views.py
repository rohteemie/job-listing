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
    """Extracts information like email, phone number, and raw text from a PDF resume."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    # Extract email using regex
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else None

    # Extract phone number using regex
    phone_match = re.search(r'\+?\d[\d -]{8,}\d', text)
    phone = phone_match.group(0) if phone_match else None

    # Check for missing info and return an appropriate response
    if not email:
        email = "Email not found"
    if not phone:
        phone = "Phone number not found"

    return {
        'email': email,
        'phone': phone,
        'raw_text': text
    }