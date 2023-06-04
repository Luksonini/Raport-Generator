from django import forms
from django.core.validators import FileExtensionValidator



class DocxUploadForm(forms.Form):
    
    file = forms.FileField(
        label='',
        widget=forms.ClearableFileInput(
            attrs={"accept": '.docx', "type": "file", "class": "custom-file-input", "id" : "docx-file-input"}),
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=['docx'])],
        error_messages={
            'required': ' "Please select an Excel document to upload',
            'invalid_extension': 'File extension “%(extension)s” is not allowed. The only Allowed extension is: .docx'
        }
    )
    
    num_words = forms.IntegerField(
        label='',
        min_value=1,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Number of words to replace'}),
        required=True
    )


class ReplaceWordsForm(forms.Form):
    search = forms.CharField(
        label='', max_length=255, required=True,
        widget=forms.TextInput(
            attrs={'class': "form-control search-form", "placeholder": "paste the words separated by coma",
                   "id": "word-input", "autocomplete":"off"}),
        # custom error message for the required field
        error_messages={'blank': 'custom sessage'})

    replace = forms.CharField(
        label='', max_length=1000, required=True,
        widget=forms.Textarea(
            attrs={'class': 'form-control replace-form', "placeholder": "paste the words separated by coma", "id": "search-and-replace"})
    )