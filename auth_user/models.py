from django.db import models


class Image(models.Model):
    image = models.FileField(upload_to='account_image')
