from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = '__all__'

class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='name', queryset=Genre.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title


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
    # title = serializers.SlugRelatedField(
    #     queryset=Title.objects.all(),
    #     slug_field='name'
    # )

    class Meta:
        fields = '__all__'
        read_only_fields = ('title',)
        model = Review

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(), fields=('author', 'title')
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment
