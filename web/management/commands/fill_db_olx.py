import random
import shutil

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from mixer.backend.django import mixer
from factory import LazyAttribute
from factory.django import ImageField as IF
import requests
from io import BytesIO
from uuid import uuid4

from web.models import User, Advert, Media
from web.utils import category_dict

category_for_adverts = [item for item in category_dict.keys()]

class ImageField(IF):
    def _make_data(self, params):
        width = params.get('width', 100)
        url = f'https://picsum.photos/{width}'
        resp = requests.get(url)
        return BytesIO(resp.content).getvalue()


def get_image(size=128):
    def inner():
        return ContentFile(ImageField()._make_data({'width': size}), f'{uuid4().hex}.jpeg')
    return inner


class Command(BaseCommand):

    USER_COUNT = 10
    MIN_ADVERT_COUNT = 5
    MAX_ADVERT_COUNT = 5
    MIN_MEDIA_PER_ADVERT = 3
    MAX_MEDIA_PER_ADVERT = 3

    models = (User, Advert)

    def clear_models(self):
        try:
            shutil.rmtree(settings.MEDIA_FOLDER)
        except FileNotFoundError as e:
            pass
        for model in self.models:
            model.objects.all().delete()

    def generate_users(self):
        users = mixer.cycle(self.USER_COUNT).blend(User, avatar=get_image(1024), phone_number='+380(93)-000-00-00')
        for user in users:
            user.set_password('user123')
            user.save()
        return users

    def generate_adverts(self, users):
        adverts = []
        for user in users:
            for _ in range(random.randint(self.MIN_ADVERT_COUNT, self.MAX_ADVERT_COUNT)):
                advert = mixer.blend(Advert, user=user, category=random.choice(category_for_adverts))
                adverts.append(advert)
        return adverts

    def generate_media(self, adverts):
        medias = []
        for advert in adverts:
            for _ in range(random.randint(self.MIN_MEDIA_PER_ADVERT, self.MAX_MEDIA_PER_ADVERT)):
                media = mixer.blend(Media, advert=advert, image=get_image(1024))
                medias.append(media)
        return medias

    def handle(self, *args, **options):
        self.clear_models()
        print('Clear models.')

        users = self.generate_users()
        print('Users created')
        adverts = self.generate_adverts(users)
        print('Adverts created')
        media = self.generate_media(adverts)
        print('Media created')
        print('Done!')