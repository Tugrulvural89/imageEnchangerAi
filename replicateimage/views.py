import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from replicate.exceptions import ReplicateError

from .forms import ImageUploadForm
from django.http import FileResponse, HttpResponse
from PIL import Image
from io import BytesIO
from .forms import ContactForm
from .models import Contact, CustomPage, Blog
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from decouple import config
import replicate


def index(request):
    REPLICATE_API_TOKEN = config('REPLICATE_API_TOKEN')
    # Set the REPLICATE_API_TOKEN environment variable
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    seed = config('SEED', default=1337, cast=int)
    prompt = config('PROMPT')
    dynamic = config('DYNAMIC', cast=int)
    sd_model = config('SD_MODEL')
    scheduler = config('SCHEDULER')
    creativity = config('CREATIVITY', cast=float)
    lora_links = config('LORA_LINKS')
    downscaling = config('DOWNSCALING', cast=bool)
    resemblance = config('RESEMBLANCE', cast=float)
    scale_factor = config('SCALE_FACTOR', cast=int)
    tiling_width = config('TILING_WIDTH', cast=int)
    tiling_height = config('TILING_HEIGHT', cast=int)
    custom_sd_model = config('CUSTOM_SD_MODEL')
    negative_prompt = config('NEGATIVE_PROMPT')
    num_inference_steps = config('NUM_INFERENCE_STEPS', cast=int)
    downscaling_resolution = config('DOWNSCALING_RESOLUTION', cast=int)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            myForm = form.save(commit=False)
            myForm.description = form.cleaned_data['description']
            myForm.save()
            # Use request.build_absolute_uri() to build the full URL
            full_url = request.build_absolute_uri(settings.MEDIA_URL + myForm.image.name)
            try:
                output = replicate.run(
                    "philz1337x/clarity-upscaler:67f36b842ae88c238b2332d34630cc325f25ee14e9b50a188d6eca1a2a77816c",
                    input={
                        "seed": seed,
                        "image": full_url,
                        "prompt": prompt + myForm.description,
                        "dynamic": dynamic,
                        "sd_model": sd_model,
                        "scheduler": scheduler,
                        "creativity": creativity,
                        "lora_links": lora_links,
                        "downscaling": downscaling,
                        "resemblance": resemblance,
                        "scale_factor": scale_factor,
                        "tiling_width": tiling_width,
                        "tiling_height": tiling_height,
                        "custom_sd_model": custom_sd_model,
                        "negative_prompt": negative_prompt,
                        "num_inference_steps": num_inference_steps,
                        "downscaling_resolution": downscaling_resolution
                    }
                )
                output_url = output[0]
            except ReplicateError as e:
                print(f"An error occurred: {e.status} - {e.detail}")
                output_url = f"An error occurred: {e.status} - {e.detail}"
            return render(request, 'index.html', {'output_url': output_url, 'full_url': full_url})
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We will reach out to you as soon as possible.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def custom_page(request, slug=None):
    content = get_object_or_404(CustomPage, slug=slug)
    return render(request, 'custom.html', {'content': content})


def blog(request):
    blog_list = Blog.objects.all().order_by('-publish')  # Assuming there's a date_posted field
    paginator = Paginator(blog_list, 10)  # Show 10 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})


def blog_detail(request, slug=None):
    blogDetail = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'post': blogDetail})


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Allow: /",
        "Sitemap: https://www.imageupgradeai.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
