from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'partidos'

urlpatterns = [
    # Partidos
    path('', views.PartidoListView.as_view(), name='lista_partidos'),
    path('partido/<int:pk>/', views.PartidoDetailView.as_view(), name='detalle_partido'),
    path('partido/<int:partido_id>/evento/nuevo/', views.EventoPartidoCreateView.as_view(), name='crear_evento'),
    path('partido/<int:partido_id>/comentario/', views.ComentarioCreateView.as_view(), name='crear_comentario'),

    # Equipos
    path('equipos/', views.EquipoListView.as_view(), name='lista_equipos'),
    path('equipo/<int:pk>/', views.EquipoDetailView.as_view(), name='detalle_equipo'),

    # Jugadores
    path('jugadores/', views.JugadorListView.as_view(), name='lista_jugadores'),
    path('jugador/<int:pk>/', views.JugadorDetailView.as_view(), name='detalle_jugador'),

    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
