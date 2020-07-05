import random
import string

from django.utils.text import slugify

def unique_string_generator(size = 10, characters = string.ascii_uppercase+string.digits):
    return ''.join(random.choice(characters) for _ in range(size))

def unique_id_generator(instance, new_slug = None):
    if new_slug is None:
        slug = slugify("ORD")
    else:
        slug = new_slug

    klass = instance.__class__
    qs = klass.objects.filter(orderid = slug)
    if qs.exists():
        return unique_id_generator(instance, f'{slug}-{unique_string_generator(4)}')
    return slug