from django.shortcuts import render
from .models import Product, Content
# Create your views here.


def showProducts(request,type):
    products = Product.objects.all()
    contents = Content.objects.all()
    context = {
        "products": products,
        "tags": contents,
        "type": type,
    }
    return render(request, "products/products.html", context)


def showSingleProduct(request, pk):
    return render(request, "products/single-product.html")
