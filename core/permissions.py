from rest_framework import permissions

class IsTweetCreatorOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir apenas ao criador do tweet editar ou excluir.
    """

    def has_object_permission(self, request, view, obj):
        # Permite que todos possam visualizar (GET), independentemente da permissão.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permite ao criador do tweet editar ou excluir.
        return obj.user == request.user
