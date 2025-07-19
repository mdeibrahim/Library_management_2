from rest_framework import serializers
from apps.member.models import Book

class AddBookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(help_text="Title of the book")
    author = serializers.CharField(help_text="Author of the book")
    published_date = serializers.DateField(help_text="Publication date (YYYY-MM-DD)")
    category = serializers.CharField(help_text="Book category/genre")
    quantity = serializers.IntegerField(min_value=1, help_text="Number of copies available")
    available = serializers.BooleanField(default=True, help_text="Whether the book is available for borrowing")
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'category', 'available', 'quantity']

class EditBookSerializer(serializers.ModelSerializer):
    published_date = serializers.DateField(help_text="Publication date (YYYY-MM-DD)")
    category = serializers.CharField(help_text="Book category/genre")
    quantity = serializers.IntegerField(min_value=0, help_text="Number of copies available")
    available = serializers.BooleanField(help_text="Whether the book is available for borrowing")
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'category', 'available', 'quantity']
        read_only_fields = ['title', 'author']
