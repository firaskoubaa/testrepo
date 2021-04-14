from django.db import models

# Create your models here.
class BS_tab(models.Model):
    cover           = models.CharField(max_length=200)
    title           = models.CharField(max_length=500)
    subtitle        = models.CharField(max_length=500)
    authors         = models.CharField(max_length=200)
    publishedDate   = models.CharField(max_length=10)
    price           = models.CharField(max_length=12)
    previewlink     = models.CharField(max_length=200)
    itemid          = models.CharField(max_length=100)
