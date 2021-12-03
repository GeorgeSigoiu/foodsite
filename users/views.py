from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
import products.views

from users.models import Bill, Profile

profile_logged_in = None


def profiles(request):
    return render(request, 'users/profiles.html')


def createUser(request):
    result = dict(request.POST)
    username = trim(result["username"])
    email = trim(result["email"])
    password = trim(result["password"])
    existsUsername = len(Profile.objects.filter(username=username)) > 0
    if existsUsername:
        return render(request, "login.html", {"message": "Exista deja acest utilizator!"})
    if len(username) == 0 or len(password) == 0 or len(email) == 0:
        return render(request, "login.html",
                      {"message": "Nu se poate crea contul: toate campurile trebuie completate!"})

    profile = Profile.Builder() \
        .set_username(username) \
        .set_password(password) \
        .set_email(email) \
        .build()

    profile.save()
    login(profile)
    return redirect("/")


def loginUser(request):
    result = dict(request.POST)
    username = trim(result["username"])
    password = trim(result["password"])
    if len(username) == 0 or len(password) == 0:
        return render(request, "login.html", {"message": "Nu au fost completate toate campurile!"})
    profileExists = False
    profileUsername = Profile.objects.filter(username=username)
    profile = None
    if profileUsername:
        profilePassword = Profile.objects \
            .filter(username=username) \
            .filter(password=password)
        if profilePassword:
            profile = profilePassword[0]
    if profile:
        profileExists = True
    if profileExists:
        login(profile)
        return redirect("/")
    else:
        return render(request, "login.html", {"message": "Numele de utilizator sau parola nu sunt corecte!"})


def showProfile(request, username):
    global profile_logged_in
    context = {
        "profile": profile_logged_in,
        "numberOfProducts": getNumberOfProducts(),
    }
    return render(request, 'users/profiles.html', context)


def updatePersonalInfo(request):
    global profile_logged_in
    result = dict(request.POST)
    address, email, firstname, phone, surname = get_information_personal_data(result)
    set_information_personal_data(address, email, firstname, phone, surname)
    context = {
        "profile": profile_logged_in,
        "numberOfProducts": getNumberOfProducts(),
    }
    return render(request, 'users/profiles.html', context)


def set_information_personal_data(address, email, firstname, phone, surname):
    global profile_logged_in
    profile_logged_in.firstname = firstname
    profile_logged_in.surname = surname
    profile_logged_in.phone = phone
    profile_logged_in.email = email
    profile_logged_in.address = address
    profile_logged_in.save()


def get_information_personal_data(result):
    firstname = trim(result["firstname"])
    surname = trim(result["surname"])
    phone = trim(result["phone"])
    email = trim(result["email"])
    address = trim(result["address"])
    return address, email, firstname, phone, surname


def logoutUser(request):
    global profile_logged_in
    profile_logged_in = None
    logout()
    return redirect("/")


def login(user):
    global profile_logged_in
    profile_logged_in = user


def logout():
    global profile_logged_in
    profile_logged_in = None
    products.views.resetProductList()


def getProfileLoggedIn():
    global profile_logged_in
    return profile_logged_in


def getNumberOfProducts():
    numberOfProducts = products.views.getNumberOfProducts()
    return numberOfProducts


def trim(string):
    result = str(string).replace("['", "").replace("']", "")
    return result


def createBill(request, bill_number):
    bill = Bill.objects.get(bill_number=bill_number)
    address, deliveryCost, email, name, phone, productsString, timestamp, totalPrice = get_bill_data(bill)
    productsToShow = render_products_from_string(productsString)
    context = get_bill_context(address, deliveryCost, email, name, phone, productsToShow, timestamp, totalPrice)
    pdf = products.views.render_to_pdf('bill.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{bill}.pdf"'
    return response


def get_bill_context(address, deliveryCost, email, name, phone, productsToShow, timestamp, totalPrice):
    context = {
        'pagesize': 'A4',
        'name': name,
        'address': address,
        'phone': phone,
        'email': email,
        'products': productsToShow,
        'productsPrice': totalPrice,
        "deliveryCost": deliveryCost,
        'timestamp': timestamp,
    }
    return context


def get_bill_data(bill):
    name = bill.name
    address = bill.address
    phone = bill.phone
    email = bill.email
    timestamp = str(bill.created_at)[:10]
    totalPrice = bill.price
    deliveryCost = 10
    if totalPrice > 60:
        deliveryCost = 0
    productsString = bill.products
    return address, deliveryCost, email, name, phone, productsString, timestamp, totalPrice


def render_products_from_string(productsString):
    products = productsString.split(", ")
    productsList = []
    for product in products:
        productParts = product.split(" ")
        if len(productParts) < 3:
            break
        title = productParts[0].replace("-", " ")
        quantity = int(productParts[1])
        priceTotal = int(productParts[2])
        priceUnit = priceTotal / quantity
        newProduct = MyProduct(title, priceUnit)
        element = (newProduct, quantity, priceTotal)
        productsList.append(element)
    return productsList


class MyProduct:
    def __init__(self, title, price):
        self.title = title
        self.price = price
