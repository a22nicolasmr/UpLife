from rest_framework import serializers
from .models import Usuarios, Auga, Medallas, Tarefas, Categorias, Exercicios, Plantillas, Comidas, Grupos

# facer apis con todos os campos de todos os modelos
class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

class AugaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auga
        fields = '__all__'

class MedallasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medallas
        fields = '__all__'

class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'

class ExerciciosSerializer(serializers.ModelSerializer):
    categoria = CategoriasSerializer()
    
    class Meta:
        model = Exercicios
        fields = '__all__'

class PlantillasSerializer(serializers.ModelSerializer):
    exercicios = ExerciciosSerializer(many=True)

    class Meta:
        model = Plantillas
        fields = '__all__'

class ComidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comidas
        fields = '__all__'

class GruposSerializer(serializers.ModelSerializer):
    comidas = ComidasSerializer(many=True)

    class Meta:
        model = Grupos
        fields = '__all__'
