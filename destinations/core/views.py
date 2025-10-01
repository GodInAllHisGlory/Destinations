from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def index(req: HttpRequest):
    return render(req, "core/index.html")