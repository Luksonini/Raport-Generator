from users.models import Profile, ExcelFile, ModifiedFile
from django.shortcuts import render, redirect
from raport_from_list.forms import DocxUploadForm
from django.contrib.auth.models import User
from .forms import ExscelUploadForm, ColumnChoiceForm, FilenameChoiceForm
from django.contrib.auth.decorators import login_required
from raport_from_list.raport_functions import generate_html
from raport_from_list.raport_functions import generate_reports, delete_old_files
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.conf import settings

@login_required
def load_excel_example(request, username):
    user = User.objects.get(username=username)

    # Initialize FileSystemStorage at your static files directory
    fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])

    # Open the docx file
    with fs.open('raport_from_list/example/test.docx') as example_file:
        uploaded_docx = File(example_file)

        # Extract the filename from the docx file
        docx_filename = os.path.basename(example_file.name)

        # Save it to your user's profile
        profile = Profile.objects.get(user=user)
        delete_old_files(profile)
        profile.doc_file.save(docx_filename, uploaded_docx, save=True)

    # Open the Excel file
    with fs.open('raport_from_list/example/test.xlsx') as example_file:
        uploaded_excel = File(example_file)

        # Extract the filename from the Excel file
        excel_filename = os.path.basename(example_file.name)

        # Create a new ExcelFile instance and save it
        excel_file = ExcelFile(profile=profile)
        excel_file.excel_file.save(excel_filename, uploaded_excel, save=True)

    return redirect('choose_columns', username=request.user.username)

@login_required
def excel_upload(request, username):
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        excel_form = ExscelUploadForm(request.POST, request.FILES)
        if excel_form.is_valid():
            delete_old_files(profile)
            uploaded_docx = excel_form.cleaned_data['doc_file']
            uploaded_excel = excel_form.cleaned_data['excel_file']

            try:
                profile = Profile.objects.get(user__username=username)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)

            # Create an instance of ExcelFile and associate it with the profile
            excel_file = ExcelFile(profile=profile)
            profile.doc_file = uploaded_docx
            excel_file.excel_file = uploaded_excel
            profile.save()
            excel_file.save()

            return redirect('choose_columns', username=request.user.username)
    else:
        excel_form = ExscelUploadForm()

    return render(request, 'raport_from_excel/excel_upload.html', {'excel_form': excel_form})


# Create your views here.
@login_required
def choose_columns(request, username):
    selected_columns = None
    words_to_replace = None
    selected_filename = None
    
    profile = Profile.objects.get(user__username=username)
    excel = profile.excelfile_set.first()
    excel_path = excel.excel_file.path

    docx_html = generate_html(profile)

    # Handle the Excel file upload logic
    excel_data = pd.read_excel(excel_path).head()
    columns = excel_data.columns  # Get column names from the Excel data
    column_choices = [(col, col)
                      for col in columns]  # Create choices for the form
    filename_columns = [('Default filenames', 'Default filenames')] + column_choices
    
    # Convert Excel data to HTML table using Pandas
    excel_html_table = excel_data.to_html(
        index=False, classes='table table-bordered')
    
    
    # replace the opening <tr> tag with the <tr> tag and the class attribute

    excel_html_table = excel_html_table.replace(
        '<tr>', '<tr class="table-row">')
    
    excel_html_table = excel_html_table.replace(
        '<thead>', '<thead class="table-header">')
    

    if request.method == 'POST':
        # Pass column_choices to the form
        columns_form = ColumnChoiceForm(request.POST, choices=column_choices)
        filenames_form = FilenameChoiceForm(request.POST, filename_columns=filename_columns)
        
        for column_choice in column_choices:
            words_to_replace = []
            words_to_replace.append(request.POST.get(column_choice))

        if columns_form.is_valid() and filenames_form.is_valid():
            selected_columns = columns_form.cleaned_data.get('columns')
            selected_filename_column = filenames_form.cleaned_data.get('filenames')
            if selected_filename_column not in "Default filenames":
                selected_filenames = excel_data[selected_filename_column].to_list()
                selected_filenames = [str(filename) + '.docx' for filename in selected_filenames]
                
                request.session['selected_filenames'] = selected_filenames
                request.session['filenames'] = selected_filename
            excel_words_to_replace = {}
            for column in selected_columns:
                word = request.POST.get(column)
                if word is not None:
                    excel_words_to_replace[column] = word    
                    replace_df_column_dict = {}
                    # get all ModifiedFile instances for this profile
                    modified_files = ModifiedFile.objects.filter(profile=profile)

                    # delete all the instances
                    for file in modified_files:
                        file.delete()

                    for column, word in excel_words_to_replace.items():
                        replace_df_column_dict[word] = excel_data[column].values.tolist(
                        )
               
                    # request.session['replace_df_column_dict'] = replace_df_column_dict
                    results = generate_reports(profile, replace_df_column_dict, request)
                    docx_urls = results.get('docx_urls', [])
                    not_found = results.get('not_found', [])
                    
                    if not_found:
                        error_message = f"{', '.join(str(element) for element in set(not_found))} not found in the document text."
                        context = {
                        'excel_html_table': excel_html_table,
                        'columns_form': columns_form,
                        'filenames_form': filenames_form,
                        'docx_html': docx_html,
                        'selected_columns': selected_columns,
                        'selected_filename': selected_filename,
                        'error_message' : error_message,
                        }
                        return render(request, 'raport_from_excel/excel_detail.html', context)

                    if not None in replace_df_column_dict.keys():
                        request.session['docx_urls'] = docx_urls
                        return redirect('results_page', username=username)

    else:
        # Initialize form with column choices
        columns_form = ColumnChoiceForm(choices=column_choices)
        # filenames_form = FilenameChoiceForm(choices=column_choices)
        filenames_form = FilenameChoiceForm(filename_columns=filename_columns)

    context = {
    'excel_html_table': excel_html_table,
    'columns_form': columns_form,
    'filenames_form': filenames_form,
    'docx_html': docx_html,
    'selected_columns': selected_columns,
    'selected_filename': selected_filename,
    }
    return render(request, 'raport_from_excel/excel_detail.html', context)

