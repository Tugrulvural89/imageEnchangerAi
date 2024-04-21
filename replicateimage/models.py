from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    text = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set on create only
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on every save
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='static/blog_images/')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='static/uploaded_images/')
    description = models.TextField(blank=True, max_length=150, null=True)






class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"



class CustomPage(models.Model):
    tag = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='static/pages_images/')
    slug = models.SlugField(unique=True, max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # Eğer slug alanı boş ise, başlıktan slug oluştur
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('custom_page', kwargs={'slug': self.slug})


