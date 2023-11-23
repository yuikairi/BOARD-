from django.contrib.auth.backends import ModelBackend

class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        pass
