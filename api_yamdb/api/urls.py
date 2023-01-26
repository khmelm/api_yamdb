from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserCreateView,
    UsersViewSet,
    UserTokenView,
)

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='title')
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='title'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='title'
)

auth_urls = [
    path('signup/', UserCreateView.as_view()),
    path('token/', UserTokenView.as_view()),
]

urlpatterns = [
    # path('v1/users/me/', UsersMeView.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
