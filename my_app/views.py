import requests
from urllib.parse import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_TEST_URL = 'https://www.jumia.com.ng/catalog/?q={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_TEST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class': 'core'})

    final_posting = []
    for post in post_titles:
        post_title = post.find(class_='name').text
        post_image = post.find(class_='img').get('data-src')
        post_url = post.get('href')
        if post.find(class_='prc'):
            post_price = post.find(class_='prc').text
        else:
            post_price = post.find(class_='prc').text
        final_posting.append((post_title, post_price, post_image, post_url))

    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
