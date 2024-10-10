from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=70, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    subject = models.CharField(max_length=70, verbose_name='موضوع')
    text = models.TextField(verbose_name='متن')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'پبام'
        verbose_name_plural = 'پیام ها'
