import requests 
import requests_cache 
import json 

#setup our api cache location (this is going to make a temporary database storage for our api calls)

requests_cache.install_cache('image_cache', backend='sqlite')


def get_image(search):
    # 4 parts to every api:
    # url Required
    # queries/paremeters Optional
    # headers/authorization Optional
    # body/posting Optional
    
    url = "https://google-search72.p.rapidapi.com/imagesearch/"

    querystring = {"q": search,"gl":"us","lr":"lang_en","num":"10","start":"0"}

    headers = {
        "X-RapidAPI-Key": "5bb8b6eab7msh7111c8bf2c05cd2p139b99jsn519fe659662c",
        "X-RapidAPI-Host": "google-search72.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    # print(data)

    img_url = ""

    if 'items' in data.keys():
           img_url = data['items'][0]['originalImageUrl'] 

    return img_url