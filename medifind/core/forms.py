from django import forms

class UploadForm(forms.Form):
    prescription = forms.ImageField()

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('kn', 'Kannada'),
        ('te', 'Telugu'),
        ('ta', 'Tamil'),
    ]
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=True,
        label="Preferred Language"
    )
