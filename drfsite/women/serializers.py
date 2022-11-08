from rest_framework import serializers
from .models import Women
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


# ----------------------------------Абстрактная штука-------------------------------------
# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255) # прописанные имена должны совпадать с атрибутами WomenModel
#     content = serializers.CharField()


# def encode(): # выполнять кодирования преобразования объектов WomenModel в json-формат
#     model = WomenModel('Angeline Jolie', 'Content: Angeline Jolie')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data) # JSONRenderer преобразовывает объект сериализации в байтовую json-строку
#     print(json)


# def decode(): # обратное преобразование из json-строки в объект класса WomenModel
#     stream = io.BytesIO(b'{"title": "Angeline Jolie", "content": "Content: Angeline Jolie"}')
#     data = JSONParser().parse(stream)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data) # коллекция validated_data - результат декодирования json-строки


# # class WomenSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Women
# #         fields = ('title', 'cat_id')





# ----------------------------------Для модели приложения-------------------------------------

# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField() # не как в модели (там ForeignKey, здесь IntegerField)

#     # метод, создающий новые записи в БД
#     def create(self, validated_data):
#         return Women.objects.create(**validated_data)


#     # метод, изменяющий уже существующие записи в БД
#     def update(self, instance, validated_data): # instance - ссылка на объект модели Women
#                                                 # validated_data - словарь из проверенных данных, которые нужно изменить
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.time_update = validated_data.get("time_update", instance.time_update)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save()
#         return instance

#            ||
#            ||
#           ----
#           \  /
#            \/


# Но т.к. мы работаем с моделью Джанго, то можно использовать другой, более подходящий класс:

class WomenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # HiddenField - скрытое поле, CurrentUserDefault - текущий пользователь
    class Meta:
        model = Women
        # fields = ("title", "content", "cat")
        fields = "__all__" # если хотим указать все поля
