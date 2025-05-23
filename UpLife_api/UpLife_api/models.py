from django.db import models
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
import os
import cloudinary.uploader
from django.db.models.signals import pre_save
# opcions modo_aplicacion
MODO_CHOICES = [
    ('C', 'Claro'),
    ('E', 'Escuro'),
]

class Usuarios(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=100)
    nome_usuario=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=255, unique=True)
    contrasinal=models.CharField(max_length=100)
    imaxe_perfil = models.ImageField(upload_to="avatares", null=True, blank=True)
    xenero=models.CharField(max_length=7, null=True, blank=True)
    altura=models.IntegerField(null=True, blank=True)
    peso=models.IntegerField(null=True, blank=True)
    obxectivo=models.CharField(max_length=30, null=True, blank=True)
    actividade=models.CharField(max_length=30,null=True, blank=True)
    idade=models.IntegerField(null=True, blank=True)
    calorias_diarias=models.IntegerField(null=True, blank=True)
    auga_diaria=models.IntegerField(null=True, blank=True)
    modo_aplicacion=models.CharField(max_length=1,choices=MODO_CHOICES)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.contrasinal = make_password(self.contrasinal)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"nome={self.nome}, nome_usuario={self.nome_usuario}, email={self.email}, contrasinal={self.contrasinal}, imaxe_perfil={self.imaxe_perfil}, altura={self.altura}, peso={self.peso}, obxectivo={self.obxectivo}, actividade={self.actividade}, idade={self.idade}, calorias_diarias={self.calorias_diarias}, auga_diaria={self.auga_diaria}, modo_aplicacion={self.modo_aplicacion}"

# cando se actualiza a imaxe de perfil , borrase a existente e actualizase ca nova
# @receiver(models.signals.pre_save, sender=Usuarios)
# def auto_delete_old_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return

#     try:
#         old_file = sender.objects.get(pk=instance.pk).imaxe_perfil
#     except sender.DoesNotExist:
#         return

#     new_file = instance.imaxe_perfil
#     if old_file and old_file.name:
#         try:
#             if os.path.isfile(old_file.path):
#                 os.remove(old_file.path)
#         except Exception as e:
#             print(f"Error eliminando archivo anterior: {e}")

@receiver(pre_save, sender=Usuarios)
def borrar_imaxe_anterior_cloudinary(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        usuario_anterior = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # Se a imaxe cambia, borrar a anterior
    if usuario_anterior.imaxe_perfil and usuario_anterior.imaxe_perfil != instance.imaxe_perfil:
        try:
            public_id = usuario_anterior.imaxe_perfil.public_id
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Erro ao borrar a imaxe anterior: {e}")            
class Auga(models.Model):
    id_auga=models.BigAutoField(primary_key=True)
    cantidade=models.IntegerField()
    hora=models.TimeField()
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    data=models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f"cantidade={self.cantidade}, hora={self.hora}, usuario={self.usuario}"

class Medallas(models.Model):
    id_medalla=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=50,unique=True)
    descripcion=models.CharField(max_length=200,unique=True)
    completado=models.BooleanField()
    icona=models.ImageField(upload_to="media")
    usuarios=models.ManyToManyField(Usuarios)
    def __str__(self):
        return f"nome={self.nome}, descripcion={self.descripcion}, completado={self.completado}, icona={self.icona}"

class Tarefas(models.Model):
    id_tarefa=models.BigAutoField(primary_key=True)
    hora=models.TimeField(blank=True,null=True)
    titulo=models.CharField(max_length=255)
    data=models.DateField()
    completado=models.BooleanField()
    data=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)

    def __str__(self):
        return f"titulo={self.titulo}, hora={self.hora}, data={self.data}, completado={self.completado}, usuario={self.usuario}"

class Categorias(models.Model):
    id_categoria=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=10)

    def __str__(self):
        return f"nome={self.nome}"

class Exercicios(models.Model):
    id_exercicio=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255)
    repeticions=models.CharField(max_length=10)
    peso=models.FloatField()
    data=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    categoria=models.ForeignKey(Categorias,on_delete=models.CASCADE)

    def __str__(self):
        return f"nome={self.nome}, repeticions={self.repeticions}, peso={self.peso}, usuario={self.usuario}, categoria={self.categoria}"

class Plantillas(models.Model):
    id_plantilla=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255,unique=True)
    icona = models.CharField(max_length=255)
    data=models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    exercicios = models.ManyToManyField(Exercicios, blank=True)

    def __str__(self):
        return f"nome={self.nome}, icona={self.icona}, exercicios={[e.nome for e in self.exercicios.all()]}"

class Comidas(models.Model):
    id_comida=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255)
    peso=models.FloatField()
    graxas=models.FloatField()
    carbohidratos=models.FloatField()
    proteinas=models.FloatField()
    calorias=models.FloatField()
    data=models.DateField(null=True, blank=True)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE)

    def __str__(self):
        return f"nome={self.nome}, peso={self.peso}, graxas={self.graxas}, carbohidratos={self.carbohidratos}, proteinas={self.proteinas}, calorias={self.calorias}, usuario={self.usuario}"

class Grupos(models.Model):
    id_grupo=models.BigAutoField(primary_key=True)
    nome=models.CharField(max_length=255)
    icona= models.CharField(max_length=255)
    comidas=models.ManyToManyField(Comidas)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f"nome={self.nome}, icona={self.icona}, comidas={[c.nome for c in self.comidas.all()]}"

