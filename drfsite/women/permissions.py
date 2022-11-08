from rest_framework import permissions


# создаем свой класс ограничений прав доступа (удалять может только админ, а читать зарегистрированные пользователи)
class IsAdminOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

		return bool(request.user and request.user.is_staff)


# читать могут все, изменять только пользователь, создавший запись
class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner == request.user