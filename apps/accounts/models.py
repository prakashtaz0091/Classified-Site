from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class myaccountmanager(BaseUserManager):
    def create_user(self,full_name,email,password=None):
        if not email:
            raise ValueError('user must have an email address')

        if not full_name:
            raise ValueError('user must have an full_name')

        
        user=self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        return user


    def create_superuser(self,full_name,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
            
        )

        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user







class Account(AbstractBaseUser):
    full_name= models.CharField(max_length=50)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=20,null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['full_name',]

    objects=myaccountmanager()

    def __str__(self):
        return self.email
    

    def has_perm(self,perm,obj=None):
        return self.is_admin
    

    def has_module_perms(self,add_label):
        return True



class UserProfile(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    email_address = models.EmailField(unique=True)
    notes = models.TextField(blank=True,null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    
    
    def get_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        return '/assets/img/profile-img.jpg'
    
    
    def __str__(self):
        return self.full_name