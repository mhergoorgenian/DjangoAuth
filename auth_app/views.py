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


class UserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request:Request,id=None):
        try:   
            if id:
                user_profile = UserProfile.objects.get(id=id)
                serializer = UserProfileSerializer(user_profile)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UsersView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request:Request):
        try:   
            username=request.query_params.get('username',None)
            limit = request.query_params.get('limit', 5)  
            offset = request.query_params.get('offset', 0)
            
            if username:
                total = UserProfile.objects.filter(user__username__startswith=username).count()
                users = UserProfile.objects.filter(user__username__startswith=username)[int(offset): int(limit)]
            else:
                total = UserProfile.objects.count()
                users = UserProfile.objects.all()[offset : limit]
                
            serializer = UserProfileSerializer(users, many=True)

            return Response(
                {"data": serializer.data, "total-count": total},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MeView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request:Request):
        try: 
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
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
        

        

class RegisterView(APIView):
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


