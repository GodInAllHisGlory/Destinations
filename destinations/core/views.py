from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# TODO When makeing a user have it redirect to destination not '/'

def index(req: HttpRequest):
    return render(req, "core/index.html")

def create_account(req: HttpRequest):
    return render(req, "core/create_account.html")

# Makes a user from the create account form
# If any field (name, email, password) dosen't meet the requirments it just reloads the page via redirect right now
def user(req: HttpRequest):
    query = req.POST
    name = query["name"]
    email = query["email"]
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