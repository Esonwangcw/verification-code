from django.urls import path
from .views import (
    api_signup,
    api_verify_email,
    api_password_reset,
    api_password_reset_confirm
)

urlpatterns = [
    path('api/signup/', api_signup),
    path('api/verify_email/', api_verify_email),
    path('api/password_reset/', api_password_reset),
    path('api/password_reset_confirm/', api_password_reset_confirm),
    # other URL patterns here...
]
