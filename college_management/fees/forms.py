from dal import autocomplete
from django import forms
from .models import Fees

class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = '__all__'
        widgets = {
            'student': autocomplete.ModelSelect2(url='student-autocomplete'),
        }