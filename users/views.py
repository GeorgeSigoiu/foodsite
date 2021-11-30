from django.shortcuts import redirect, render
import products.views

from users.models import Bill, Profile

# Create your views here.
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
        return render(request, "login.html", {"message": "Nu se poate crea contul: toate campurile trebuie completate!"})
    profile = Profile.create(email=email, username=username, password=password)
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
        profilePassword = Profile.objects.filter(
            username=username).filter(password=password)
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
        "profile": profile_logged_in
    }
    return render(request, 'users/profiles.html', context)


def updatePersonalInfo(request):
    global profile_logged_in
    result = dict(request.POST)
    print(result)
    firstname = trim(result["firstname"])
    surname = trim(result["surname"])
    phone = trim(result["phone"])
    email = trim(result["email"])
    address = trim(result["address"])
    profile_logged_in.firstname = firstname
    profile_logged_in.surname = surname
    profile_logged_in.phone = phone
    profile_logged_in.email = email
    profile_logged_in.address = address
    profile_logged_in.save()
    context = {
        "profile": profile_logged_in
    }
    return render(request, 'users/profiles.html', context)


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


def trim(string):
    result = str(string).replace("['", "").replace("']", "")
    return result
