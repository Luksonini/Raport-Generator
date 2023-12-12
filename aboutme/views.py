from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
import os
from django.conf import settings


def aboutme(request):
    #
    # pdf_directory = r'D:\programowanie\raport generator\Raport-Generator\aboutme\static\courses'
    pdf_directory = r'/home/Luksonini/Raport-Generator/aboutme/static/courses'

    # Get the list of PDF course files in the directory
    pdf_files = os.listdir(pdf_directory)
    pdf_files = [file for file in pdf_files if file.endswith('.pdf')]

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            from_email = f"{first_name} {last_name} <{sender}>"
            to_email = "Łukasz <lukasz.jozef.gasior@gmail.com>"

            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )

            # Email sent successfully
            success_message = "Email sent successfully!"
            return render(request, 'aboutme/aboutme.html', {'form': form, 'pdf_files': pdf_files, 'success_message': success_message})
    else:
        form = ContactForm()

    return render(request, 'aboutme/aboutme.html', {'form': form, 'pdf_files': pdf_files})