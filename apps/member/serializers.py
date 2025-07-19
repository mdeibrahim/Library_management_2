from rest_framework import serializers
from .models import Member, Profile, Book

class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'quantity', 'published_date', 'category', 'available']

class ProfileNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'address', 'phone']


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileNestedSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'is_active', 'date_joined', 'profile']
        read_only_fields = ['id', 'email', 'date_joined']
        
        
class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'quantity', 'published_date', 'category', 'available']
        read_only_fields = ['available']


class ReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'quantity', 'published_date', 'category', 'available']
        read_only_fields = ['available']
