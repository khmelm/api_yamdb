from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class UserBaseSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )


class UserCreateSerializer(UserBaseSerializer):
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                {'username': 'username не может быть `me`!'}
            )
        return value

    def validate(self, attrs):
        if User.objects.filter(
            username=attrs.get('username'),
            email=attrs.get('email'),
        ):
            return attrs
        if User.objects.filter(username=attrs.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=attrs.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return attrs


class UserTokenSerializer(UserBaseSerializer):
    confirmation_code = serializers.CharField(max_length=25)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('title',)
        model = Review

    def validate(self, attrs):
        if self.context.get('request').method != 'POST':
            return attrs
        user = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=user, title__pk=title_id).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв!',
            )
        if not 1 < attrs.get('score') < 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment
