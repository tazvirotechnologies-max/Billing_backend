from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    authentication_classes = []  # allow login without auth
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user or not user.is_active:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)  # SESSION LOGIN
        return Response({
            "user": UserSerializer(user).data
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class StaffView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin only
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        # Admin only: create cashier
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'CASHIER')

        if not username or not password:
            return Response({"detail": "username & password required"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )
        return Response(UserSerializer(user).data, status=201)