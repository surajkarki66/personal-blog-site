import os

from blog.email_thread import EmailThread
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .forms import CommentForm, PostForm
from .models import Post,Quote
from accounts.models import Signup,Author,Contact
from accounts.forms import EmailSignupForm



def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


def index(request):
    quote = Quote.objects.all()
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    form = EmailSignupForm()

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'quote':quote,
        'form':form
    }
    return render(request, 'index.html' ,context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)

def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'form': form,
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count
    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))


def send_email(user):
    mail_subject = 'Information Regarding Help'
    email_from = settings.EMAIL_HOST_USER

    img_path = os.path.join(settings.MEDIA_ROOT, 'logo/me.png')
  
    if not os.path.exists(img_path):
        raise FileNotFoundError({
            'message': 'Image not found'
        })

    with open(img_path, 'rb') as image_file:
        image_data = image_file.read()

    template = get_template('email_help.html')

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
def contact(request):
   context = {
            'show_alert': False,
            
    }
   if request.method == "POST":
      name = request.POST.get('name', '')
      email = request.POST.get('email', '')
      phone = request.POST.get('phone', '')
      desc = request.POST.get('desc', '')
      contact = Contact(name=name, email=email, phone=phone, desc=desc)
      user = {
                "email": email,
                "name": name
             }
      send_email(user)
      contact.save()
      context = {
            'show_alert': True,
            
    }
   return render(request, 'contact.html', context=context)


def faq(request):
    contact = Contact.objects.all
    return render(request,'faq.html',{'contact':contact})


    








