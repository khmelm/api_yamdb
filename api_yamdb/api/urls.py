from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    UserCreateView,
    UserTokenView,
)

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='title')

auth_urls = [
    path('signup/', UserCreateView.as_view()),
    path('token/', UserTokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
