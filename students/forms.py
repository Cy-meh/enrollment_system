from django import forms
from .models import Student, FamilyBackground, EducationalBackground


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['date_enrolled']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class FamilyForm(forms.ModelForm):
    class Meta:
        model = FamilyBackground
        exclude = ['student']


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        exclude = ['student']