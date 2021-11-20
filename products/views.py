from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import Product, Content, Drink, Sauce
from collections import Counter
# Create your views here.

productsDict = []
productsList = []


def showHomePage(request):
    context = {
        "numberOfProducts": len(productsList),
    }
    return render(request, "home.html", context=context)


def showProductsCart(request):
    global productsDict
    global productsList
    context = {
        "products": productsDict,
        "numberOfProducts": len(productsList),
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
        "numberOfProducts": len(productsList),
    }
    return render(request, "products/products.html", context=context)


def showSingleProduct(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
        "numberOfProducts": len(productsList),
    }
    return render(request, "products/single_product.html", context=context)


def getProductsFromJS(request):
    response = handleRequestFromJs("append", request)
    return response


def deleteProductsFromJS(request):
    response = handleRequestFromJs("delete", request)
    return response


def productsSearch(request):
    global productsList
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
        "numberOfProducts": len(productsList),
    }
    if len(productsDistinct) == 0:
        productsNotFoundMessage = "Nu s-au gasit rezultate pentru '"+search+"'!"
        context["productsNotFound"] = productsNotFoundMessage
    return render(request, "products/products.html", context=context)


def productsSort(request, type):
    drinks = Drink.objects.all()
    contents = Content.objects.filter(typeof=type)
    allProducts = Product.objects.filter(typeof=type)
    requestResult = list(request.POST.items())
    products = []
    enabledTags = []
    for tagTitle, enabled in requestResult:
        enabledTags.append(tagTitle)
    for product in allProducts:
        for tagTitle, enabled in requestResult:
            content = product.content.filter(title=tagTitle)
            if len(content) > 0:
                products.append(product)
    productsDistinct = set(products)
    context = {
        "products": productsDistinct,
        "drinks": drinks,
        "tags": contents,
        "enabledTags": enabledTags,
        "type": type,
        "numberOfProducts": len(productsList),
    }
    return render(request, "products/products.html", context=context)
# -------------------------------------------------------------


def handleRequestFromJs(instruction, request):
    global productsDict
    global productsList
    intermediateList = []
    data = {}
    if request.method == "POST":
        foodProducts = dict(request.POST)["market[]"]
        for id in foodProducts:
            try:
                prod = Product.objects.get(id=id)
                intermediateList.append(prod)
            except:
                drink = Drink.objects.get(id=id)
                intermediateList.append(drink)
        if instruction == "delete":
            productsList.remove(intermediateList[0])
        elif instruction == "append":
            productsList.extend(intermediateList)
        productsDict = dict(Counter(productsList))
    elif request.method == "GET":
        numberOfProducts = len(productsList)
        data = {
            "numberOfProducts": numberOfProducts,
        }
    return JsonResponse(data)


def getProductsByTitle(search, allProducts):
    result = []
    for product in allProducts:
        if search in product.title.lower():
            result.append(product)
    return result


def getProductsByContent(search, allProducts):
    result = []
    for prod in allProducts:
        content = prod.content.filter(title__contains=search)
        if len(content) > 0:
            result.append(prod)
    return result
