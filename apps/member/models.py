from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .manager import UserManager


class Member(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = (
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    )
    
    email= models.EmailField('Your Email', unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default= False)
    
    # otp = models.CharField(max_length=6, blank=True, null=True)
    # otp_exp = models.DateTimeField(blank=True, null=True) 
    # otp_verified = models.BooleanField(default=False)

    objects= UserManager()
    USERNAME_FIELD= 'email'
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField()
    CHOICE_GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=CHOICE_GENDER, default='other')
    address = models.TextField()
    phone = models.CharField(max_length=255)

    def __str__(self):
          return self.member.email
      
class Book(models.Model):
    # member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    category = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class BorrowRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.email} borrowed {self.book.title}"

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name