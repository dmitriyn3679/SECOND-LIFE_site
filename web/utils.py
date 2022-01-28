from web.models import Advert, Media
import datetime
import pytz

utc = pytz.UTC

category_dict = {
    'detskiy-mir': 'Дитячий світ',
    'nedvizhimost': 'Нерухомість',
    'transport': 'Авто',
    'zapchasti-dlya-transporta': 'З/ч для транспорта',
    'rabota': 'Робота',
    'uslugi': 'Бізнес та послуги',
    'Moda': 'Мода і стиль',
    'novostroyki': 'Новобудови',
    'zhivotnye': 'Тварини',
    'dom-i-sad': 'Дім і сад',
    'elektronika': 'Електроніка',
    'hobbi-otdyh-i-sport': 'Хобі'
}

#TIME_TO_LIVE = datetime.second()

def generate_categories_dict():
    categories_dict = {}
    for item in category_dict.keys():
        categories_dict.setdefault(item, {})
    return categories_dict


#def update_categories_dict():
#    categories_dict = generate_categories_dict()
#    adverts = Advert.objects.all()
#    for advert in adverts:
#        categories_dict.get(advert.category).setdefault()
#    return categories_dict


#def generate_adverts():
#    adverts_list = []
#    adverts = Advert.objects.all()
#    for advert in adverts:
#        print(utc.localize(datetime.datetime.now()))
#        if advert.pub_date + datetime.timedelta(hours=2, minutes=15) > utc.localize(datetime.datetime.now()):
#            adverts_list.append(advert)
#    return adverts_list


def generate_data(count_adverts=4, count_image=1):
    categories_dict = generate_categories_dict()
    #adverts = generate_adverts()
    adverts = Advert.objects.all()
    media = Media.objects.all()
    for category in categories_dict:
        for advert in adverts:
            if advert.category == category:
                if len(categories_dict.get(advert.category).keys()) < count_adverts:
                    categories_dict.get(advert.category).setdefault(advert, [])
                    for image in media:
                        if image.advert_id == advert.id:
                            if len(categories_dict.get(advert.category).get(advert)) < count_image:
                                categories_dict.get(advert.category).get(advert).append(image)
    return categories_dict





