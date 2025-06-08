from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Prefetch
from .models import Partido, Equipo, Jugador, EventoPartido, ComentarioPartido
from .forms import EventoPartidoForm, ComentarioPartidoForm
from .mixins import AdminRequiredMixin


# Vistas para Partidos
class PartidoListView(ListView):
    model = Partido
    template_name = 'partidos/lista_partidos.html'
    context_object_name = 'partidos'

    def get_queryset(self):
        return Partido.objects.select_related(
            'local', 'visitante', 'estadio'
        ).prefetch_related(
            Prefetch('eventos', queryset=EventoPartido.objects.select_related('jugador')),
            Prefetch('comentarios', queryset=ComentarioPartido.objects.select_related('usuario'))
        ).order_by('-fecha')


class PartidoDetailView(DetailView):
    model = Partido
    template_name = 'partidos/detalle_partido.html'
    context_object_name = 'partido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comentario'] = ComentarioPartidoForm()
        return context


class EventoPartidoCreateView(AdminRequiredMixin, CreateView):
    model = EventoPartido
    form_class = EventoPartidoForm
    template_name = 'partidos/crear_evento.html'

    def form_valid(self, form):
        form.instance.partido_id = self.kwargs['partido_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_partido', kwargs={'pk': self.kwargs['partido_id']})


# Vistas para Equipos
class EquipoListView(ListView):
    model = Equipo
    template_name = 'partidos/lista_equipos.html'
    context_object_name = 'equipos'

    def get_queryset(self):
        return Equipo.objects.prefetch_related(
            Prefetch('jugadores', queryset=Jugador.objects.order_by('numero'))
        ).order_by('nombre')


class EquipoDetailView(DetailView):
    model = Equipo
    template_name = 'partidos/detalle_equipo.html'
    context_object_name = 'equipo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugadores'] = self.object.jugadores.all().order_by('numero')
        return context


# Vistas para Jugadores
class JugadorListView(ListView):
    model = Jugador
    template_name = 'partidos/lista_jugadores.html'
    context_object_name = 'jugadores'

    def get_queryset(self):
        return Jugador.objects.select_related('equipo').order_by('equipo__nombre', 'numero')


class JugadorDetailView(DetailView):
    model = Jugador
    template_name = 'partidos/detalle_jugador.html'
    context_object_name = 'jugador'


# Vistas de autenticación
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'partidos/registration/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'lista_partidos'


# Vista para crear comentarios
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = ComentarioPartido
    form_class = ComentarioPartidoForm

    def form_valid(self, form):
        form.instance.partido_id = self.kwargs['partido_id']
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_partido', kwargs={'pk': self.kwargs['partido_id']})