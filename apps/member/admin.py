from django.contrib import admin
from .models import Member, Profile, Book, BorrowRecord, Author

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['member', 'age', 'gender', 'phone']
    list_filter = ['gender', 'age']
    search_fields = ['member__email', 'member__first_name', 'member__last_name', 'phone']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'quantity', 'available', 'category', 'published_date']
    list_filter = ['available', 'category', 'published_date']
    search_fields = ['title', 'author', 'category']
    ordering = ['title']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['member', 'book', 'borrow_date', 'return_date']
    list_filter = ['borrow_date', 'return_date']
    search_fields = ['member__email', 'book__title']
    date_hierarchy = 'borrow_date'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'bio']
