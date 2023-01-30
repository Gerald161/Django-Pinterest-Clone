from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


# Create your models here.
class Pin(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True)
    image = models.ImageField()

    def __str__(self):
        return str(self.slug)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # if self.image:
        #     if self.image.size > 35000:
        #         im = Image.open(self.image)
        #
        #         width, height = im.size
        #
        #         output = BytesIO()
        #
        #         if self.image.size >= 10000000:
        #             im = im.resize((width // 20, height // 20), Image.ANTIALIAS)
        #         elif self.image.size >= 5000000:
        #             im = im.resize((width // 10, height // 10), Image.ANTIALIAS)
        #         elif self.image.size >= 4000000:
        #             im = im.resize((width // 6, height // 6), Image.ANTIALIAS)
        #         elif self.image.size >= 2000000:
        #             im = im.resize((width // 4, height // 4), Image.ANTIALIAS)
        #         elif self.image.size >= 1000000:
        #             im = im.resize((width // 3, height // 3), Image.ANTIALIAS)
        #         elif self.image.size >= 800000:
        #             im = im.resize((width // 2, height // 2), Image.ANTIALIAS)
        #         elif self.image.size >= 500000:
        #             im = im.resize((width // 5, height // 5), Image.ANTIALIAS)
        #         elif self.image.size >= 300000:
        #             im = im.resize((width // 4, height // 4), Image.ANTIALIAS)
        #         elif self.image.size >= 150000:
        #             im = im.resize((width // 3, height // 3), Image.ANTIALIAS)
        #         elif self.image.size >= 100000:
        #             im = im.resize((width // 2, height // 2), Image.ANTIALIAS)
        #         else:
        #             im = im.resize((width // 2, height // 2), Image.ANTIALIAS)
        #
        #         rgb_im = im.convert('RGB')
        #
        #         rgb_im.save(output, format='JPEG', quality=70)
        #
        #         output.seek(0)
        #
        #         self.additional_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',sys.getsizeof(output), None)

        super().save(*args, **kwargs)

    def save_without_images(self, *args, **kwargs):
        super().save(*args, **kwargs)