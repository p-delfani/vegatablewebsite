from django.db import models
from django.urls import reverse

from account.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='نویسنده')
    title = models.CharField(max_length=80, verbose_name='عنوان')
    text = models.TextField(verbose_name='متن')
    image = models.ImageField(upload_to='img/blog/posts', verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'


class BlogComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blog_comments', verbose_name='پست')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='کامنت والد')
    text = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
