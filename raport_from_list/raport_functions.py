from users.models import Profile, ModifiedFile, PDFFile, ExcelFile, DocxZipFile, PdfZipFile
from docx import Document 
import tempfile
import zipfile
from io import BytesIO
from django.core.files.base import ContentFile
import os
from pathlib import Path
from docx2pdf import convert
from django.conf import settings
# import pythoncom


def convert_docxs_to_zip(profile, modified_files):
    try:
        # Delete old zip files
        old_zip_files = DocxZipFile.objects.filter(profile=profile)
        for old_zip_file in old_zip_files:
            old_zip_file.docx_zip_file.delete()
            old_zip_file.delete()

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for modified_file in modified_files:
                file_path = os.path.join(modified_file.modyfied_doc_file.path)
                zip_file.write(file_path, os.path.basename(file_path))

        zip_buffer.seek(0)
        new_zip_file = DocxZipFile(profile=profile)
        new_zip_file_name = 'all_docx_files.zip'
        new_zip_file.docx_zip_file.save(new_zip_file_name, ContentFile(zip_buffer.getvalue()))
        new_zip_file.save()

        return new_zip_file.docx_zip_file.url
    except Exception as e:
        # Handle the exception or log the error
        print(f"Error generating zip from docx: {str(e)}")
        return None
     

def convert_pdfs_to_zip(profile):
    try:
        # Delete old zip files
        old_zip_files = PdfZipFile.objects.filter(profile=profile)
        for old_zip_file in old_zip_files:
            old_zip_file.pdf_zip_file.delete()
            old_zip_file.delete()

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            pdf_files = PDFFile.objects.filter(profile=profile)
            for pdf_file in pdf_files:
                file_path = os.path.join(pdf_file.pdf_file.path)
                zip_file.write(file_path, os.path.basename(file_path))

        zip_buffer.seek(0)
        new_zip_file = PdfZipFile(profile=profile)
        new_zip_file_name = 'all_pdf_files.zip'
        new_zip_file.pdf_zip_file.save(new_zip_file_name, ContentFile(zip_buffer.getvalue()))
        new_zip_file.save()

        return new_zip_file.pdf_zip_file.url
    except Exception as e:
        # Handle the exception or log the error
        print(f"Error generating PDF zip file: {str(e)}")
        return None

def convert_to_pdf(modified_files, username):
    profile = Profile.objects.get(user__username=username)
    old_pdf_files = PDFFile.objects.filter(profile=profile)

    for pdf_file in old_pdf_files:
        pdf_file.pdf_file.delete()
        pdf_file.delete()

    try:
        pdf_urls = []
        # pythoncom.CoInitialize()
        doc_file_path = Path(modified_files[0].modyfied_doc_file.path)
        doc_dir_path = doc_file_path.parent
        # Construct PDF directory path
        pdf_dir_path = os.path.join(settings.MEDIA_ROOT, username, 'pdf_documents')

        # Convert docx files to pdf
        convert(doc_dir_path, pdf_dir_path)

        # Get the file names and paths in the pdf_dir_path
        pdf_files = os.listdir(pdf_dir_path)

        for file_name in pdf_files:
            relative_file_path = os.path.join(username, 'pdf_documents', file_name)
            pdf_file = PDFFile.objects.create(pdf_file=relative_file_path, profile=profile)
            pdf_urls.append(pdf_file.pdf_file.url)

        return pdf_urls
    except Exception as e:
        # Handle the exception or log the error
        print(f"Error converting to PDF: {str(e)}")
        return []


def delete_old_files(profile):
    try:
        # Delete ModifiedFile objects
        ModifiedFile.objects.filter(profile=profile).delete()

        # Delete PDFFile objects
        PDFFile.objects.filter(profile=profile).delete()

        # Delete ExcelFile objects
        ExcelFile.objects.filter(profile=profile).delete()

        # Delete DocxZipFile objects
        DocxZipFile.objects.filter(profile=profile).delete()

        # Delete PdfZipFile objects
        PdfZipFile.objects.filter(profile=profile).delete()

        # Delete doc_file from Profile
        if profile.doc_file:
            profile.doc_file.delete()
            profile.doc_file = None
            profile.save()

        # Delete other model objects if needed

    except Exception as e:
        # Handle the exception or log the error
        print(f"Error deleting old files: {str(e)}")

def generate_modified_filename(prefix, file_number):
    modified_filename = f"{prefix}_{file_number}.docx"
    return modified_filename


def generate_reports(profile, form_data, request):
    try:
        original_file_path = profile.doc_file.path
        docx_urls = []
        not_found = []
        words_number = len(form_data[list(form_data.keys())[0]])
        selected_filenames = request.session.get('selected_filenames', None)

        # delete_old_files(profile)  # delete old modified files

        for i in range(words_number):
            with open(original_file_path, "rb") as original_file:
                doc = Document(original_file)

                for search_key, word_list in form_data.items():
                    word_to_replace = word_list[i]
                    found = False

                    for paragraph in doc.paragraphs:
                        if search_key in paragraph.text:
                            found = True
                            paragraph.text = paragraph.text.replace(search_key, word_to_replace)

                    if not found:
                        not_found.append(search_key)

                if selected_filenames:
                    modified_filename = selected_filenames[i]
                else:
                    modified_filename = generate_modified_filename("file", i)

                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    doc.save(temp_file.name)
                    temp_file.close()

                    with open(temp_file.name, "rb") as file:
                        modified_file = ModifiedFile(profile=profile)
                        modified_file.modyfied_doc_file.save(modified_filename, file, save=False)
                        modified_file.modyfied_doc_file_name = modified_filename
                        modified_file.save()

                        docx_urls.append(modified_file.modyfied_doc_file.url)

                    os.unlink(temp_file.name)

        return {
            'docx_urls': docx_urls,
            'not_found': not_found,
        }
    except Exception as e:
        # Handle the exception or log the error
        print(f"Error generating reports: {str(e)}")
        return {
            'docx_urls': [],
            'not_found': [],
        }

from bs4 import BeautifulSoup


def generate_html(profile):
    original_file_path = profile.doc_file.path

    with open(original_file_path, "rb") as original_file:
        document = Document(original_file)
        soup = BeautifulSoup('', 'html.parser')

        for para in document.paragraphs:
            p = soup.new_tag('p')
            for run in para.runs:
                words = run.text.split()
                for word in words:
                    if run.bold and run.italic:
                        span = soup.new_tag('span', style='font-weight: bold; font-style: italic;')
                    elif run.bold:
                        span = soup.new_tag('span', style='font-weight: bold;')
                    elif run.italic:
                        span = soup.new_tag('span', style='font-style: italic;')
                    elif run.underline:
                        span = soup.new_tag('span', style='text-decoration: underline;')
                    else:
                        span = soup.new_tag('span')
                    span.string = word
                    p.append(span)
                    p.append(' ')  # Append a space after each word
            soup.append(p)

        return str(soup)