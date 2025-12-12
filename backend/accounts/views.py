# backend/accounts/views.py
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    payload: { "username": "...", "password": "...", "password2": "...", "email": "..."}
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/accounts/me/  -> return current user
    PATCH /api/accounts/me/ -> update profile (first_name, last_name, email)
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
