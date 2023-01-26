from django.contrib.auth import get_user_model
from django.db.models import Avg
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


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    # rating = serializers.IntegerField(max_value=10, min_value=1)
    rating = serializers.SerializerMethodField()

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

    def get_rating(self, obj: Title):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title

    def to_representation(self, instance):
        serializer = TitleSerializer(instance)
        return serializer.data


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)


class UserCreateSerializer(UserBaseSerializer):
    email = serializers.EmailField()


class UserTokenSerializer(UserBaseSerializer):
    confirmation_code = serializers.CharField(max_length=25)


class UsersSerializer(serializers.ModelSerializer):
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


class UserMeSerializer(UsersSerializer):
    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)


class UserAdminSerializer(UsersSerializer):
    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
            password=User.objects.make_random_password()
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
