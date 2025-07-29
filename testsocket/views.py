import uuid

from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from testsocket.models import CustomUser, ChatGroup
from testsocket.serializers import UserSerializer


# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        # اعتبارسنجی داده‌های ورودی
        try:
            name = data.get('name')
            username = data.get('username')
            password = data.get('password')


        except KeyError as e:
            return Response({'error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not name:
            return Response({'error': 'name is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'username is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'password is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # تبدیل is_company به بولین

        # ایجاد کاربر

        try:
            if CustomUser.objects.filter(username=username).exists():
                return Response({'error': 'Username already used'}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                name=name,
            )
            user_serializer = UserSerializer(user)
        except IntegrityError:
            return Response({'error': 'Username already used'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class StartChatView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_name = f"chat_{uuid.uuid4().hex[:8]}"

        chat_group = ChatGroup.objects.create(
            name=group_name,
            creator=request.user
        )

        current_time = timezone.now().strftime("%H:%M:%S")

        return Response({
            'group_name': group_name,
            'websocket_url': f'ws://{request.get_host()}/ws/chat/{group_name}/',
            'message': f'سلام {request.user.username} الان ساعت {current_time} است'
        })