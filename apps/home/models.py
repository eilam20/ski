# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True, verbose_name="תאריך החזרה")
    name = models.CharField(blank=True, null=True, max_length=255, verbose_name="שם")
    place = models.CharField(blank=True, null=True, max_length=255, verbose_name="מקום")
    notes = models.CharField(blank=True, null=True, max_length=255, verbose_name="הערות")
    pack = models.IntegerField(blank=True, null=True, verbose_name="חליפות")
    coat = models.IntegerField(blank=True, null=True, verbose_name="מעילים")
    pants = models.IntegerField(blank=True, null=True, verbose_name="מכנסיים")
    phone = models.CharField(blank=True, null=True, max_length=10, verbose_name="טלפון")
    done = models.BooleanField(default=False, verbose_name="הוחזר")



def __str__(self):
        return f'{self.name}-{self.phone}'