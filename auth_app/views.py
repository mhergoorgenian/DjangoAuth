from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status

class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request,id=None):
        try:
            if request.user.is_superuser:  
                if id is None:
                    users = UserProfile.objects.all()
                else:
                    users = UserProfile.objects.filter(id=id)
                serializer = UserProfileSerializer(users, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
               
            

            user = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class UserLoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        
        print("Username:", username)
        print("Password:", password)
        
        user = authenticate(username=username, password=password)
        
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({ "error" : {"message"  : "Invalid username or password"} },status=400)
        

class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        
        print("Username:", username)
        print("Password:", password)
        try:
            user=User.objects.filter(username=username)
            if user:
                Response({"error": {"message": "User already exists"}}, status=400)
            user = User(username=username)
            user.set_password(password)
            user.save()
            
            
            profile = UserProfile.objects.create(user=user)
            data = UserProfileSerializer(profile).data
            return Response({"data": data}, status=201)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


