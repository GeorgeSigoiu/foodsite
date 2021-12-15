import users.views
from users.models import Bill
from django.http.response import JsonResponse
import io as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, Content, Drink, Sauce
from collections import Counter
from django.template.loader import render_to_string
import datetime
# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

productsDict = []
productsList = []
pdfResponseDownload = None
rendered_string_from_html = None


def showHomePage(request):  # home page
    context = get_context()
    return render(request, "home.html", context=context)


def showProductsCart(request):  # products intended to be bought
    global productsDict
    context = get_context(products=productsDict)
    return render(request, "products/buy_products.html", context=context)


def showProducts(request, typeof):  # show all products of type "type"
    products = Product.objects.filter(typeof=typeof)
    contents = Content.objects.filter(typeof=typeof)
    drinks = Drink.objects.all()
    context = get_context(contents=contents, drinks=drinks, products=products, typeof=typeof)
    return render(request, "products/products.html", context=context)


def get_context(contents=None, drinks=None, products=None, typeof=None, product=None, enabledTags=None):
    context = {
        "products": products,
        "product": product,
        "drinks": drinks,
        "tags": contents,
        "typeof": typeof,
        "enabledTags": enabledTags,
        "numberOfProducts": getNumberOfProducts(),
        "profile": getProfile(),
    }
    return context


def showSingleProduct(request, pk):  # show informations about one product
    product = Product.objects.get(id=pk)
    type1 = product.typeof
    products = Product.objects.filter(typeof=type1).exclude(title=product.title)
    drinks = Drink.objects.all()
    context = get_context(products=products, product=product, drinks=drinks)
    return render(request, "products/single_product.html", context=context)


def getProductsFromJS(request):  # getting products from javascript and adding to list
    response = handleRequestFromJs("append", request)
    return response


def deleteProductsFromJS(request):  # deleting products from list
    response = handleRequestFromJs("delete", request)
    return response


# showing the products containing search string in name or in its containings
def productsSearch(request):
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
    context = get_context(products=productsDistinct, drinks=drinks, contents=contents, typeof="search")
    if len(productsDistinct) == 0:
        productsNotFoundMessage = "Nu s-au gasit rezultate pentru '" + search + "'!"
        context["productsNotFound"] = productsNotFoundMessage
    return render(request, "products/products.html", context=context)


def productsSort(request, typeof):  # showing the products which containg some tags
    drinks = Drink.objects.all()
    contents = Content.objects.filter(typeof=typeof)
    allProducts = Product.objects.filter(typeof=typeof)
    requestResult = list(request.POST.items())
    products = []
    enabledTags = []
    for tagTitle, _ in requestResult:
        enabledTags.append(tagTitle)
    for product in allProducts:
        for tagTitle, enabled in requestResult:
            content = product.content.filter(title=tagTitle)
            if len(content) > 0:
                products.append(product)
    productsDistinct = set(products)
    if len(productsDistinct) == 0:
        return redirect("/products/" + typeof)
    context = get_context(products=productsDistinct, drinks=drinks, contents=contents, enabledTags=enabledTags,
                          typeof=typeof)
    return render(request, "products/products.html", context=context)


def prepareBill(request):  # preparing the bill and sending email
    result = doWork(request)
    requestDict = dict(request.POST)
    sendEmail(trimString(requestDict["email"]))
    return result


def downloadBill(request):  # downloading the bill and sending email
    doWork(request)
    requestDict = dict(request.POST)
    sendEmail(trimString(requestDict["email"]))
    return redirect("/")


# -------------------------------------------------------------


def sendEmail(receiverEmail):  # sending the email
    body = '''Buna ziua,
    
    Va multumim pentru comanda efectuata la noi!
    Atasata aveti factura.
    
    O zi frumoasa,
    Echipa G.G.
    '''
    # put your email here
    sender = 'pazvantialfredo@gmail.com'
    # get the password in the gmail (manage your google account, click on the avatar on the right)
    # then go to security (right) and app password (center)
    # insert the password and then choose mail and this computer and then generate
    # copy the password generated here
    password = 'tlbxatzunohicfxz'
    # put the email of the receiver here
    receiver = receiverEmail

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = '[Restaurant Cataleya] Comanda inregistrata'

    message.attach(MIMEText(body, 'plain'))

    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%S')
    pdfname = ("factura-comanda-" + timestamp + ".pdf").replace(":", "-")
    resultFile = open(pdfname, "w+b")

    # convert HTML to PDF
    global rendered_string_from_html
    pisa.CreatePDF(rendered_string_from_html, dest=resultFile)

    # close output file
    resultFile.close()

    # open the file in bynary
    binary_pdf = open(pdfname, 'rb')

    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload(binary_pdf.read())

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    # enable security
    session.starttls()

    # login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent')


def doWork(request):  # creating the bill and initializing the pdf-bill
    global pdfResponseDownload
    requestDict = dict(request.POST)
    pdfResponseDownload = createBill(requestDict)
    bill = addBillToDatabase(requestDict)
    profile = getProfile()
    if profile:
        profile.bills.add(bill)
        profile.save()
    resetProductList()
    return pdfResponseDownload


def resetProductList():
    global productsDict
    global productsList
    productsList = []
    productsDict = []


def createBill(requestDict):  # creates the bill in pdf format
    address, email, name, phone, totalPrice, deliveryCost = get_bill_information(requestDict)
    global productsDict
    global rendered_string_from_html
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d')
    productsToShow = []
    for product, number in productsDict.items():
        tup = (product, number, product.price * number)
        productsToShow.append(tup)
    context = {
        'pagesize': 'A4',
        'name': name,
        'address': address,
        'phone': phone,
        'email': email,
        'products': productsToShow,
        'productsPrice': totalPrice,
        'deliveryCost': deliveryCost,
        'timestamp': timestamp,
    }
    rendered_string_from_html = render_to_string('bill.html', context)
    pdf = render_to_pdf('bill.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="delivery_order.pdf"'
    return response


def addBillToDatabase(requestDict):  # creates the bill objects and then saves in database
    address, email, name, phone, totalPrice, deliveryCost = get_bill_information(requestDict)
    global productsDict
    products = ""
    for product, number in productsDict.items():
        products += str(product).replace(" ", "-") + " " + str(number) + " " + str(product.price * number) + ", "
    bill = Bill.Builder() \
        .set_name(name) \
        .set_email(email) \
        .set_address(address) \
        .set_phone(phone) \
        .set_products(products) \
        .set_price(totalPrice) \
        .build()
    bill.save()
    return bill


def get_bill_information(requestDict):  # split requestDict in more variables
    name = trimString(requestDict["firstname"]) + " " + trimString(requestDict["surname"])
    address = trimString(requestDict["deliveryAddress"])
    phone = trimString(requestDict["phone"])
    email = trimString(requestDict["email"])
    totalPrice = trimString(requestDict["priceTotal"])
    deliveryCost = "10"
    if int(totalPrice) > 60:
        deliveryCost = "0"
    else:
        totalPrice = int(totalPrice) + 10
    return address, email, name, phone, totalPrice, deliveryCost


def trimString(string):
    result = str(string).replace("[", "").replace("]", "").replace("'", "")
    return result


def render_to_pdf(template_src, context_dict):  # creates a pdf from html page
    template = get_template(template_src)
    context = dict(context_dict)
    html = template.render(context)
    result = StringIO.BytesIO()
    pdf = pisa.pisaDocument(StringIO.BytesIO(
        html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error generating PDF file")


def handleRequestFromJs(instruction, request):  # gets the product list from js
    global productsDict
    global productsList
    intermediateList = []
    data = {}
    if request.method == "POST":
        foodProducts = dict(request.POST)["market[]"]
        for product_id in foodProducts:
            try:
                prod = Product.objects.get(id=product_id)
                intermediateList.append(prod)
            except:
                drink = Drink.objects.get(id=product_id)
                intermediateList.append(drink)
        if instruction == "delete":
            productsList.remove(intermediateList[0])
        elif instruction == "append":
            productsList.extend(intermediateList)
        productsDict = dict(Counter(productsList))
    elif request.method == "GET":
        data = {
            "numberOfProducts": len(productsList),
        }
    return JsonResponse(data)


def getProductsByTitle(search, allProducts):  # searching for products which contains a string in their names
    result = []
    for product in allProducts:
        if search in product.title.lower():
            result.append(product)
    return result


def getProductsByContent(search, allProducts):  # searching from products which contains some tags
    result = []
    for prod in allProducts:
        content = prod.content.filter(title__contains=search)
        if len(content) > 0:
            result.append(prod)
    return result


def getProfile():  # gets the user who is logged in
    profile = users.views.getProfileLoggedIn()
    return profile


def getNumberOfProducts():  # gets the number of products from cart
    global productsList
    numberOfProducts = len(productsList)
    return numberOfProducts
