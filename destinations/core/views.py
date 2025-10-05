from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password, check_password

def index(req: HttpRequest):
    return render(req, "core/index.html")

def create_account(req: HttpRequest):
    return render(req, "core/create_account.html")

def user(req: HttpRequest):
    query = req.POST
    name = query["name"]
    email = query["email"]
    password_unhashed = query["password"]
    if len(name) == 0:
        return
    print(name, email, password_unhashed)
    return redirect("/")