from django.contrib import admin
from .models import Blog, UploadedImage, Contact, CustomPage


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'text')
    prepopulated_fields = {'slug': ('title',)}


class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content')
    search_fields = ('name', 'email')


class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('tag', 'title', 'text', 'image', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Blog, BlogAdmin)
admin.site.register(UploadedImage, UploadedImageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(CustomPage, CustomPageAdmin)
