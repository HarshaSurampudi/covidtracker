from django.db import models

class PhoneNumber(models.Model):
    wap_number = models.CharField(max_length=15)
    def __str__(self):
        return self.wap_number
