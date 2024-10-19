from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

class ResumeParserTests(TestCase):
    def create_test_pdf(self):
        # Create a PDF file in memory
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "This is a test resume.")
        p.drawString(100, 730, "Email: johndoe@example.com")
        p.drawString(100, 710, "Phone: +1234567890")
        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer

    def test_resume_upload_form_renders(self):
        response = self.client.get(reverse('upload_resume'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_resume_upload(self):
        pdf_buffer = self.create_test_pdf()
        resume = SimpleUploadedFile("test_resume.pdf", pdf_buffer.read(), content_type="application/pdf")
        response = self.client.post(reverse('upload_resume'), {'resume': resume})
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])

    def test_pdf_info_extraction(self):
        # Create a PDF file with mock content
        pdf_buffer = self.create_test_pdf()
        resume = SimpleUploadedFile("test_resume.pdf", pdf_buffer.read(), content_type="application/pdf")

        # Send a POST request with the mock PDF
        response = self.client.post(reverse('upload_resume'), {'resume': resume})

        # Verify response contains extracted information
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['email'], 'johndoe@example.com')
        self.assertEqual(json_response['phone'], '+1234567890')
