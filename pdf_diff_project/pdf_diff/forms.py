from django import forms

class PDFUploadForm(forms.Form):
    file1 = forms.FileField(label='PDF File 1')
    file2 = forms.FileField(label='PDF File 2')
