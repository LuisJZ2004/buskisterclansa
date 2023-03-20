# Django
from django import forms

# This app
from .models import Review

class ReviewForm(forms.ModelForm):
    name = forms.CharField(min_length=1, max_length=70, required=True)
    content = forms.CharField(min_length=7, max_length=2600, required=True)

    class Meta:
        model = Review
        fields = ("name", "content", "rate_by_stars")