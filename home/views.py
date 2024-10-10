from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from product.models import Product
from .forms import ContactUsForm


class HomeView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        return render(request, 'home/home.html', {'products': products})


class AboutUsView(TemplateView):
    template_name = 'home/about.html'


class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'home/contact.html', {'form': form})

    def post(self, request):
        form = ContactUsForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')

        return render(request, 'home/contact.html', {'form': form})
