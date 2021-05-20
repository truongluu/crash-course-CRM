from django.db import models
from django.db.models.deletion import CASCADE

from typing import Set
from django.utils.translation import gettext_lazy as _

# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin


# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser
#         disabled_fields = set()  # type: Set[str]

#         if not is_superuser:
#             disabled_fields |= {
#                 'username',
#                 'is_superuser',
#                 'user_permissions',
#             }

#         for f in disabled_fields:
#             if f in form.base_fields:
#                 form.base_fields[f].disabled = True

#         return form
# # Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customer')

    def __str__(self):
        return self.name

    @property
    def orders(self):
        order_count = self.order_set.all().count()
        return str(order_count)


class Product(models.Model):

    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField()
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Product')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')

    def __str__(self):
        return str(self.product)


# RELATED SET EXAMLE
# class ParentModel(models.Model):
#     name = models.CharField(max_length=100, null=True)
#     created = models.DateField(auto_now_add=True)


# class ChildModel(models.Model):
#     parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     created = models.DateField(auto_now_add=True)
