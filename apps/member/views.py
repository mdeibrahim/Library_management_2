
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.member.models import Member, Book, BorrowRecord
from rest_framework.permissions import IsAuthenticated
from apps.member.serializers import BorrowBookSerializer, ReturnBookSerializer
from django.shortcuts import get_object_or_404
from datetime import date


class BorrowBookView(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({
                "success": False,
                "message": "book_id is required",
                "status code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = get_object_or_404(Book, id=book_id)
            
            # Check if book is available
            if not book.available or book.quantity <= 0:
                return Response({
                    "success": False,
                    "message": "Book is not available for borrowing",
                    "status code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user already borrowed this book
            existing_borrow = BorrowRecord.objects.filter(
                member=request.user,
                book=book,
                return_date__isnull=True
            ).first()
            
            if existing_borrow:
                return Response({
                    "success": False,
                    "message": "You have already borrowed this book",
                    "status code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create borrow record
            BorrowRecord.objects.create(
                member=request.user,
                book=book
            )
            
            # Update book quantity
            book.quantity -= 1
            if book.quantity == 0:
                book.available = False
            book.save()
            
            return Response({
                "success": True,
                "message": "Book borrowed successfully",
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "remaining_quantity": book.quantity
                },
                "status code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Error borrowing book: {str(e)}",
                "status code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReturnBookView(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({
                "success": False,
                "message": "book_id is required",
                "status code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = get_object_or_404(Book, id=book_id)
            
            # Find the borrow record
            borrow_record = BorrowRecord.objects.filter(
                member=request.user,
                book=book,
                return_date__isnull=True
            ).first()
            
            if not borrow_record:
                return Response({
                    "success": False,
                    "message": "You have not borrowed this book",
                    "status code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update borrow record
            borrow_record.return_date = date.today()
            borrow_record.save()
            
            # Update book quantity
            book.quantity += 1
            if not book.available:
                book.available = True
            book.save()
            
            return Response({
                "success": True,
                "message": "Book returned successfully",
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "remaining_quantity": book.quantity
                },
                "status code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Error returning book: {str(e)}",
                "status code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        user = Member.objects.filter(email=request.user.email).first()

        return Response({
            "success": True,
            "message": "Profile data",
            "status code": status.HTTP_200_OK,
            "user_id": user.id,
            "user_email": user.email,
            "profile": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "age": user.profile.age,
                "gender": user.profile.gender,
                "address": user.profile.address,
                "phone": user.profile.phone,
                "is_active": user.is_active
            },
            
        }, status=status.HTTP_200_OK)
        
        


