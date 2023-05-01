from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import CategoryViewSet, GenreViewSet, TitleGETViewSet, SignUpView, AuthTokenView, ReviewViewSet, CommentViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleGETViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_v1.register(r'users', UserViewSet)
# router_v1.register('auth/signup/', SignUpView.as_view(), basename='signup')
# router_v1.register('auth/token/', AuthTokenView.as_view(), basename='token')

v1_patterns = [
    path('', include(router_v1.urls)),
]
urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', AuthTokenView.as_view(), name='token'),
    ]
