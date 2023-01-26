from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    AdminOnlyPermission,
    AdminOrReadOnlyPermission,
    AuthorAdminModeratorPermission,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    UserAdminSerializer,
    UserCreateSerializer,
    UserMeSerializer,
    UserTokenSerializer,
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnlyPermission,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        else:
            return TitleCreateSerializer


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
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
            try:
                User.objects.create_user(
                    **serializer.validated_data,
                    password=code,
                )
            except ValidationError as error:
                return Response(error, status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(code)
            user.save()
        self.send_confirmation_code(code, serializer.validated_data['email'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def send_confirmation_code(code, mail):
        send_mail(
            'Ваш код подтверждения для входа на сайт YaMDb',
            'Здравствуйте!\n\nВаш код подтверждения для входа на сайт YaMDb: '
            f'{code}\n\nС наилучшими пожеланиями,\nКоманда YaMDb.',
            'noreply@yamdb.com',
            [mail],
            fail_silently=False,
        )


class UsersMeView(APIView):
    def get(self, request):
        return Response(UserMeSerializer(request.user).data)

    def patch(self, request):
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (AdminOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorPermission, )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(review=review, author=self.request.user)
