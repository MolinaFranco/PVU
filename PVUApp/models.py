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

class Observacionpsico(models.Model):
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
        return user_obj
    def create_superuser(self, email, password = None):
        user_obj = self.model(
            email = self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_superuser = True
        user_obj.save(using=self.db)
        return user_obj


class MyUser(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    NIVELES = [
        ('1', 'Admin'),
        ('2', 'Psicopedagogo'),
        ('3', 'Cocinero')]

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
    'Can view domicilio','Can add domicilio','Can delete domicilio',
    'Can view chico','Can add chico','Can delete chico',
    'Can view familiar','Can add familiar','Can delete familiar',
    'Can view observacionpsico','Can add observacionpsico','Can delete observacionpsico',
    'Can view taller','Can add taller','Can delete taller',
    'Can view asistencia','Can add asistencia','Can delete asistencia',
    'Can view observacion','Can add observacion','Can delete observacion',
    'Can view comida','Can add comida','Can delete comida',
    'Can view menu','Can add menu','Can delete menu',
    'Can view ingrediente','Can add ingrediente','Can delete ingrediente',
    ]
    if created:
        if instance.nivel == '1': 
            permissions = Permission.objects.filter(name__in = all)
            instance.user_permissions.set(permissions) 
        elif instance.nivel == '2':
            permissions = Permission.objects.filter(name__in = ['Can view observacionpsico','Can add observacionpsico','Can view asistencia','can add asistencia','Can delete asistencia', 'Can view observacion','Can add observacion','Can delete observacion'])
            instance.user_permissions.set(permissions)
        elif instance.nivel == '3':
            permissions = Permission.objects.filter(name__in = ['Can view comida','Can add comida','Can delete comida','Can view menu','Can add menu','Can delete menu', 'Can view ingrediente','Can add ingrediente','Can delete ingrediente',])
            instance.user_permissions.set(permissions)

post_save.connect(set_perms, sender = MyUser)

