from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def index(req: HttpRequest):
    return render(req, "core/index.html")

def create_account(req: HttpRequest):
    return render(req, "core/create_account.html")