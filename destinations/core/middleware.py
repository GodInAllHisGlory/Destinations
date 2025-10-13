from django.http import HttpRequest

def authentication_middleware(next):

    def middleware(req: HttpRequest):
        print("Middleware looking fine")
        res = next(req)
        return res
    
    return middleware