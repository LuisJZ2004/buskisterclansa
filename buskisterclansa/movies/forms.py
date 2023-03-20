from django import forms

class ReviewForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=70, required=True)
    content = forms.CharField(min_length=7, max_length=2600, required=True)
    rate = forms.ChoiceField(
        ((1,1,),(2,2,),(3,3,),(4,4,),(5,5,),), required=True
    )