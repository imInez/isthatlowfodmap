import os
from io import StringIO
from tempfile import NamedTemporaryFile
from urllib import request
from urllib.request import Request, urlopen

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import models
from django.urls import reverse
from PIL import Image

from analyzer.utils.safety import calculate_safety


def get_admin_user():
    return get_user_model().objects.get_or_create(username='inez')

class Meal(models.Model):
    meal_name = models.CharField(max_length=100)
    ingredients = models.TextField()
    tokens = models.TextField(blank=True)
    results = models.TextField(blank=True)
    safety =  models.TextField(blank=True)
    meal_url = models.URLField(blank=True)
    image_file = models.ImageField(default='default_big.jpg', upload_to='meals_images', blank=True)
    image_url = models.URLField(blank=True, max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_admin_user))
    collectors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meals_collected', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meal_name

    def get_absolute_url(self):
        return reverse('cards:meal_details', args=[self.id])

    def get_image_from_url(self, *args, **kwargs):
        if self.image_url and self.image_file.name == 'default_big.jpg':
                img_temp = NamedTemporaryFile(delete=True)
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                                         'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;'
                                     'q=0.9,image/webp,*/*;q=0.8'}
                req = Request(url=self.image_url, headers=headers)
                img_temp.write(urlopen(req).read())
                img_temp.flush()
                self.image_file.save(f"image_{self.meal_name}.jpg", File(img_temp))
                self.save()

    def resize_image(self):
        img = Image.open(self.image_file.path)
        if img.height > img.width:
            img = img.rotate(90, expand=True)
        if img.width > 350 or img.height > 285:
            output_size = (350, 285)
            img.thumbnail(output_size)
            img.save(self.image_file.path)

    def upload_safety(self):
        self.safety = calculate_safety(self.results)

    def save(self, *args, **kwargs):
        if self.image_url:
            self.get_image_from_url()
            # self.resize_image()
            # make aws lambda function
        self.upload_safety()
        super(Meal, self).save(*args, **kwargs)
