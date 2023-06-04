from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile, DocxZipFile, PdfZipFile
from django.contrib import messages
from django.core.mail import send_mail
from .forms import FileSharingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('users:home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print('Logout message added')
        return response

def home(request):    
    for message in messages.get_messages(request):
        print(f"this is the message from logging out{message}")
    return render(request, 'raport_from_list/home.html')

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user = User.objects.get(username=username)
                return redirect('profile', username=username)
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "There was an error with the form")

    form = LoginForm()
    return render(request, 'users/login.html',  {"form" : form})


def register_view(request):
    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'users/register_done.html')
        else:
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        register_form = UserRegisterForm()
    
    return render(request, "users/register.html", {"register_form": register_form})


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    pdf_zip_link = None
    docx_zip_link = None
    
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    try:
        docx_zip_file = DocxZipFile.objects.get(profile=profile)
        docx_zip_link = request.build_absolute_uri(docx_zip_file.docx_zip_file.url)
    except DocxZipFile.DoesNotExist:
        pass

    try:
        pdf_zip_file = PdfZipFile.objects.get(profile=profile)
        pdf_zip_link = request.build_absolute_uri(pdf_zip_file.pdf_zip_file.url)
    except PdfZipFile.DoesNotExist:
        pass

    if pdf_zip_link:
        results_url = pdf_zip_link
    else:  
        results_url = docx_zip_link

    if request.method == 'POST':
        form = FileSharingForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            file_url = docx_zip_link 

            subject = 'File Sharing'
            message += f'\n\nHere is the link to the raports: {file_url}'
            sender = 'sender@example.com' 
            recipient = email
            send_mail(subject, message, sender, [recipient])

            messages.success(request, 'File shared successfully!')
        
    else:
        form = FileSharingForm()

    return render(request, 'users/profile.html', {
        'results_url': results_url,
        'form': form,
    })

def privacy_policy(request):
    return render(request, 'users/privacy_policy.html')

def handler500(request):
    return render(request, 'users/error500.html', status=500)

def handler404(request, exception):
    return render(request, 'users/error500.html', status=404)