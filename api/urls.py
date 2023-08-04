from django.urls import path
from .views.authenticate.authenticate import register, login, entrySuccessful
from .views.whatsapp.whatsapp import userCredentials


urlpatterns = [
    path("", login , name="login"),
    path("register", register , name="register"),
    path("login", login , name="login"),
    path("getUserData", entrySuccessful, name="entrySuccessful"),
    path("whatsapp", userCredentials, name='whatsapp')
]