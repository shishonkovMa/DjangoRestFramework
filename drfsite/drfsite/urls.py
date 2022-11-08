from django.contrib import admin
from django.urls import path, include, re_path
from women.views import *
from rest_framework import routers # Чтобы определить набор стандартных маршрутов для WomenViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


# ДО ДУБЛИРОВАНИЯ КОДА

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('api/v1/womenlist/', WomenAPIView.as_view()),
#     # path('api/v1/womenlist/<int:pk>/', WomenAPIView.as_view()), # было со своим представлением
#     path('api/v1/womenlist/', WomenAPIList.as_view()),
#     path('api/v1/womenlist/<int:pk>/', WomenAPIUpdate.as_view()),
#     # path('api/v1/womenlist/<int:pk>/', WomenAPIList.as_view()),   # стало с классом от разрабов
#     path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),
# ]


#            ||
#            ||
#           ----
#           \  /
#            \/


# ПОСЛЕ УНИЧТОЖЕНИЯ ДУБЛИРОВАНИЯ КОДА


# # SimpleRouter
# # router = routers.SimpleRouter()
# # router.register(r'women', WomenViewSet) # после создания нам нужно зарегистрировать в нем класс ViewSet'ов


# # DefaultRouter - разница с SimpleRouter в том, что в DefaultRouter есть маршрут "http://127.0.0.1:8000/api/v1/"
# router = routers.DefaultRouter()
# router.register(r'women', WomenViewSet, basename='women') # можем задать свой префикс basename='men' 
#                                                         #(он обязателен, если в WomenViewSet мы не указываем атрибут "queryset")
# print(router.urls)


# # Класс роутеров фактически формирует список маршрутов и связывает их с определенным ViewSet


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v1/', include(router.urls)), # маршрут будет выглядеть так: http://127.0.0.1:8000/api/v1/women/
#     # path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})), # откуда прописываем словарь внутри класса-представления? Документация: https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
#     # path('api/v1/womenlist/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
# ]

#            ||
#            ||
#           ----
#           \  /
#            \/


# ДЛЯ ПОНИМАНИЯ PERMISSIONS

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/drf-auth/', include('rest_framework.urls')), # авторизация на основе сессий-кук

    path('api/v1/women/', WomenAPIList.as_view()), #для получения списка статей
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()), #для обновления статей
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()), #для удаления записей

    path('api/v1/auth/', include('djoser.urls')), # для джосера (авторизация)
    re_path(r'^auth/', include('djoser.urls.authtoken')), # для джосера

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
