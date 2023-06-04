from django import forms
from django.core.validators import FileExtensionValidator

class ExscelUploadForm(forms.Form):

    doc_file = forms.FileField(
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
    
    excel_file = forms.FileField(
        label= 'Chooce excel file',
        widget=forms.ClearableFileInput(attrs={"accept": '.xlsx', "type": "file", "class": "custom-excel-input", "id" : "excel-file-input"}),
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=['xlsx'])],
        error_messages={
            'required': '<div class="alert alert-danger">Please select an Excel document to upload</div>',
            'invalid_extension': '<div class="alert alert-danger">File extension is not allowed. Allowed extensions are: %(allowed_extensions)s.</div>'
        }
    )


class ColumnChoiceForm(forms.Form):
    columns = forms.MultipleChoiceField(
        label='Select the data source columns',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'column-choose-box'}),
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        # Get the 'choices' argument and remove it from kwargs
        choices = kwargs.pop('choices', None)
        super(ColumnChoiceForm, self).__init__(*args, **kwargs)
        # Set the choices for the 'columns' field
        self.fields['columns'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        selected_columns = cleaned_data.get('columns', [])
        for column in selected_columns:
            self.fields[column] = forms.CharField(
                label=column,
                required=True,
                widget=forms.TextInput(
                    attrs={'placeholder': 'Enter word to replace', "class": "form-control", "id" : "id_num_words"})
            )
        return cleaned_data
    

class FilenameChoiceForm(forms.Form):
    filenames = forms.ChoiceField(
        label='Select the column containing filenames',
        widget=forms.Select(attrs={'class': 'filename-choose-box'}),
        required=False  # Set the field as not required
    )

    def __init__(self, *args, **kwargs):
        filename_columns = kwargs.pop('filename_columns', None)
        super(FilenameChoiceForm, self).__init__(*args, **kwargs)
        self.fields['filenames'].choices = filename_columns