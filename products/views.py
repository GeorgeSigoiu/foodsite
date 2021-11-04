import webbrowser
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

import products
from .models import Product, Content
from collections import Counter
# Create your views here.

productsForBuying = []
productsToBuy = []


def showHomePage(request):
    context = {
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "home.html", context)


def openLocationOnMaps(request, map_string):
    webbrowser.open('https://www.google.com/maps/place/' + map_string)
    context = {
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "home.html", context)


def showProductsCart(request):
    global productsForBuying
    context = {
        "products": productsForBuying,
        "numberOfProducts": len(productsToBuy),
    }
    print("PRODUCTS CART: ", productsForBuying)
    return render(request, "products/buy_products.html", context)


def showProducts(request, type):
    products = Product.objects.filter(typeof=type)
    contents = Content.objects.filter(typeof=type)
    context = {
        "products": products,
        "tags": contents,
        "type": type,
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "products/products.html", context)


def showSingleProduct(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "products/single-product.html", context)


def transferBetweenDJandJS(request):
    global productsForBuying
    global productsToBuy
    data = {}
    if request.method == "POST":
        productsInMarket = dict(request.POST)["market[]"]
        for id in productsInMarket:
            prod = Product.objects.get(id=id)
            productsToBuy.append(prod)
        productsForBuying = dict(Counter(productsToBuy))
        print(productsForBuying)
    elif request.method == "GET":
        numberOfProducts = len(productsToBuy)
        data = {
            "numberOfProducts": numberOfProducts,
        }
    return JsonResponse(data)


def productsSearch(request):
    search = request.POST.get("search", "")
    allProducts = Product.objects.all()
    print(allProducts)
    productsByName = getProductsByTitle(search.lower(), allProducts)
    print(productsByName)
    context = {
        "products": productsByName,
        "type": "search",
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "products/products.html", context)


# -------------------------------------------------------------
def getProductsByTitle(search, allProducts):
    result = []
    for product in allProducts:
        if search in product.title.lower():
            result.append(product)
    return result
