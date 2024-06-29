from django import forms
from .models import Libro

class BookForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('name', 'author', 'gender', 'editorial', 'year', 'price', 'image')