from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponseBadRequest
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Session, Destination
import random
import string

# Gets the 5 most recent destinations and prints them out
def index(req: HttpRequest):
    destination_query = Destination.objects.all().order_by("-id")
    query_length = len(destination_query)
    destinations = []

    i = 0
    while len(destinations) < 5 and i != query_length:
        destination = destination_query[i]
        if destination.share_publicly:
            destinations.append(destination)
        i += 1
    return render(req, "core/index.html", {"destinations": destinations})

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
        return HttpResponseBadRequest("Email already in use")

    if len(name) == 0:
        return HttpResponseBadRequest("Must have a name")
    
    if '@' not in email:
        return HttpResponseBadRequest("Must be a real email")
    
    if not any(char.isdigit() for char in password_unhashed) and not len(password_unhashed) >= 8:
        return HttpResponseBadRequest("Password must be at least 8 characters and have 1 number in it")
    
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

# Makes a session object and returns it
def make_session(user: User):
    full_string_set = string.ascii_letters + string.digits
    token = "".join(random.choice(full_string_set) for _ in range(128))
    
    session = Session(
        user = user,
        token = token
    )

    session.save()
    return session

# Deletes the session cookie and session object associated with the cookie
def destroy_session(req: HttpRequest):
    response = redirect("/")
    token = req.COOKIES["session_token"]

    Session.objects.get(token = token).delete()
    response.delete_cookie("session_token")
    return response
        
def destinations(req: HttpRequest):
    destinations = Destination.objects.filter(user = req.user)

    return render(req, "core/destinations.html", {"destinations": destinations.order_by("-id")})

def new_destination(req: HttpRequest):
    return render(req, "core/new_destination.html")

# Takes in a post request and makes a destination if anything is wrong it reloads the page via redirect 
def create_destination(req: HttpRequest):
    query = req.POST
    name, review, rating, share = extract_destination(query)

    try:
        rating = int(rating)
    except Exception:
        return HttpResponseBadRequest("Rating MUST be a number")
    
    bad_response = check_destinations(name, review, rating, share)
    if bad_response != "":
        return bad_response

    destination = Destination(
        name = name,
        review = review,
        rating = rating,
        share_publicly = share == "True",
        user = req.user
    )

    destination.save()

    return redirect("/destinations")

# Renders a page that lets you edit your destination
def destination_card(req: HttpRequest, id: int):
    try:
        destination = Destination.objects.get(id = id)
    except Exception:
        raise Http404("You don't have the permissions to do this action")

    if destination.user != req.user:
        raise Http404("You don't have the permissions to do this action")

    return render(req,"core/destination.html", {"destination": destination})

# updates the destination
def destination_edit(req: HttpRequest, id: int):
    destination = Destination.objects.get(id = id)

    if destination.user != req.user:
        raise Http404("You don't have the permissions to do this action")

    query = req.POST
    name, review, rating, share = extract_destination(query)

    try:
        rating = int(rating)
    except Exception:
        return HttpResponseBadRequest("Rating MUST be a number")
    bad_response = check_destinations(name, review, rating, share)
    if bad_response != "":
        return bad_response
    
    destination.name = name
    destination.review = review
    destination.rating = rating
    destination.share_publicly = share
    destination.save()

    return redirect("/destinations")

# Endpoint that deletes a destination 
def delete_destination(req: HttpRequest, id: int):
    destination = Destination.objects.get(id = id)

    if destination.user != req.user:
        raise Http404("You don't have the permissions to do this action")

    destination.delete()
    return redirect("destinations")


# Gets everything from a destination object
def extract_destination(query):
    name = query.get("name","")
    review = query.get("review","")
    rating = query.get("rating","")
    share = query.get("share","")
    return name, review, rating, share

# Checks to make sure everything the user entered is good
def check_destinations(name, review, rating, share):
    if name == "":
        return HttpResponseBadRequest("Must have a name")
    elif review == "":
        return HttpResponseBadRequest("Must have a review")
    elif rating < 1 or rating > 5:
        return HttpResponseBadRequest("Rating must be valid")
    elif share == "":
        return HttpResponseBadRequest("I don't know how or why but you must submit yes or no to share")
    return ""
