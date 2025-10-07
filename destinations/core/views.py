from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# TODO When making a user have it redirect to destination not '/'

def index(req: HttpRequest):
    return render(req, "core/index.html")

def create_account(req: HttpRequest):
    return render(req, "core/create_account.html")

# Makes a user from the create account form
# If any field (name, email, password) doesn't meet the requirements it just reloads the page via redirect right now
def user(req: HttpRequest):
    query = req.POST
    name = query.get("name","")
    email = query.get("email", "").lower()
    password_unhashed = query["password"]

    if len(name) == 0:
        return redirect("/user/new")
    if '@' not in email:
        return redirect("/user/new")
    if not any(char.isdigit() for char in password_unhashed) and not len(password_unhashed) >= 8:
        return redirect("/user/new")
    password = make_password(password_unhashed)
    
    user = User(
        name = name,
        email = email,
        password_hash = password
    )
    user.save()
    return redirect("/")

def sign_in(req: HttpRequest):
    return render(req, "core/sign_in.html")

# Signs in the user and makes a session
def sessions(req: HttpRequest):
    query = req.POST
    email = query.get("email","").lower()
    password = query.get("password", "")

    try :
        user = User.objects.get(email = email)
    except Exception:
        raise Http404("Check that you have the proper email and password")
    
    if not check_password(password, user.password_hash):
        raise Http404("Check that you have the proper email and password")
    
    # TODO Make a seesion token with the users password or email
    # Make a seesion object

    return redirect("/session/new")
        
