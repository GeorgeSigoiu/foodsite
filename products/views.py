from django.http.response import JsonResponse
import io as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from html import escape
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, Content, Drink, Sauce
from collections import Counter
# Create your views here.

productsDict = []
productsList = []
pdfResponseDownload = None


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
    if len(productsDistinct) == 0:
        return redirect("/products/"+type)
    context = {
        "products": productsDistinct,
        "drinks": drinks,
        "tags": contents,
        "enabledTags": enabledTags,
        "type": type,
        "numberOfProducts": len(productsList),
    }
    return render(request, "products/products.html", context=context)


def prepareBill(request):
    global pdfResponseDownload
    requestDict = dict(request.POST)
    pdfResponseDownload = createBill(requestDict)
    # send email TODO
    global productsDict
    global productsList
    productsList = []
    productsDict = []
    return pdfResponseDownload


def downloadBill(request):
    global pdfResponseDownload
    return pdfResponseDownload

# -------------------------------------------------------------


def createBill(requestDict):
    name = trimString(requestDict["firstname"]) + \
        " "+trimString(requestDict["surname"])
    address = trimString(requestDict["deliveryAddress"])
    phone = trimString(requestDict["phone"])
    email = trimString(requestDict["email"])
    totalPrice = trimString(requestDict["priceTotal"])
    deliveryCost = "10"
    if int(totalPrice) > 60:
        deliveryCost = "0"
    global productsDict
    pdf = render_to_pdf(
        'bill.html',
        {
            'pagesize': 'A4',
            'name': name,
            'address': address,
            'phone': phone,
            'email': email,
            'products': productsDict,
            'productsPrice': totalPrice,
            'deliveryCost': deliveryCost,
        }
    )
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    return response


def trimString(string):
    result = str(string).replace("[", "").replace("]", "").replace("'", "")
    return result


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = dict(context_dict)
    html = template.render(context)
    result = StringIO.BytesIO()

    pdf = pisa.pisaDocument(StringIO.BytesIO(
        html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error generating PDF file")


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
