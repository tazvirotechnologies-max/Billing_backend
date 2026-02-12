from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import LoginSerializer, UserSerializer
from .authentication import CsrfExemptSessionAuthentication


# =========================
# LOGIN
# =========================
class LoginView(APIView):
    authentication_classes = []   # no auth required
    permission_classes = []       # no permission required

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

        login(request, user)  # ✅ SESSION LOGIN
        return Response({
            "user": UserSerializer(user).data
        })


# =========================
# CURRENT USER (ME)
# =========================
class MeView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# =========================
# LOGOUT
# =========================
class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"})


# =========================
# STAFF MANAGEMENT (ADMIN)
# =========================
class StaffView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    # 🔹 List users
    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        return Response(
            UserSerializer(users, many=True).data
        )

    # 🔹 Create user
    def post(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'CASHIER')

        if not username or not password:
            return Response(
                {"detail": "username & password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role,
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


# =========================
# ACTIVATE / DEACTIVATE USER
# =========================
class StaffStatusView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.role != 'ADMIN':
            return Response(
                {"detail": "Only admin allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ❌ Prevent self deactivate
        if user.id == request.user.id:
            return Response(
                {"detail": "You cannot change your own status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        action = request.data.get("action")

        if action == "activate":
            user.is_active = True

        elif action == "deactivate":
            user.is_active = False

        else:
            return Response(
                {"detail": "Invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.save()

        return Response(
            UserSerializer(user).data
        )
