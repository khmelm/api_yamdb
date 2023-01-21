from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review


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