from django.shortcuts import get_object_or_404
from apps.member.models import Book
from .serializers import AddBookSerializer, EditBookSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.member.permissions import IsLibrarian, IsLibrarianOrAdmin
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from apps.member.models import Member

# Create your views here.

class AddBookView(generics.CreateAPIView):
    permission_classes = [IsLibrarian]
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        author = request.data.get('author')
        
        book = Book.objects.filter(title=title, author=author).first()
        if book:
            book.quantity += 1
            book.save()
            serializer = self.get_serializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsLibrarian])
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = EditBookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = AddBookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsLibrarian])
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AllProfilesView(APIView):
   
    permission_classes = [IsAdminUser,IsLibrarian]

    
    def get(self, request):
       
        users = Member.objects.all()
        user_data = []
        for user in users:
            try:
                profile_data = {
                    "age": user.profile.age,
                    "gender": user.profile.gender,
                    "address": user.profile.address,
                    "phone": user.profile.phone,
                }
            except:
                # Handle case where profile doesn't exist
                profile_data = {
                    "age": 0,
                    "gender": "other",
                    "address": "",
                    "phone": "",
                }
            
            user_data.append({
                "user_id": user.id,
                "user_email": user.email,
                "profile": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "bio": user.bio,
                    "is_active": user.is_active,
                    **profile_data
                }
            })
        return Response({
            "success": True,
            "message": "All profiles data",
            "status code": status.HTTP_200_OK,
            "profiles": user_data
        }, status=status.HTTP_200_OK)
