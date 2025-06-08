from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    ROLES = (
        ('AFICIONADO', 'Aficionado'),
        ('ADMIN', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='AFICIONADO')


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nacionalidad = models.CharField(max_length=100)
    equipos_favoritos = models.ManyToManyField('Equipo', blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    escudo = models.ImageField(upload_to='escudos/', null=True, blank=True)
    pais = models.CharField(max_length=100)
    grupo = models.CharField(max_length=1)

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    posicion = models.CharField(max_length=50)
    numero = models.PositiveIntegerField()

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.nombre_completo()


class Estadio(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='estadios/', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Partido(models.Model):
    local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    estadio = models.ForeignKey(Estadio, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)
    finalizado = models.BooleanField(default=False)
    grupo = models.CharField(max_length=1)

    def marcador(self):
        return f"{self.goles_local} - {self.goles_visitante}"

    def __str__(self):
        return f"{self.local} vs {self.visitante}"


class EventoPartido(models.Model):
    TIPO_EVENTO = (
        ('GOL', 'Gol'),
        ('AMARILLA', 'Tarjeta amarilla'),
        ('ROJA', 'Tarjeta roja'),
        ('CAMBIO', 'Cambio'),
        ('LESION', 'Lesión'),
    )
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=10, choices=TIPO_EVENTO)
    minuto = models.PositiveIntegerField()
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.jugador}"


class ComentarioPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario}"