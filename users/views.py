from django.http.response import HttpResponse
from django.shortcuts import redirect, render

import products.views
from users.models import Bill, Profile

profile_logged_in = None


def profiles(request):
    return render(request, 'users/profiles.html')


def createUser(request):  # creates a new user
    result = dict(request.POST)
    username = trim(result["username"])
    email = trim(result["email"])
    password = trim(result["password"])
    existsUsername = len(Profile.objects.filter(username=username)) > 0
    if existsUsername:
        return render(request, "login.html", {"message": "Exista deja acest utilizator! Incercati din nou."})
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
    return redirect("/")  # redirect to home page


def loginUser(request):  # login the user
    result = dict(request.POST)
    username = trim(result["username"])
    password = trim(result["password"])
    if len(username) == 0 or len(password) == 0:
        return render(request, "login.html", {"message": "Nu au fost completate toate campurile!"})

    usernameExists = Profile.objects.filter(username=username)  # first check that username exists
    profile = None
    if usernameExists:
        passwordExists = Profile.objects \
            .filter(username=username) \
            .filter(password=password)  # second verify the username has that password
        if passwordExists:
            profile = passwordExists[0]
    if profile:  # if the profile exists
        login(profile)
        return redirect("/")
    else:
        return render(request, "login.html", {"message": "Numele de utilizator sau parola nu sunt corecte!"})


def showProfile(request, username):  # shows the informations for the current user logged in
    context = {
        "profile": getProfileLoggedIn(),
        "numberOfProducts": getNumberOfProducts(),
    }
    return render(request, 'users/profiles.html', context)


def updatePersonalInfo(request):  # modify the personal data
    result = dict(request.POST)
    address, email, firstname, phone, surname = get_information_personal_data(result)
    set_information_personal_data(address, email, firstname, phone, surname)
    context = {
        "profile": getProfileLoggedIn(),
        "numberOfProducts": getNumberOfProducts(),
    }
    return render(request, 'users/profiles.html', context)


def set_information_personal_data(address, email, firstname, phone, surname):  # save the modifications on personal data
    global profile_logged_in
    profile_logged_in.firstname = firstname
    profile_logged_in.surname = surname
    profile_logged_in.phone = phone
    profile_logged_in.email = email
    profile_logged_in.address = address
    profile_logged_in.save()


def get_information_personal_data(result):  # gets more variables from one
    firstname = trim(result["firstname"])
    surname = trim(result["surname"])
    phone = trim(result["phone"])
    email = trim(result["email"])
    address = trim(result["address"])
    return address, email, firstname, phone, surname


def logoutUser(request):  # logout the user
    global profile_logged_in
    profile_logged_in = None
    logout()
    return redirect("/")


def login(user):  # set de logged in user
    global profile_logged_in
    profile_logged_in = user


def logout():  # log out the user and reset the product list
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


def createBill(request, bill_number):  # creates the pdf format bill
    bill = Bill.objects.get(bill_number=bill_number)
    info, productsString = get_bill_data(bill)
    productsToShow = render_products_from_string(productsString)
    context = get_bill_context(info, productsToShow)
    pdf = products.views.render_to_pdf('bill.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{bill}.pdf"'
    return response


def get_bill_context(info, productsToShow):  # prepare context for rendering into html page
    context = {
        'pagesize': 'A4',
        'name': info[3],
        'address': info[0],
        'phone': info[4],
        'email': info[2],
        'products': productsToShow,
        'productsPrice': info[6],
        "deliveryCost": info[1],
        'timestamp': info[5],
    }
    return context


def get_bill_data(bill):  # return information about bill
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
    return [address, deliveryCost, email, name, phone, timestamp, totalPrice], productsString


def render_products_from_string(productsString):  # convert string into product list
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


class MyProduct:  # class created for easily rendering products from a string
    def __init__(self, title, price):
        self.title = title
        self.price = price
