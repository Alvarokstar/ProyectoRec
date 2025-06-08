from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'rol'),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nacionalidad')
    filter_horizontal = ('equipos_favoritos',)

class EventoPartidoInline(admin.TabularInline):
    model = EventoPartido
    extra = 1

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'grupo')
    list_filter = ('grupo', 'pais')
    search_fields = ('nombre', 'pais')

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'equipo', 'posicion', 'numero')
    list_filter = ('equipo', 'posicion')
    search_fields = ('nombre', 'apellido')

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fecha', 'estadio', 'grupo', 'marcador')
    list_filter = ('grupo', 'estadio', 'finalizado')
    inlines = [EventoPartidoInline]

@admin.register(Estadio)
class EstadioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'capacidad')

@admin.register(EventoPartido)
class EventoPartidoAdmin(admin.ModelAdmin):
    list_display = ('partido', 'tipo', 'jugador', 'minuto')

@admin.register(ComentarioPartido)
class ComentarioPartidoAdmin(admin.ModelAdmin):
    list_display = ('partido', 'usuario', 'fecha')