from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != 'ADMIN':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class FavoritosMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['favoritos'] = {
                'equipos': self.request.user.perfilusuario.equipos_favoritos.all(),
            }
        return context