from rest_framework import viewsets
from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos
from .serializers import UsuariosSerializer, AugaSerializer, MedallasSerializer, TarefasSerializer, CategoriasSerializer, ExerciciosSerializer, PlantillasSerializer, ComidasSerializer, GruposSerializer

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

class AugaViewSet(viewsets.ModelViewSet):
    queryset = Auga.objects.all()
    serializer_class = AugaSerializer

class MedallasViewSet(viewsets.ModelViewSet):
    queryset = Medallas.objects.all()
    serializer_class = MedallasSerializer

class TarefasViewSet(viewsets.ModelViewSet):
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

class ExerciciosViewSet(viewsets.ModelViewSet):
    queryset = Exercicios.objects.all()
    serializer_class = ExerciciosSerializer

class PlantillasViewSet(viewsets.ModelViewSet):
    queryset = Plantillas.objects.all()
    serializer_class = PlantillasSerializer

class ComidasViewSet(viewsets.ModelViewSet):
    queryset = Comidas.objects.all()
    serializer_class = ComidasSerializer

class GruposViewSet(viewsets.ModelViewSet):
    queryset = Grupos.objects.all()
    serializer_class = GruposSerializer
