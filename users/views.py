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
    profile = Profile.create(email=email, username=username, password=password)
    profile.save()
    login(profile)
    return redirect("/")


def loginUser(request):
    result = dict(request.POST)
    username = trim(result["username"])
    password = trim(result["password"])
    profileExists = False
    profile = Profile.objects.filter(
        username=username).filter(password=password)[0]
    if profile:
        profileExists = True
    if profileExists:
        login(profile)
        return redirect("/")
    else:
        return render(request, "login.html", {"message": True})


def showProfile(request, username):
    global profile_logged_in
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
    print(type(user))


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
