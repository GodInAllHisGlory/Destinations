from django.shortcuts import redirect
from django.http import HttpRequest
from .models import Session, User

def authentication_middleware(next):
    #Gets the "session_token" cookie and if there isn't one it the token is replaced by an empty string
    def middleware(req: HttpRequest):
        session_uris = ["/destinations", "/destinations/new"]
        uri = req.get_full_path()
        token = req.COOKIES.get("session_token", "")
        req.signed_in = False

        #Since empty strings are falsy it will skip over getting the user if there is no token
        if token:
            session = Session.objects.get(token=token)
            req.user = session.user
            req.signed_in = True

        #If you don't have a session then it checks to make sure you can actually go where you requested
        elif uri in session_uris:
            return redirect("/session/new")
        
        res = next(req)
        return res
    
    return middleware