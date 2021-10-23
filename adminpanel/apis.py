from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        try:
            payload = {
                "name": request.data['name'],
                "email": request.data['email'],
                "password": request.data['password'],
                "is_staff": request.data['is_staff']
            }
            print(payload)
            register_user_serializer = UserSerializer(data=payload)
            if register_user_serializer.is_valid():
                register_user_serializer.save()
                return Response(register_user_serializer.data, status=status.HTTP_201_CREATED)
            return Response(register_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        try:
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(email=email).first()
            token=get_tokens_for_user(user=user)
        
            if user is None:
                raise AuthenticationFailed('User not found')
            if not user.check_password(password):
                raise AuthenticationFailed('Wrong Password')
            return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        except KeyError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_user(request):
    if request.method == 'POST':
        try:
            user_id = request.data['id']
            user = User.objects.filter(pk=user_id)
            print(user)
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_200_OK)
            return Response({'user': UserSerializer(user, many=True).data}, status=status.HTTP_200_OK)
        except KeyError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # return Response(status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }