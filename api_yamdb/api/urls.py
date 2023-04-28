from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleGETViewSet

router_v1 = DefaultRouter()
router_v1.register('category', CategoryViewSet, basename='category')
router_v1.register('genre', GenreViewSet, basename='genre')
router_v1.register('titles', TitleGETViewSet, basename='titles')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', TitleGETViewSet, basename='titles'
)
