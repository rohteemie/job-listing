from django.shortcuts import render
from django.http import JsonResponse
from .forms import ResumeUploadForm
from .utils import extract_info_from_pdf


# Create your views here.
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume']

            # Check if the uploaded file is a valid PDF
            if uploaded_file.content_type != 'application/pdf':
                return JsonResponse({'error': 'Invalid file type. Please upload a PDF.'}, status=400)

            if uploaded_file.size > 5 * 1024 * 1024:  # Limit file size to 5MB
                return JsonResponse({'error': 'File too large. Please upload a file smaller than 5MB.'}, status=400)

            try:
                extracted_info = extract_info_from_pdf(uploaded_file)
                return JsonResponse(extracted_info)
            except Exception as e:
                return JsonResponse({'error': 'Failed to process PDF file.'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid form data.'}, status=400)

    form = ResumeUploadForm()
    return render(request, 'upload.html', {'form': form})


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