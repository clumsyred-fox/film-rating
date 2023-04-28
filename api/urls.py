from django.urls import include, path


urlpatterns = [
    path('auth/signup/', SignUpAPI.as_view(), name='signup'),
    path('auth/token/', GetTokenAPI.as_view(), name='token'),
]
