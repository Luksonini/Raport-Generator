from django.shortcuts import render, redirect
from .forms import DocxUploadForm, ReplaceWordsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile, ModifiedFile
from .raport_functions import convert_docxs_to_zip, convert_to_pdf, generate_reports, convert_pdfs_to_zip, delete_old_files, generate_html 
from django.core.files import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

@login_required
def load_example(request, username):
    user = User.objects.get(username=username)

    # Initialize FileSystemStorage at your static files directory
    fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])

 # Open the file
    with fs.open('raport_from_list/example/test.docx') as example_file:
        uploaded_docx = File(example_file)

        # Extract the filename from the file
        filename = os.path.basename(example_file.name)

        # Now you can save it to your user's profile
        profile = Profile.objects.get(user=user)
        delete_old_files(profile)
        profile.doc_file.save(filename, uploaded_docx, save=True)
    
    # Redirect to the document_detail view
    return redirect('list_upload', username=request.user.username)


@login_required
def list_upload(request, username):
    user = User.objects.get(username=username)
    doc_form = DocxUploadForm(request.POST or None, request.FILES or None)
    if doc_form.is_valid():  
        uploaded_docx = doc_form.cleaned_data['file']
        number_words_to_replace = doc_form.cleaned_data['num_words']
        request.session['number_words_to_replace'] = number_words_to_replace

        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
        
        delete_old_files(profile)
        
        # Check if the user already has an uploaded document
        if profile.doc_file:
            # Delete the old file
            profile.doc_file.delete()
        
        # Save the uploaded file to the doc_file field
        profile.doc_file = uploaded_docx
        profile.save()
        
        # Redirect to the document_detail view
        return redirect('list_upload', username=request.user.username)
    else:
        doc_form = DocxUploadForm()

    return render(request, 'raport_from_list/list_upload.html', {'doc_form': doc_form})

@login_required
def create_replace_list(request, username):
    profile = Profile.objects.get(user__username=username)
    list_forms = []
    list_forms_data = {}
    docx_html = generate_html(profile=profile)

    number_words_to_replace = request.session.get('number_words_to_replace', None)
    for i in range(number_words_to_replace):
        list_form = ReplaceWordsForm(request.POST, prefix=f'form_{i+1}' or None)
        list_forms.append(list_form)

    if request.method == 'POST':
        for form in list_forms:
            if form.is_valid():
                search_word = form.cleaned_data.get('search')
                replace_words = form.cleaned_data.get('replace')
                replace_words_list = [word.strip() for word in replace_words.split(',')]
                list_forms_data[search_word] = replace_words_list

        # Check if the lists are equal in size
        word_list_lengths = [len(word_list) for word_list in list_forms_data.values() if word_list]
        if len(set(word_list_lengths)) > 1:
            error_message = "The lists should be equally sized."
            return render(request, 'raport_from_list/create_replace_list.html', {'list_forms': list_forms, 'error_message': error_message, 'docx_html': docx_html})

        results = generate_reports(profile, list_forms_data, request)
        docx_urls = results.get('docx_urls', [])
        not_found = results.get('not_found', [])

        if not_found:
            error_message = f"{' and '.join(not_found)} not found in the document text."
            return render(request, 'raport_from_list/create_replace_list.html', {'list_forms': list_forms, 'error_message': error_message, 'docx_html': docx_html})

        request.session['docx_urls'] = docx_urls
        return redirect('results_page', username=username)

    return render(request, 'raport_from_list/create_replace_list.html', {'list_forms': list_forms, 'docx_html': docx_html})


def results_page(request, username):
    # pythoncom.CoInitialize()
    pdf_urls = []
    zip_file_url = []
    pdf_zip_url = []
    docx_zip_path = []
    
    profile = Profile.objects.get(user__username=username)
    modified_files = ModifiedFile.objects.filter(profile=profile)  # Obtain the queryset of ModifiedFile objects
    docx_urls = [doc.modyfied_doc_file.url for doc in modified_files]
    if docx_urls:
        docx_zip_path = convert_docxs_to_zip(profile, modified_files)  # Pass the queryset to generate_zip function
    for pdf_file in profile.pdffile_set.all():
        pdf_file.pdf_file.delete()
    
    # if request.method == 'POST' and 'convert_to_pdf' in request.POST:
    #     pdf_urls = convert_to_pdf(modified_files, username) 
    #     pdf_zip_url = convert_pdfs_to_zip(profile)

    return render(request, 'raport_from_list/results_page.html', {
        'docx_urls': docx_urls,
        'docx_zip_path': docx_zip_path,
        'pdf_urls': pdf_urls,
        'zip_file_url': zip_file_url,
        'pdf_zip_url' : pdf_zip_url,
    })












