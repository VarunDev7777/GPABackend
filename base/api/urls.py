from django.urls import path
from . import views
from .views import MyTokenObtainPairView , RegisterAPIView ,LogOutAPIView,ImageAPIView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(),name='register_view'),
    path('logout/', LogOutAPIView.as_view(),name='logout_view'),
    path('images/<class>/<num>/', ImageAPIView.as_view(), name='image_view'),
    path('base/static/images/<class>/<item>/<img>/', ImageAPIView.as_view(), name='image_view'),
]