from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

# Create your models here.

class myaccountmanager(BaseUserManager):
    def create_user(self, full_name, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

        # Create associated UserProfile
        UserProfile.objects.create(
            user=user,
            full_name=user.full_name,
            email_address=user.email
        )

        return user


class Account(AbstractBaseUser):
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    role = models.CharField(blank=True, null=True, max_length=100,)
    last_activity = models.DateTimeField(null=True, blank=True)
    last_password_change = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = myaccountmanager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])
    
    def set_password(self, raw_password):
        super().set_password(raw_password)
        if self.pk is None:
            # Save the instance first to ensure it has a primary key
            self.save()
        self.last_password_change = timezone.now()
        self.save(update_fields=['last_password_change'])


class UserProfile(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="profile"
    )
    email_address = models.EmailField(unique=True)
    notes = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to="profile_photos/", blank=True, null=True, default="profile_photos/profile.png"
    )
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name
