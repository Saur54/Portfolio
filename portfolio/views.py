from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SocialLink, HomeSection, AboutSection, Skill, Education, Experience, Service, Project, ContactInfo, QueryMessage, Blog

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and subject and message:
            QueryMessage.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
            messages.success(request, 'Message sent successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please fill all required fields.')

    context = {
        'social_links': SocialLink.objects.all(),
        'home': HomeSection.objects.first(),
        'about': AboutSection.objects.first(),
        'skills': Skill.objects.all(),
        'education': Education.objects.all(),
        'experience': Experience.objects.all(),
        'services': Service.objects.all(),
        'projects': Project.objects.all(),
        'contact_info': ContactInfo.objects.all(),
    }
    return render(request, 'portfolio/index.html', context)

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-date_posted')
    context = {
        'blogs': blogs,
        'social_links': SocialLink.objects.all(),
        'home': HomeSection.objects.first(),
    }
    return render(request, 'portfolio/blog.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    context = {
        'blog': blog,
        'social_links': SocialLink.objects.all(),
        'home': HomeSection.objects.first(),
    }
    return render(request, 'portfolio/blog_detail.html', context)
