from django.urls import path
from .views import home, signup, verify_email, signin, signout, password_reset, verify_password_reset_email

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('verify_email/', verify_email, name='verify_email'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('password_reset/', password_reset, name='password_reset'),
    path('verify_password_reset_email/', verify_password_reset_email, name='verify_password_reset_email'),
    # other URL patterns here...
]
