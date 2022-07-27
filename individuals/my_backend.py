from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend





class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print('user_model')
        print(UserModel)
        UserModel._meta.get_fields()
        try:
            user = UserModel.objects.get(email=email)

            #print(lol)
            #print(email)
            print("user object")
            print(user)
        except UserModel.DoesNotExist:
        
            print("not exit")
            return None
        else:
            print('triggered else')
            if user.check_password(password):
                print('found')
                print(user)
                return user
        print("none ya basha")
        return None

