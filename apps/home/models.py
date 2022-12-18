# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    place = models.CharField(blank=True, null=True, max_length=255)
    notes = models.CharField(blank=True, null=True, max_length=255)
    pack = models.IntegerField(blank=True, null=True)
    coat = models.IntegerField(blank=True, null=True)
    pants = models.IntegerField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=10)


    def __str__(self):
        return f'{self.name}-{self.phone}'