from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg

from api.v1.filters import TitleFilter
from api.v1.mixins import ListCreateDestroyViewSet
from api.v1.permissions import (
    AdminOnlyPermission,
    AdminOrReadOnlyPermission,
    AuthorAdminModeratorPermission,
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserTokenSerializer,
)
from api.v1.utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnlyPermission,)
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleCreateSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )
        if not check_password(
            serializer.validated_data['confirmation_code'],
            user.password,
        ):
            return Response(
                {
                    'error': 'Неверный confirmation_code!',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                'access': str(RefreshToken.for_user(user).access_token),
            },
        )


class UserCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        ).first()
        code = User.objects.make_random_password()
        if not user:
            User.objects.create_user(
                **serializer.validated_data,
                password=code,
            )
        else:
            user.set_password(code)
            user.save()
        send_confirmation_code(code, serializer.validated_data['email'])
        return Response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def users_me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        data = request.data.copy()
        if 'role' in data:
            data.pop('role')
        serializer = UserSerializer(
            request.user,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(password=User.objects.make_random_password())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def check_correct_title_id(self, review):
        title_id_url = self.kwargs.get('title_id')
        title_id_database = review.title.pk
        if int(title_id_url) != title_id_database:
            raise ValidationError('Некорректный id произведения')

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        self.check_correct_title_id(review)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        self.check_correct_title_id(review)
        serializer.save(review=review, author=self.request.user)
