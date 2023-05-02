from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import CategoryViewSet, GenreViewSet, TitleGETViewSet

router_v1 = DefaultRouter()
router_v1.register('category', CategoryViewSet, basename='category')
router_v1.register('genre', GenreViewSet, basename='genre')
router_v1.register('titles', TitleGETViewSet, basename='titles')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', TitleGETViewSet, basename='titles'
)
v1_patterns = [
    path('', include(router_v1.urls)),
]
urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('auth/signup/', SignUpAPI.as_view(), name='signup'),
    path('auth/token/', GetTokenAPI.as_view(), name='token'),
]
