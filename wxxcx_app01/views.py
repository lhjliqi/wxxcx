from django.db.utils import IntegrityError
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Courier
from .serializers import CourierSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import User


class CourierCreateAPI(generics.CreateAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TaskCreateAPI(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': '任务成功创建'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(request.data)
        user = authenticate(username=username, password=password)
        if not username or not password:
            return Response({'status': 'fail', 'message': '用户名和密码是必填的'})
        if user:
            return Response({'status': 'success', 'message': '登录成功'})
        else:
            return Response({'status': 'fail', 'message': '用户名或密码错误,请重新输入'})


class RegisterAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        avatar = request.FILES.get('avatar')
        nickname = request.data.get('nickname')
        print(request.data)
        # 检查必要的字段是否存在
        if not phone or not password or not avatar or not nickname:
            return Response({'status': 'fail', 'message': '电话，密码，手机号，用户名均为必填项'})

        # 检查电话号码
        if len(phone) != 11 or not phone.isdigit():
            return Response({'status': 'fail', 'message': '电话号码不符合标准'})

        # 检查密码
        if not (8 <= len(password) <= 16) or password.isdigit() or not password.isalnum():
            return Response({'status': 'fail', 'message': '密码格式不正确'})

        try:
            user = User.objects.create_user(phone=phone, password=password, avatar=avatar, username=nickname)
            return Response({'status': 'success', 'message': '注册成功'})
        except IntegrityError:
            return Response({'status': 'fail', 'message': '该账号已注册'})
        except ValueError as e:
            return Response({'status': 'fail', 'message': str(e)})


class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
