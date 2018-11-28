from django.db import models


class CropImage(models.Model):
    name = models.CharField(max_length=128)
    imgrect = models.CharField(max_length=64)
    file = models.CharField(max_length=256)
    source_path = models.CharField(max_length=256)
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class SkinImage(models.Model):
    # from <skinset>
    skin_category = models.CharField(max_length=128)
    # from <skin>
    skin_name = models.CharField(max_length=128)
    texture = models.CharField(max_length=256)
    # from <img>
    name = models.CharField(max_length=128)
    imgrect = models.CharField(max_length=64)

    def __str__(self):
        return '{}/{}/{}'.format(self.skin_category, self.skin_name, self.name)

