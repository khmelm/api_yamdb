from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import CustomPermission
from reviews.models import Title, Category, Genre

from api.serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    UserCreateSerializer,
    UserTokenSerializer,
    ReviewSerializer
)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('titles__category')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('titles__genre')


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


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.review

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)