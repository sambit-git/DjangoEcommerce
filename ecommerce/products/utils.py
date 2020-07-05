import random
import string

from django.utils.text import slugify

def unique_string_generator(size = 10, characters = string.ascii_lowercase+string.digits):
    return ''.join(random.choice(characters) for _ in range(size))

def unique_slug_generator(instance, new_slug = None):
    if new_slug is None:
        slug = slugify(instance.title)
    else:
        slug = new_slug

    klass = instance.__class__
    qs = klass.objects.filter(slug = slug)
    if qs.exists():
        return unique_slug_generator(instance, f'{slug}-{unique_string_generator(4)}')
    return slug