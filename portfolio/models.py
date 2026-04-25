from django.db import models

from .storage import get_image_storage, get_raw_storage

class SocialLink(models.Model):
    icon = models.CharField(max_length=50, help_text='FontAwesome icon class (e.g., fa-brands fa-twitter)')
    url = models.URLField()

    def __str__(self):
        return self.icon

class HomeSection(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)
    description = models.TextField()
    hero_image = models.ImageField(upload_to='hero_images/', storage=get_image_storage())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AboutSection(models.Model):
    first_name = models.CharField(max_length=50, default="Steve")
    last_name = models.CharField(max_length=50, default="Milner")
    age = models.IntegerField(default=27)
    nationality = models.CharField(max_length=50, default="Tunisian")
    freelance = models.CharField(max_length=50, default="Available")
    address = models.CharField(max_length=100, default="Tunis")
    phone = models.CharField(max_length=20, default="+21621184010")
    email = models.EmailField(default="you@mail.com")
    skype = models.CharField(max_length=50, default="steve.milner")
    languages = models.CharField(max_length=100, default="French, English")
    description = models.TextField(blank=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True, storage=get_raw_storage())

    def __str__(self):
        return "About Info"

class Skill(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.IntegerField()

    def __str__(self):
        return self.name

class Education(models.Model):
    year_range = models.CharField(max_length=50, help_text='e.g., 2021-2024')
    degree_title = models.CharField(max_length=100)
    institution = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.degree_title} at {self.institution}"

class Experience(models.Model):
    year_range = models.CharField(max_length=50, help_text='e.g., 2024-2025')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company}"

class Service(models.Model):
    icon = models.CharField(max_length=50, help_text='FontAwesome icon class (e.g., fa-solid fa-mobile-alt)')
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Project(models.Model):
    CATEGORIES = (
        ('Web', 'Web'),
        ('Mobile', 'Mobile'),
        ('Design', 'Design'),
    )
    category = models.CharField(max_length=50, choices=CATEGORIES, default='Web')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', storage=get_image_storage())
    tech_stack = models.CharField(max_length=200, help_text='Comma separated, e.g., HTML, CSS, JS', blank=True)
    is_featured = models.BooleanField(default=False)
    code_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_tech_stack(self):
        return [tech.strip() for tech in self.tech_stack.split(',')] if self.tech_stack else []

class ContactInfo(models.Model):
    icon = models.CharField(max_length=50, help_text='FontAwesome icon class')
    title = models.CharField(max_length=100)
    data = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class QueryMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True, storage=get_image_storage())
    description = models.TextField(help_text="Short description for the blog list")
    content = models.TextField(help_text="Full blog content (You can use HTML tags like <b>, <p>, <br> here)")
    date_posted = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
