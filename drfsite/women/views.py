from rest_framework import generics, viewsets, mixins
from django.shortcuts import render
from .models import Women, Category
from .serializers import WomenSerializer
from rest_framework.views import APIView # стоит во главе иерархии всех классов представлений django.rest_framework
from rest_framework.response import Response
from django.forms import model_to_dict
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination


# ----------------------------------Для абстрактного примера-------------------------------------
# class WomenAPIView(APIView):
#     def get(self, request): # для обработки get-запросов, request - содержит все параметры get-запроса
#         lst = Women.objects.all().values()
#         # return Response({'title': 'Angelina Jolie'}) # Response - класс, который преобразовывает словарь в json-строку
#         return Response({'posts': list(lst)})

#     def post(self, request):
#         # return Response({'title': 'Jen'})
#         post_new = Women.objects.create(
#             title=request.data['title'],
#             content=request.data['content'],
#             cat_id=request.data['cat_id']
#         )
#         return Response({'post': model_to_dict(post_new)}) # model_to_dict - преобразовывает объект модели Women в словарь


# # class WomenAPIView(generics.ListAPIView):
# #     queryset = Women.objects.all()
# #     serializer_class = WomenSerializer





# ----------------------------------Для реального примера-------------------------------------

# class WomenAPIView(APIView):
#     def get(self, request):
#         w = Women.objects.all()
#         return Response({'posts': WomenSerializer(w, many=True).data}) # many=True означает, что сериализатор должен
#                                                                     # обрабатывать не одну запись, а список
#                 # Response, который преобразовывает в байтовую json-строку
#     # т.е. выше выполняются те же самые действия, которые мы прописали в методе encode()


#     # def post(self, request):
#     #     serializer = WomenSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)

#     #     post_new = Women.objects.create(
#     #         title=request.data['title'],
#     #         content=request.data['content'],
#     #         cat_id=request.data['cat_id']
#     #     )
#     #     return Response({'post': WomenSerializer(post_new).data}) # в качестве аргумента передаем один объект
#     #                                                                 # many=True писать не нужно, т.к. many - по умолчанию False


#     # перепишем метод post для того чтобы сам сериализатор сохранял данные в БД
#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save() # вызовет метод create из serializers.py

#         return Response({'post': serializer.data})


#     # метод, обновляющий данные в БД (уже существующих записей)
#     def put(self, request, *args, **kwargs): # плюс набор позиционных аргументов и именнованных
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Metod PUT not allowed"})

#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})

#         serializer = WomenSerializer(data=request.data, instance=instance) # когда мы задаем такие параметры у сериализатора,
#                                                                            # ниженаписанный метод save() автоматически вызовет
#                                                                            # метод update() из serializers.py
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})


#     # метод для удаления записей
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})

#         # здесь код для удаления записи с переданным pk (сейчас это метод-заглушка)

#         return Response({"post": "delete post " + str(pk)})

#            ||
#            ||
#           ----
#           \  /
#            \/


# # Но т.к. мы работаем с Джанго, разрабы потрудились упростить взаимодействие с API и создали свои классы
# # Класс для чтения и создания списка данных


# class WomenAPIList(generics.ListCreateAPIView): # это представление реализует два метода GET и POST
#     queryset = Women.objects.all() # строгое обозначение атрибутов
#     serializer_class = WomenSerializer


# class WomenAPIUpdate(generics.UpdateAPIView): # представление реализует методы PUT и PATCH
#     queryset = Women.objects.all() # ленивый запрос
#     serializer_class = WomenSerializer


# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView): # класс-представление для чтения,
#                                                                     # изменения и добавления отдельной записи 
#                                                                     # (GET-, PUT-, PATCH- и DELETE-запросы)
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

#            ||
#            ||
#           ----
#           \  /
#            \/

# Однако, т.к. у нас во всех классах-представлениях наблюдается дублирование кода, разрабы пошли еще дальше:


# class WomenViewSet(viewsets.ModelViewSet):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# # или это можно реализовать так:


# class WomenViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    # mixins.DeleteModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#     # queryset = Women.objects.all()
#     serializer_class = WomenSerializer


#     # Переопределяем queryset, если хотим выбирать определенные данные
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")

#         if not pk:
#             return Women.objects.all()[:3]

#         return Women.objects.filter(pk=pk)


#     # добавляем новый маршрут в класс WomenViewSet
#     @action(methods=['get'], detail=True) # detail=False - список записей, если True, то одна запись
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})

#            ||
#            ||
#           ----
#           \  /
#            \/

# ДЛЯ ПОНИМАНИЯ PERMISSIONS перепишем наши представления несколько иначе

class WomenAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = WomenAPIListPagination


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # permission_classes = (IsOwnerOrReadOnly, )
    permission_classes = (IsAuthenticated, ) # чтобы содержимое записи мог просматривать только авторизованный пользователь
    # authenticated_classes = (TokenAuthentication, ) # предоставляет доступ только тем пользователям, 
                                                    # которые получают доступ именно по токенам (по сессиям мы уже получить доступ не сможем)
                                                    # если закомментировать, то будут возможны оба варианта


class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # permission_classes = (IsAdminUsers, ) # доступ удалять записи - только у администраторов
    permission_classes = (IsAdminOrReadOnly, ) # наш вариант, а выше вариант разрабов (но немного другой)










