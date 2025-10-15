from django.shortcuts import redirect
from django.http import HttpRequest
from .models import Session, Destination

def authentication_middleware(next):
    #Gets the "session_token" cookie and if there isn't one it the token is replaced by an empty string
    def middleware(req: HttpRequest):
        session_uris = ["/destinations", "/destinations/new"]
        uri = req.get_full_path()
        token = req.COOKIES.get("session_token", "")

        #Since empty strings are falsy it will skip over getting the user if there is no token
        if token:
            session = Session.objects.get(token = token)
            user = session.user
            req.user = user

        #If you don't have a session then it checks to make sure you can actually go where you requested
        elif uri in session_uris or not find_digit(uri):
            return redirect("/session/new")
        
        res = next(req)
        return res
    
    return middleware

def find_digit(uri):
    for char in uri:
        if char.isdigit():
            return True
    return False