from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save

#class Ejemplo(models.Model):
#    def __str__(self):
#        return 

class Persona(models.Model):
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Edad = models.IntegerField()
    def __str__(self):
        return self.Nombre + " " + self.Apellido
    

class Comedor(models.Model):
    Nombre = models.CharField(max_length=50)
    Calle = models.CharField(max_length=50, null = True)
    Numero = models.IntegerField(null = True)
    Complejo = models.CharField(blank=True, max_length=50)
    class Meta:
         verbose_name_plural = "Comedores"
    def __str__(self):
        return self.Nombre

class Chico(Persona):
    GENEROS = (
            ('1', 'Masculino'),
            ('2', 'Femenino'),
            ('3', 'Otros'),
    )
    Fecha_nacimiento = models.DateField()
    Comedor = models.ForeignKey(Comedor, on_delete = models.CASCADE, null = True, blank = True)
    Genero = models.CharField(max_length=1, choices=GENEROS, default=1)

class Psico_chico(Persona):
    GENEROS = (
            ('1', 'Masculino'),
            ('2', 'Femenino'),
            ('3', 'Otros'),
    )
    Fecha_nacimiento = models.DateField()
    Genero = models.CharField(max_length=1, choices=GENEROS, default=1)
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True, verbose_name='En caso de ser un chico de un comerdor ya existente')
    class Meta:
         verbose_name = "Chico del programa de psicologia"
         verbose_name_plural = "Chicos del programa de psicologia"

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
    Psico_chico = models.ForeignKey(Psico_chico, on_delete = models.CASCADE, null = True, blank = True)
    Parentesco = models.CharField(max_length=1, choices=PARENTESCOS)
    Trabajo = models.CharField(max_length=50)
    class Meta:
         verbose_name_plural = "Familiares"

class Observacion_psico(models.Model):
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    Texto = models.TextField(verbose_name='Introducir texto')
    Fecha = models.DateField(auto_now = True)
    Alergias = models.CharField(max_length=50)
    Altura = models.IntegerField()
    Altura = models.CharField(max_length=50)
    Peso = models.IntegerField()
    def __str__(self):
        return self.Chico + " " + str(self.Fecha)
    class Meta:
        verbose_name = "Observaciones Psicologica"
        verbose_name_plural = "Observaciones Psicologicas"

class Taller(models.Model):
    Nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.Nombre
    class Meta:
        verbose_name_plural = "Talleres"

class Asistencia(models.Model):
    Fecha = models.DateField()
    Chico = models.ManyToManyField(Chico)
    Taller = models.ForeignKey(Taller, on_delete = models.CASCADE, null = True, blank = True)
    def __str__(self):
        return str(self.Fecha)

class Observacion(models.Model):
    Chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    Texto = models.TextField(verbose_name='Introducir texto')
    Fecha = models.DateField(auto_now = True)
    Taller = models.ForeignKey(Taller, on_delete = models.CASCADE, null = True, blank = True)
    class Meta:
        verbose_name_plural = "Observaciones"
    def __str__(self):
        return self.Chico.Nombre + " " + str(self.Fecha)

class Alimento(models.Model):
    MEDIDAS = (
            ('1', 'Kilos'),
            ('2', 'Gramos'),
            ('3', 'Litros'),
    )
    Nombre = models.CharField(max_length=50)
    Cantidad = models.IntegerField()
    Medidas = models.CharField(max_length=1, choices=MEDIDAS)
    Fecha_de_vencimiento = models.DateField()
    Enviado =  models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Chequear cuando el alimento sea enviado'
        ))
    Comedor_destino = models.ForeignKey(Comedor, on_delete = models.CASCADE, null = True, blank = True)
    def __str__(self):
        return self.Nombre

class Comida(models.Model):
    Nombre = models.CharField(max_length=50)
    Fecha = models.DateField()
    def __str__(self):
        return self.Nombre

class Menu(models.Model):
    Fecha = models.DateField()
    Comida = models.ManyToManyField(Comida)
    class Meta:
        verbose_name_plural = "Menús"
    def __str__(self):
        return ', '.join([x.Nombre for x in self.Comida.all()]) + " " + str(self.Fecha)

class MyUserManager(BaseUserManager):
    def create_user(self, email, nivel, password = None):
        if not email:
            raise ValueError('Los usuarios deben tener una un mail')
        user_obj = self.model(
            email = self.normalize_email(email)
            )
        user_obj.set_password(password)
        user_obj.is_staff = True
        user_obj.is_active = True
        user_obj.save(using=self.db)
        return self.user_obj
    def create_superuser(self, email, password = None):
        user_obj = self.model(
            email = self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_superuser = True
        user_obj.save(using=self.db)
        return self.user_obj


class MyUser(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    NIVELES = [
        ('1', 'Admin'),
        ('2', 'Psicopedagogo'),
        ('3', 'Psicologo'),
        ('4', 'Cocinero')]

    nombre = models.CharField(max_length=50, blank=False)
    
    apellido = models.CharField(max_length=50, blank=False)

    nivel = models.CharField(max_length=1, choices=NIVELES, null = True)

    email = models.EmailField(_('email address'), blank=False, unique = True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Puede loggearse en esta página.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Quitar este parámetro en lugar de borrar cuentas'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.email

def set_perms(sender, instance, created, **kwargs):
    all = ['Can view religion','Can add religion','Can delete reparacion',
    'Can view chico','Can add chico','Can delete chico',
    'Can view familiar','Can add familiar','Can delete familiar',
    'Can view observacion_psico','Can add observacion_psico','Can delete observacion_psico',
    'Can view taller','Can add taller','Can delete taller',
    'Can view asistencia','Can add asistencia','Can delete asistencia',
    'Can view observacion','Can add observacion','Can delete observacion',
    'Can view comida','Can add comida','Can delete comida',
    'Can view menu','Can add menu','Can delete menu',
    'Can view ingrediente','Can add ingrediente','Can delete ingrediente',
    'Can view psico_chico','Can add psico_chico','Can delete psico_chico',
    'Can view comedor','Can add comedor','Can delete comedor',
    ]
    if created:
        if instance.nivel == '1': 
            permissions = Permission.objects.filter(name__in = all)
            instance.user_permissions.set(permissions) 
        elif instance.nivel == '2':
            permissions = Permission.objects.filter(name__in = ['Can view observacionpsico','Can add observacionpsico','Can view asistencia','Can delete asistencia', 'Can view observacion','Can add observacion','Can delete observacion'])
            instance.user_permissions.set(permissions)
        elif instance.nivel == '3':
            permissions = Permission.objects.filter(name__in = ['Can view psico_chico','Can add psico_chico','Can view chico','Can add chico','Can view observacion_psico','Can add observacion_psico','Can delete observacion_psico'])
            instance.user_permissions.set(permissions)
        elif instance.nivel == '4':
            permissions = Permission.objects.filter(name__in = ['Can view comida','Can add comida','Can delete comida','Can view menu','Can add menu','Can delete menu', 'Can view ingrediente','Can add ingrediente','Can delete ingrediente',])
            instance.user_permissions.set(permissions)

post_save.connect(set_perms, sender = MyUser)

