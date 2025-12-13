from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Wishlist
from .serializers import WishlistSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wishlist_list(request):
    qs = Wishlist.objects.filter(user=request.user)
    return Response(WishlistSerializer(qs, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wishlist_add(request):
    serializer = WishlistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def wishlist_remove(request, tmdb_id):
    Wishlist.objects.filter(
        user=request.user,
        tmdb_id=tmdb_id
    ).delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
