from django.shortcuts import render
from .models import Product, Content
# Create your views here.


def showProducts(request, type):
    products = Product.objects.filter(typeof=type)
    contents = Content.objects.filter(typeof=type)
    context = {
        "products": products,
        "tags": contents,
        "type": type,
    }
    return render(request, "products/products.html", context)


def showSingleProduct(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, "products/single-product.html", context)
