from django.urls import path
from . import views



urlpatterns = [
    path("old", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login_old", views.login_request, name="login_old"),
    path("logout_old", views.logout_request, name= "logout_old"),
    path("sign_up", views.sign_up_req, name="sign_up"),
    path("papers", views.country_documents, name="country documents"),
    path("create_wallet", views.create_wallet, name="create_wallet"),
    path("", views.main_page, name="main_page"),

    path("login", views.log_me_in, name="login"),

    path("logout", views.log_me_out, name="logout"),
    
    path("wallet", views.retrive_wallet, name="retrive_wallet"),
    
    path("vbank", views.list_vbank, name="list_vbank"),
    
    path("make", views.make_deposit, name="make_deposit"),
    #path("contact/<pk>/", views.contact_detail, name="contact_detail"),
    
    
]