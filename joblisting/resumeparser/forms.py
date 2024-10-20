from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(label='Upload your resume (PDF)', widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        # Validate file type
        if resume.content_type != 'application/pdf':
            raise forms.ValidationError('Invalid file type. Please upload a PDF.')

        # Validate file size (restrict to 5MB)
        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File too large. Please upload a file smaller than 5MB.')

        return resume
