from django.urls import path
from . import views



urlpatterns = [
    path("old", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("sign_up", views.sign_up_req, name="sign_up"),
    path("papers", views.country_documents, name="country documents"),
    path("create_wallet", views.create_wallet, name="create Wallet"),
    path("", views.main_page, name="main_page"),

    path("contact/<pk>/", views.contact_detail, name="contact_detail"),
    
    
]