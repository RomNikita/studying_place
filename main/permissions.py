from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class CanChangeCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ('GET', 'PUT', 'PATCH')


class CannotCreateCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'POST'


class CannotDeleteCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user



