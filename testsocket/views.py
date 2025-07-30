import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from testsocket.models import CustomUser, ChatGroup
from testsocket.serializers import UserSerializer


class RegisterAPIView(APIView):
    @swagger_auto_schema(
        operation_description="ثبت‌نام کاربر جدید",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'username', 'password'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='نام کامل'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='نام کاربری یکتا'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='رمز عبور'),
            },
        ),
        responses={
            201: UserSerializer,
            400: openapi.Response('خطای ورودی یا تکراری بودن نام کاربری')
        }
    )
    def post(self, request):
        data = request.data

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

    @swagger_auto_schema(
        security=[{'Bearer': []}],  # این خط مهم است
        operation_description="ایجاد یک گروه چت جدید و دریافت آدرس وب‌سوکت",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='نام گروه چت تولیدشده'),
                    'websocket_url': openapi.Schema(type=openapi.TYPE_STRING, description='آدرس ws گروه چت'),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='پیام خوش‌آمد و ساعت فعلی')
                }
            ),
            401: openapi.Response('نیازمند توکن JWT معتبر')
        }
    )
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

class SendTestMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        operation_description="ارسال پیام 'test' به گروه چت مشخص‌شده از طریق WebSocket",
        manual_parameters=[
            openapi.Parameter(
                'group_name',
                openapi.IN_QUERY,
                description="نام گروه چت (مثل chat_a1b2c3d4)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='پیام موفقیت')
                }
            ),
            400: openapi.Response('گروه یافت نشد یا پارامتر نامعتبر'),
            401: openapi.Response('نیازمند توکن JWT معتبر')
        }
    )
    def get(self, request):
        group_name = request.query_params.get('group_name')

        if not group_name:
            return Response({'error': 'group_name is required'}, status=400)

        # بررسی وجود گروه
        if not ChatGroup.objects.filter(name=group_name, creator=request.user).exists():
            return Response({'error': 'Group not found or you are not the creator'}, status=400)

        # ارسال پیام به گروه از طریق WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': 'test'
            }
        )

        return Response({'message': 'Test message sent to WebSocket group'}, status=200)