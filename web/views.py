from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from web.models import Advert, Media
from web.utils import generate_categories_dict, generate_data
from web.forms import SignUpForm, AdvertForm, MediaForm


def start_page(request):
    all_data = generate_data(count_adverts=4, count_image=1)
    return render(request, 'web/menu.html', context={'categories': all_data})


def advert(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    return render(request, 'web/advert.html', context={'advert': advert})


def all_in_category(request, category):
    all_data = generate_data(count_adverts=float('inf'), count_image=1)
    adverts = all_data.get(category)
    return render(request, 'web/all_in_category.html', context={'category': category, 'adverts': adverts})


def create_advert(request):
    if request.method == 'POST':
        advert_form = AdvertForm(request.POST)
        media_form = MediaForm(request.POST)
        if advert_form.is_valid() or media_form.is_valid():
            advert = advert_form.save(commit=False)
            advert.user = request.user
            advert.save()
            media = request.FILES.getlist('media')
            for image in media:
                item = Media(image=image, advert=advert)
                item.save()
            return redirect('web:start_page')
    else:
        advert_form = AdvertForm()
        media_form = MediaForm()
    return render(request, 'web/create_advert.html', {'advert_form': advert_form, 'media_form': media_form})


def edit_profile(request):
    return render(request, 'web/edit_profile.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth:login')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', context={'form': form})