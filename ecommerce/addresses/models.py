from django.db import models
from billing.models import BillingProfile


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


# Create your models here.
class Address(models.Model):
    billing         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type    = models.CharField(max_length = 120, choices= ADDRESS_TYPES)
    address_line1   = models.CharField(max_length = 120) 
    address_line1   = models.CharField(max_length = 120, null = True, blank = True)
    city            = models.CharField(max_length = 120)
    state           = models.CharField(max_length = 120)
    country         = models.CharField(max_length = 120, default = 'India')
    zip             = models.CharField(max_length = 120)

    def __str__(self):
        return str(self.billing)