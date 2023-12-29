import os
import json
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from email.mime.image import MIMEImage
from django.db import transaction
from blog.email_thread import EmailThread
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.loader import get_template

from .forms import EmailSignupForm,Signup
from .forms import UserRegisterForm,UserUpdateForm



def register(request):
    if request.method == 'POST':

        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6LcUObIUAAAAAEPkFHzvfg0CBC_ri5LhK2kfurRM'

        captchadata = {
            'secret': secretkey,
            'response': clientkey
        }

        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        
        if(verify == False):
            messages.error(request, "First verify the reCAPTCHA!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def myaccount(request):
    return render(request,'accounts/myaccount.html')





@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
       
        if u_form.is_valid():
            u_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('index')

    else:
        u_form = UserUpdateForm(instance=request.user)
        

    context = {
        'u_form': u_form,
        
    }

    return render(request, 'accounts/profile.html', context)


def send_email(user):
    mail_subject = 'Information Regarding Subscription'
    email_from = settings.EMAIL_HOST_USER

    img_path = os.path.join(settings.MEDIA_ROOT, 'logo/me.png')
  
    if not os.path.exists(img_path):
        raise FileNotFoundError({
            'message': 'Image not found'
        })

    with open(img_path, 'rb') as image_file:
        image_data = image_file.read()

    template = get_template('email_subscription.html')

    app_domain = settings.SITE_DOMAIN

    context = {
        'user': user,
        'app_domain': app_domain,
        'link': "https://surajkarki66.com.np"
    }
    html_message = template.render(context)
    msg = EmailMultiAlternatives(
        mail_subject, html_message, email_from, [user["email"]]
    )
    msg.attach_alternative(html_message, 'text/html')
    img = MIMEImage(image_data, 'png')
    img.add_header('Content-Id', '<site_logo>')
    img.add_header('Content-Disposition', 'inline')
    msg.attach(img)
    EmailThread(msg).start()

@transaction.atomic
def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                print("already subscribed")
                messages.success(request, "You are already subscribed.")
            else:
                user = {
                    "email": form.instance.email,
                }
                send_email(user)
                messages.success(request, "Thank you for subscribing! Check your email for confirmation.")
                form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



