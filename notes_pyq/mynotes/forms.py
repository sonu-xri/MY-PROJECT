from django import forms
from .models import PYQ

class PYQUploadForm(forms.ModelForm):
    """Form for uploading PYQ files"""
    class Meta:
        model = PYQ
        fields = ['title', 'subject', 'exam_year', 'semester', 'exam_type', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., B.Sc Mathematics 2023 Question Paper'}),
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Mathematics, Physics, Computer Science'}),
            'exam_year': forms.Select(choices=[('', 'Select Year')] + [(str(y), str(y)) for y in range(2026, 2014, -1)]),
            'semester': forms.Select(choices=[
                ('', 'Select Semester/Year'),
                ('Semester 1', 'Semester 1'), ('Semester 2', 'Semester 2'),
                ('Semester 3', 'Semester 3'), ('Semester 4', 'Semester 4'),
                ('Semester 5', 'Semester 5'), ('Semester 6', 'Semester 6'),
                ('Semester 7', 'Semester 7'), ('Semester 8', 'Semester 8'),
                ('1st Year', '1st Year'), ('2nd Year', '2nd Year'),
                ('3rd Year', '3rd Year'), ('4th Year', '4th Year'),
            ]),
            'exam_type': forms.Select(choices=[
                ('', 'Select Exam Type'),
                ('Internal Exam', 'Internal Exam'),
                ('Semester Exam', 'Semester Exam'),
                ('Final Exam', 'Final Exam'),
                ('Model Exam', 'Model Exam'),
                ('Practice Test', 'Practice Test'),
            ]),
            'description': forms.Textarea(attrs={'placeholder': 'Add any additional information about this question paper...'}),
            'file': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,.pptx,.xls,.xlsx,.ppt'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (100MB limit)
            if file.size > 100 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 100MB.")
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.pptx', '.xls', '.xlsx', '.ppt']
            if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("File type not supported. Please upload PDF, DOC, DOCX, PPTX, XLS, XLSX, or PPT files.")
        return file