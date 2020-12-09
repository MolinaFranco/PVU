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
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre + " " + self.apellido


class Comedor(models.Model):
    nombre = models.CharField(max_length=50)
    calle = models.CharField(max_length=50, null = True)
    numero = models.IntegerField(null = True)
    complejo = models.CharField(blank=True, max_length=50)
    class Meta:
         verbose_name_plural = "Comedores"
    def __str__(self):
        return self.nombre

class Chico(Persona):
    generos = (
            ('1', 'Masculino'),
            ('2', 'Femenino'),
            ('3', 'Otros'),
    )
    fecha_nacimiento = models.DateField()
    comedor = models.ForeignKey(Comedor, on_delete = models.CASCADE, null = True, blank = True)
    genero = models.CharField(max_length=1, choices=generos, default=1)

    def Edad(self):
        import datetime
        self.edad = ((datetime.date.today().year - self.fecha_nacimiento.year))
        return self.edad
            

    def __str__(self) -> str:
        return super().__str__()

class Psicochico(Persona):
    generos = (
            ('1', 'Masculino'),
            ('2', 'Femenino'),
            ('3', 'Otros'),
    )
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=generos, default=1)

    def Edad(self):
        import datetime
        self.edad = ((datetime.date.today().year - self.fecha_nacimiento.year))
        return self.edad

    class Meta:
         verbose_name = "Chico del programa de psicologia"
         verbose_name_plural = "Chicos del programa de psicologia"

class Familiar(Persona):
    parentesco = (
            ('1', 'Padre'),
            ('2', 'Madre'),
            ('3', 'Tio'),
            ('4', 'Tia'),
            ('5', 'Hermano'),
            ('6', 'Primo'),
            ('7', 'Abuelo'),
            ('8', 'Abuela'),
    )
    familia_de = models.ForeignKey(Chico , on_delete = models.CASCADE, null = True, blank = True)
    o_familia_de = models.ForeignKey(Psicochico, on_delete = models.CASCADE, null = True, blank = True)
    parentesco = models.CharField(max_length=1, choices=parentesco)
    trabajo = models.CharField(max_length=50, null = True)
    contacto = models.TextField()
    class Meta:
         verbose_name_plural = "Familiares"

class Observacion_psico(models.Model):
    chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    chico_psico = models.ForeignKey(Psicochico, on_delete = models.CASCADE, null = True, blank = True)
    texto = models.TextField(verbose_name='Introducir texto')
    fecha = models.DateField(auto_now = True)
    alergias = models.CharField(max_length=50)
    altura = models.IntegerField()
    altura = models.CharField(max_length=50)
    peso = models.IntegerField()
    def __str__(self):
        return str(self.chico) + " " + str(self.fecha)
    class Meta:
        verbose_name = "Observacion Psicologica"
        verbose_name_plural = "Observaciones Psicologicas"

class Taller(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Talleres"

class Asistencia(models.Model):
    fecha = models.DateField()
    chico = models.ManyToManyField(Chico, related_name='chico')
    taller = models.ForeignKey(Taller, on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return str(self.taller)+": " +str(self.fecha)

class Observacion(models.Model):
    chico = models.ForeignKey(Chico, on_delete = models.CASCADE, null = True, blank = True)
    texto = models.TextField(verbose_name='Introducir texto')
    fecha = models.DateField(auto_now = True)
    taller = models.ForeignKey(Taller, on_delete = models.CASCADE, null = True, blank = True)
    class Meta:
        verbose_name_plural = "Observaciones"
    def __str__(self):
        return self.chico.nombre + " " + str(self.fecha)

class Alimento(models.Model):
    medidas = (
            ('1', 'Kilos'),
            ('2', 'Gramos'),
            ('3', 'Litros'),
    )
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    medidas = models.CharField(max_length=1, choices=medidas)
    vencimiento = models.DateField()
    enviado =  models.BooleanField(
        _('enviado'),
        default=False,
        help_text=_(
            'Chequear cuando el alimento sea enviado'
        ))
    comedor_destino = models.ForeignKey(Comedor, on_delete = models.CASCADE, null = True, blank = True)
    def __str__(self):
        return self.nombre

class Comida(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    def __str__(self):
        return self.nombre

class Menu(models.Model):
    fecha = models.DateField()
    comida = models.ManyToManyField(Comida)
    class Meta:
        verbose_name_plural = "Menús"
    def __str__(self):
        return ', '.join([x.nombre for x in self.comida.all()]) + " " + str(self.fecha)

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
    niveles = [
        ('1', 'Admin'),
        ('2', 'Psicopedagogo'),
        ('3', 'Psicologo'),
        ('4', 'Cocinero')]

    nombre = models.CharField(max_length=50, blank=False)

    apellido = models.CharField(max_length=50, blank=False)

    nivel = models.CharField(max_length=1, choices=niveles, null = True)

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
    all = [
    'Can view chico','Can add chico','Can delete chico','Can change chico',
    'Can view familiar','Can add familiar','Can delete familiar','Can change familiar',
    'Can view Observacion Psicologica','Can add Observacion Psicologica','Can delete Observacion Psicologica','Can change Observacion Psicologica',
    'Can view taller','Can add taller','Can delete taller','Can change taller',
    'Can view asistencia','Can add asistencia','Can delete asistencia','Can change asistencia',
    'Can view observacion','Can add observacion','Can delete observacion','Can change observacion',
    'Can view comida','Can add comida','Can delete comida','Can change comida',
    'Can view menu','Can add menu','Can delete menu','Can change menu',
    'Can view alimento','Can add alimento','Can delete alimento','Can change alimento',
    'Can view Chico del programa de psicologia','Can add Chico del programa de psicologia','Can delete Chico del programa de psicologia','Can change Chicos del programa de psicologia',
    'Can view comedor','Can add comedor','Can delete comedor','Can change comedor',
    'Can view Usuario','Can add Usuario','Can delete Usuario','Can change Usuario',
    ]
    if created:
        #'Admin'
        if instance.nivel == '1':
            permissions = Permission.objects.filter(name__in = all)
            instance.user_permissions.set(permissions)
        #'Psicopedagogo'
        elif instance.nivel == '2':
            permissions = Permission.objects.filter(name__in = ['Can view familiar','Can add familiar','Can change familiar','Can view asistencia','Can add asistencia','Can change asistencia','Can view chico','Can add chico','Can change chico','Can view observacion','Can add observacion','Can change observacion','Can delete observacion'])
            instance.user_permissions.set(permissions)
        #'Psicologo'
        elif instance.nivel == '3':
            permissions = Permission.objects.filter(name__in = ['Can view Chico del programa de psicologia','Can add Chico del programa de psicologia','Can delete Chico del programa de psicologia','Can view Observacion Psicologica','Can add Observacion Psicologica','Can change Observacion Psicologica'])
            instance.user_permissions.set(permissions)
        #'Cocinero'
        elif instance.nivel == '4':
            permissions = Permission.objects.filter(name__in = ['Can view alimento','Can add alimento','Can change alimento','Can view comida','Can add comida','Can change comida','Can view menu','Can add menu','Can change menu',])
            instance.user_permissions.set(permissions)

post_save.connect(set_perms, sender = MyUser)
