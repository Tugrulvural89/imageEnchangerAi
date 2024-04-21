# myapp/context_processors.py

from .models import CustomPage  # Adjust the import according to your app structure and model location


def products_footer(request):
    # This function fetches pages/posts with the tag 'our products'
    products_pages = CustomPage.objects.filter(tag__icontains='our products')
    privacy_pages = CustomPage.objects.filter(tag__icontains='privacy_pages')
    about_pages = CustomPage.objects.filter(tag__icontains='about')
    return {'products_pages': products_pages, 'privacy_pages': privacy_pages, 'about_pages': about_pages}
