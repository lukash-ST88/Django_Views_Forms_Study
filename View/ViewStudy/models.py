from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
# Create your models here.



class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')
    last_accessed = models.DateTimeField(default=timezone.now)
    d = models.IntegerField(null=True)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs): # автоматически создаем слаг при сохранении
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs) #когда в методе save находился аргумент self, возникала ошибка IntegrityError

    def get_absolute_url(self):
        return reverse('DVpattern', kwargs={'slug1': self.slug})

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()

    def __str__(self):
        return self.title

