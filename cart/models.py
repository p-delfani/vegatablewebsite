from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    total_price = models.IntegerField(default=0, verbose_name='قیمت نهایی')
    products = models.ManyToManyField(Product, blank=True, null=True, related_name='orders', verbose_name='محصولات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    address = models.TextField(default='-', verbose_name='آدرس')
    discount_code = models.ForeignKey('DiscountCode', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='orders', verbose_name='تخفیف')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name='محصول')
    size = models.CharField(max_length=12, null=True, blank=True, verbose_name='سایز')
    quantity = models.SmallIntegerField(verbose_name='تعداد')
    price = models.PositiveIntegerField(verbose_name='قیمت')

    def __str__(self):
        return self.order.user.email

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'اقلام سفارش'


class DiscountCode(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام کد تخفیف')
    discount = models.SmallIntegerField(default=0, verbose_name='درصد تخفیف')
    quantity = models.SmallIntegerField(default=1, verbose_name='تعداد')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'
