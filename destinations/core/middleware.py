from django.shortcuts import redirect
from django.http import HttpRequest
from .models import Session, Destination

def authentication_middleware(next):
    #Gets the "session_token" cookie and if there isn't one it the token is replaced by an empty string
    def middleware(req: HttpRequest):
        session_uris = ["/destinations", "/destinations/new"]
        uri = req.get_full_path()
        token = req.COOKIES.get("session_token", "")
        id = get_id(uri)
        if id:
            id = int(id)

        #Since empty strings are falsy it will skip over getting the user if there is no token
        if token:
            session = Session.objects.get(token = token)
            user = session.user
            req.user = user

            if id:
                destination = Destination.objects.get(id = id)
                if destination.user != user:
                    return redirect("/destinations")

        #If you don't have a session then it checks to make sure you can actually go where you requested
        elif uri in session_uris or id != None:
            return redirect("/session/new")
        
        res = next(req)
        return res
    
    return middleware

def get_id(uri):
    id = ""
    for char in uri:
        if char.isdigit():
            id = id + char
    if len(id) != 0:
        return id
    
    return None