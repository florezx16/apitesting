from rest_framework import serializers
from .models import Book
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator , MinValueValidator, MaxValueValidator

class BookSerializer(serializers.ModelSerializer):
    
    isbn = serializers.CharField(
        validators = [
            MinLengthValidator(10),
            MaxLengthValidator(15),
            RegexValidator(regex='^[0-9 -]+$',message='This field contains invalid characters.')
        ]
    )

    title = serializers.CharField(
        validators = [
            MinLengthValidator(5),
            MaxLengthValidator(50),
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='This field contains invalid characters.')
        ]
    )
    
    author = serializers.CharField(
        validators = [
            MinLengthValidator(5),
            MaxLengthValidator(50),
            RegexValidator(regex='^[a-zA-Z ]+$',message='This field contains invalid characters.')
        ]
    )
    
    publish_date = serializers.DateField()
    
    pages_number = serializers.IntegerField(
        validators = [
            MinValueValidator(10),
            MaxValueValidator(10000)
        ]
    )
    
    genre = serializers.ChoiceField(
        choices = Book.BookGenres,
        allow_blank = False,
        help_text = Book.BookGenres.choices,
        error_messages = {
            "invalid_choice":"Ensure this value is a valid choice."
        }
    )
    
    status = serializers.IntegerField(
        required = False,
        default = 1,
        help_text = Book.BookStatus.choices,
    )
    
    def validate_status(self, value):
        if value not in [0,1]:
            raise serializers.ValidationError("This field contains invalid characters.")
        return value
    
    def validate_isbn(self,value):
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError('This ISBN number already exist in our DB.')
        return value
    
    class Meta():
        model = Book
        fields = ['isbn','title','author','publish_date','pages_number','genre','status']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = instance.get_genre_display()
        representation['status'] = instance.get_status_display()
        return representation
        
class BookQuerySerializer(serializers.Serializer):

    isbn = serializers.CharField(
        allow_blank = True,
        required = False,
        validators = [
            MaxLengthValidator(50),
            RegexValidator(regex='^[0-9 -]+$',message='This field contains invalid characters.')
        ]
    )

    title = serializers.CharField(
        allow_blank = True,
        required = False,
        validators = [
            MaxLengthValidator(50),
            RegexValidator(regex='^[a-zA-Z -]+$',message='This field contains invalid characters.')
        ]
    )
    
    author = serializers.CharField(
        allow_blank = True,
        required = False,
        validators = [
            MaxLengthValidator(50),
            RegexValidator(regex='^[a-zA-Z ]+$',message='This field contains invalid characters.')
        ]
    )
    
    genre = serializers.ChoiceField(
        choices = Book.BookGenres,
        allow_blank = True,
        required = False,
        error_messages = {
            "invalid_choice":"This choice is invalid."
        }
    )

    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        #representation['genre'] = instance.get_genre_display()
        #representation['status'] = instance.get_status_display()
        return representation