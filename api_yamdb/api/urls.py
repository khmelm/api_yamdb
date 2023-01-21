from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    UserCreateView,
    UserTokenView,
    UsersMeView,
    UsersViewSet,
)

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='title')
router.register('users', UsersViewSet, basename='users')

auth_urls = [
    path('signup/', UserCreateView.as_view()),
    path('token/', UserTokenView.as_view()),
]

urlpatterns = [
    path('v1/users/me/', UsersMeView.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
