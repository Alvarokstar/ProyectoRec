from django.utils import timezone
from django.http import HttpResponseBadRequest


class ValidacionFechaPartidoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'partidos' in request.path:
            fecha_str = request.POST.get('fecha')
            if fecha_str:
                fecha = timezone.datetime.fromisoformat(fecha_str)
                if fecha < timezone.now():
                    return HttpResponseBadRequest("No se puede registrar un partido en el pasado como futuro")
        return self.get_response(request)