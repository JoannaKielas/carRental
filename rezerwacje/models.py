from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class Auto(models.Model):

    TRANSMISSION_CHOICES = [("AUTOMATIC", "automatic"), ("MANUAL", "manual"), ("BOTH", "both")]
    TYPE_CHOICES = [("CAR", "car"), ("VANS&TRUCKS", "vans&trucks"), ("PREMIUM", "premium")]
    seats = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    brand = models.CharField(max_length=25)
    transmission = models.CharField(max_length=16, choices=TRANSMISSION_CHOICES, default="BOTH")
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default="CAR")

    @property
    def is_reserved(self):
        try:
            rez = self.rezerwacja
        except Rezerwacja.DoesNotExist:
            return False
        else:
            return True


        return rez is not None



    def __str__(self):
        return(f"{self.id}, {self.brand}, {self.seats}_{self.price}_{self.transmission}_{self.type}")



class Rezerwacja(models.Model):
    auto = models.OneToOneField(Auto, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.id} / {self.auto}"


#create a new user
#create a superuser

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have email address")
        if not username:
            raise ValueError("Users must have username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "codingwitjoanna/logo_1080_1080.png"

class Account(AbstractBaseUser, PermissionsMixin) :
    email       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username    = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login  = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    hide_email  = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perm(self, app_label):
        return True
