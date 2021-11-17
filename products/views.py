import webbrowser
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

import products
from .models import Product, Content, Drink, Sauce
from collections import Counter
# Create your views here.

productsForBuying = []
productsToBuy = []


def showHomePage(request):
    context = {
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "home.html", context=context)


def showProductsCart(request):
    global productsForBuying
    global productsToBuy
    context = {
        "products": productsForBuying,
        "numberOfProducts": len(productsToBuy),
    }

    return render(request, "products/buy_products.html", context=context)


def showProducts(request, type):
    products = Product.objects.filter(typeof=type)
    contents = Content.objects.filter(typeof=type)
    drinks = Drink.objects.all()
    context = {
        "products": products,
        "drinks": drinks,
        "tags": contents,
        "type": type,
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "products/products.html", context=context)


def showSingleProduct(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "products/single-product.html", context=context)


def getProductsFromJS(request):
    global productsForBuying
    global productsToBuy
    data = {}
    if request.method == "POST":
        foodProducts = dict(request.POST)["market[]"]
        for id in foodProducts:
            try:
                prod = Product.objects.get(id=id)
                productsToBuy.append(prod)
            except:
                drink = Drink.objects.get(id=id)
                productsToBuy.append(drink)
        productsForBuying = dict(Counter(productsToBuy))

    elif request.method == "GET":
        numberOfProducts = len(productsToBuy)
        data = {
            "numberOfProducts": numberOfProducts,
        }
    return JsonResponse(data)


def productsSearch(request):
    global productsToBuy
    search = request.POST.get("search", "")
    allProducts = Product.objects.all()
    drinks = Drink.objects.all()
    productsByName = getProductsByTitle(search.lower(), allProducts)
    productsByContent = getProductsByContent(search.lower(), allProducts)
    products = []
    products.extend(productsByName)
    products.extend(productsByContent)
    productsDistinct = Counter(products)
    contents = Content.objects.all()
    context = {
        "products": productsDistinct,
        "drinks": drinks,
        "tags": contents,
        "type": "search",
        "numberOfProducts": len(productsToBuy),
    }
    return render(request, "products/products.html", context=context)

# -------------------------------------------------------------


def getProductsByTitle(search, allProducts):
    result = []
    for product in allProducts:
        if search in product.title.lower():
            result.append(product)
    return result


def getProductsByContent(search, allProducts):
    result = []
    for prod in allProducts:
        content = prod.content.filter(name__contains=search)
        if len(content) > 0:
            result.append(prod)
    return result
