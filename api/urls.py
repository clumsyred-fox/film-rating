from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SignUpView, AuthTokenView

router = DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', AuthTokenView.as_view(), name='token'),
]
