from django.db import models
from django.urls import reverse


class Size(models.Model):
    title = models.CharField(max_length=10, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'


class Category(models.Model):
    title = models.CharField(max_length=70, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    title = models.CharField(max_length=80, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته بندی')
    price = models.IntegerField(verbose_name='قیمت')
    discount = models.IntegerField(blank=True, null=True, verbose_name='قیمت با تخفیف (این فیلد میتواند خالی باشد.)')
    image = models.ImageField(upload_to='img/products', verbose_name='تصویر')
    size = models.ManyToManyField(Size, blank=True, related_name='products', verbose_name='سایز')
    availibility = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name='موجودی (کیلوگرم. این فیلد میتواند خالی باشد.)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product:product-detail", kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
