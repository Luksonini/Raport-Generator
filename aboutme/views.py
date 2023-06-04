from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

def aboutme(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            recipients = ['lukasz.jozef.gasior@gmail.com']
            
            message = f"Message from {first_name} {last_name}, email: {sender} \n\n {message}"
            
            send_mail(subject, message, sender, recipients)
    else:
        form = ContactForm()

    return render(request, 'aboutme/aboutme.html', {'form': form})