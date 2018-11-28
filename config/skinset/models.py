from django.db import models


class CropImage(models.Model):
    name = models.CharField(max_length=128)
    imgrect = models.CharField(max_length=64)
    file = models.CharField(max_length=256)
    source_path = models.CharField(max_length=256)
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.name
