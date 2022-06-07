from django.http import JsonResponse , FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from rest_framework import status ,generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
import random
import os


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/register',
    ]

    return Response(routes)

class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self,request,format=True):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data =  {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user' : serializer.data
            }
            return Response(response_data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class LogOutAPIView(APIView):
    def post(self,request,format=True):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(response_data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class ImageAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        random.seed(45)
        response_arr = []
        if not kwargs.get('item'):
            try:
                for i in range(int(kwargs['num'])):
                    src = os.getcwd() + '/base/static/images/'
                    if kwargs['class'] == 'mix':
                        Class = random.choice(os.listdir(src))
                        src += str(Class) + '/'
                    else:
                        src += kwargs['class'] + '/'
                    item = random.choice(os.listdir(src))
                    src += str(item) + '/'
                    src += random.choice(os.listdir(src))
                    img = open(src, 'rb')
                    response_arr.append('http://127.0.0.1:8000/api' + src[len(os.getcwd()) :])
                return Response({'images': response_arr},status = status.HTTP_200_OK)
            except Exception as e:
                return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

        else:
            src = '../backend/base/static/images/{}/{}/{}'.format(
                kwargs['class'], kwargs['item'], kwargs['img'])
            
            img = open(src, 'rb')
            response = FileResponse(img)
            return response