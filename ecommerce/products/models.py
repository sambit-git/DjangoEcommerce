# python modules
import os
import random

# Django modules
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

# user defined modules
from .utils import unique_slug_generator

# user defined functions
def get_filename_ext(filename):
    basename = os.path.basename(filename)
    return os.path.splitext(basename)


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    name = str(random.randint(1, 9682152190))
    return f'products/{name}/{name}{ext}'



# Custom QuerySet
class ProductQueryset(models.query.QuerySet):
    def all(self):
        return self.filter(active = True)
    def featured(self):
        return self.filter(featured = True)

    def get_by_id(self, id):
        qs = self.filter(id=id)
        if qs.exists() and qs.count() == 1:
            return qs.first()
        return None
    
    def get_by_slug(self, slug):
        qs = self.filter(slug = slug)
        if qs.exists() and qs.count() == 1:
            return qs.first()
        return None


# Custom modelManager
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(model=self.model, using=self._db)
    
    def get_by_id(self, id = None):
        return self.get_queryset().get_by_id(id)
    
    def get_by_slug(self, slug):
        return self.get_queryset().get_by_slug(slug)

    def featured(self):
        return self.get_queryset().featured()
    
    def search(self, query = None):
        lookups = Q(title__icontains = query) | Q(description__icontains = query) | Q(price__icontains = query) | Q(tag__title__icontains = query)
        return self.get_queryset().filter(lookups).distinct()
    

# Product Model
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank = True, null= True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    


    objects = ProductManager()

    def __str__(self):
        return str(self.id)+" - "+self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug' : self.slug})



# signal receivers
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = unique_slug_generator(instance)


# signals
pre_save.connect(product_pre_save_receiver, sender=Product)