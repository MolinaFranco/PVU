from django.db import models

#class Ejemplo(models.Model):
#    def __str__(self):
#        return 

class Persona(models.Model):
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Edad = models.IntegerField()
    def __str__(self):
        return Nombre + Apellido
    
class Religion(models.Model):
    Nombre = models.CharField(max_length=50)
    def __str__(self):
        return Nombre

class Domicilio(models.Model):
    Calle = models.CharField(max_length=50)
    Numero = models.IntegerField()
    Piso = models.IntegerField(blank=True)
    Complejo = models.CharField(blank=True, max_length=50)

class Chico(Persona):
    Fecha_nacimiento = models.DateField()
    Religion = models.ForeignKey(Religion, on_delete = models.CASCADE, null = True, blank = True)
    Domicilio = models.ForeignKey(Domicilio, on_delete = models.CASCADE, null = True, blank = True)

class Familiar(Persona):
    PARENTESCOS = (
            ('1', 'Padre'),
            ('2', 'Madre'),
            ('3', 'Tio'),
            ('4', 'Tia'),
            ('5', 'Hermano'),
            ('6', 'Primo'),
            ('7', 'Abuelo'),
            ('8', 'Abuela'),
    )
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    Parentesco = models.CharField(max_length=1, choices=PARENTESCOS)
    Trabajo = models.CharField(max_length=50)

class Administrador(Persona):
    Correo_electronico = models.CharField(max_length=50)
    Contraseña = models.CharField(max_length=50)

class Psicopedagogo(Persona):
    Correo_electronico = models.CharField(max_length=50)
    Contraseña = models.CharField(max_length=50)

class Observación_Psico(models.Model):
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    Texto = models.TextField(verbose_name='Introducir texto')
    Fecha = models.DateField(auto_now = True)
    Alergias = models.CharField(max_length=50)
    Altura = models.IntegerField()
    Altura = models.CharField(max_length=50)
    Peso = models.IntegerField()

class Taller(models.Model):
    Nombre = models.CharField(max_length=50)
    def __str__(self):
        return Nombre

class Asistencia(models.Model):
    Fecha = models.DateField()
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    Taller = models.ForeignKey(Taller, on_delete = models.CASCADE, null = True, blank = True)

class Observacion(models.Model):
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    Texto = models.TextField(verbose_name='Introducir texto')
    Fecha = models.DateField(auto_now = True)
    Taller = models.ForeignKey(Taller, on_delete = models.CASCADE, null = True, blank = True)

class Ingrediente(models.Model):
    Nombre = models.CharField(max_length=50)
    Cantidad = models.IntegerField()
    Tipo_de_alimento = models.CharField(max_length=50)
    Fecha_de_vencimiento = models.DateField()
    def __str__(self):
        return Nombre

class Comida(models.Model):
    Nombre = models.CharField(max_length=50)
    Ingrediente = models.ManyToManyField(Ingrediente)
    Fecha = models.DateField()
    def __str__(self):
        return Nombre

class Menu(models.Model):
    Fecha = models.DateField()
    Comida = models.ManyToManyField(Comida)

