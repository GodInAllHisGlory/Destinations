from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Session, Destination
import random
import string

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
    response = redirect("/destinations")

    # If the length of the QuerySet if 0 then it passes over otherwise it throws an error
    # Uses the filter method because the get method throws an error if it cannot find the object
    if len(User.objects.filter(email = email)):
        return redirect("/user/new")

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

    session = make_session(user)
    response.set_cookie("session_token", session.token)

    return response

def sign_in(req: HttpRequest):
    return render(req, "core/sign_in.html")

# Signs in the user and makes a session
def sessions(req: HttpRequest):
    query = req.POST
    email = query.get("email","").lower()
    password = query.get("password", "")
    response = redirect("/destinations")
    message404 = "Check that you have the right email and password"

    try :
        user = User.objects.get(email = email)
    except Exception:
        raise Http404(message404)
    
    if not check_password(password, user.password_hash):
        raise Http404(message404)

    session = make_session(user)
    response.set_cookie("session_token", session.token)
    return response

def make_session(user: User):
    full_string_set = string.ascii_letters + string.digits
    token = "".join(random.choice(full_string_set) for _ in range(128))
    
    session = Session(
        user = user,
        token = token
    )

    session.save()
    return session

def destroy_session(req: HttpRequest):
    response = redirect("/")
    token = req.COOKIES["session_token"]

    Session.objects.get(token = token).delete()
    response.delete_cookie("session_token")
    return response
        
def destinations(req: HttpRequest):
    destinations = Destination.objects.filter(user = req.user)

    return render(req, "core/destinations.html", {"destinations": destinations})

def new_destination(req: HttpRequest):
    return render(req, "core/new_destination.html")

def create_destination(req: HttpRequest):
    query = req.POST
    name, review, rating, share = extract_destination(query)

    try:
        rating = int(rating)
    except Exception:
        return redirect("/destinations/new")
    
    if check_destinations(name, review, rating, share):
        return redirect("/destinations/new")

    destination = Destination(
        name = name,
        review = review,
        rating = rating,
        share_publicly = share == "True",
        user = req.user
    )

    destination.save()

    return redirect("/destinations")

def destination_card(req: HttpRequest, id: int):
    destination = Destination.objects.get(id = id)

    if destination.user != req.user and not destination.share_publicly:
        return redirect("/destinations")

    return render(req,"core/destination.html", {"destination": destination})

def destination_edit(req: HttpRequest, id: int):
    destination = Destination.objects.get(id = id)

    if destination.user != req.user:
        return redirect("/destinations")

    query = req.POST
    name, review, rating, share = extract_destination(query)

    try:
        rating = int(rating)
    except Exception:
        return redirect("/destinations")
    if check_destinations(name, review, rating, share):
        return redirect("/destinations")
    
    destination.name = name
    destination.review = review
    destination.rating = rating
    destination.share_publicly = share
    destination.save()

    return redirect("/destinations")

def extract_destination(query):
    name = query.get("name","")
    review = query.get("review","")
    rating = query.get("rating","")
    share = query.get("share","")
    return name, review, rating, share

def check_destinations(name, review, rating, share):
    if name == "" or review == "" or rating < 1 or rating > 5 or share == "":
        return True
    return False

def delete_destination(req: HttpRequest, id: int):
    destination = Destination.objects.get(id = id)

    if destination.user == req.user:
        destination.delete()

    return redirect("destinations")
