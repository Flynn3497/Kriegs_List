import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from urllib.parse import quote_plus
from . import models


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL =  'http://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(searches=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')  # to parse html data into bs4 object bs4 = beau soup
    # coz in inspect elements result row/title/price is
    # the class of all the hyperlinks in og craigslist website # print(data) #print(post_titles[1].text)

    post_listings =  soup.find_all('li', {'class':'result-row'})
    final_postings =[]
    for post in post_listings:
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        post_title = post.find(class_='result-title hdrlnk').text
        post_url = post.find('a').get('href')

        if post.find(class_ ='result-image').get('data-ids'):
            post_image_id = post.find(class_ ='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)

        else:
            post_image_url = 'https://i.ibb.co/q5c4SXg/8bafe6e2-0076-42a6-8354-4e2047ca0485-200x200.png'
        final_postings.append((post_title, post_url,post_image_url,post_price))

    search_res = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'my_app/new_search.html', search_res)
