from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    paginate_by = 2
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        related_products = Product.objects.all().order_by('-created_at')[:4]
        return render(request, 'product/product_detail.html',
                      {'product': product, 'related_products': related_products})


class CategoryProductView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        categories = Category.objects.all()
        products = category.products.all()
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        objects_list = paginator.get_page(page_number)
        return render(request, 'product/category_products.html',
                      {'products': objects_list, 'categories': categories, 'current_category': category})
