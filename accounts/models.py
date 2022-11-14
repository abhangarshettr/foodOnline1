from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey,OneToOneField




# Create your models here.

# UserManager will extend from baseusermanager

class UserManager(BaseUserManager):
    # Method if user doesnt provide email or username
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("User must have email address")
        
        if not username:
            raise ValueError("User must have Username")
        
        #creating method for regular user
        user =self.model(
            # It takes email address from user and converts it into lowercase
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            
        )
        # set_password is a method that takes the password and encodes it
        user.set_password(password)
        #django by default uses "using" paramater to define which db should be used
        #As for tis project we are using only on edb, self._db will take default db
        user.save(using=self._db)
        return user
    
    #creating method for super_user
    def create_superuser(self,first_name,last_name,username,email,password=None):
        #using the create_user method to create super_admin
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
            first_name = first_name,
            last_name = last_name,
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
               
# AbstracBbaseUser provides complete control for the custom model
class User(AbstractBaseUser):
    RESTRAUNT = 1
    CUSTOMER =2
    ROLE_CHOICE=(
        (RESTRAUNT,'Restraunt'),
        (CUSTOMER,'Customer'),
        
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.CharField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=12,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
    
    #required feilds
    date_joined =models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    
    #Authentication 
    #useranme is over-wriiten by email address as the default login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = UserManager()
    def __str__(self):
        return self.email
    
    #return id admin has access
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    #return TRue is user is an active super_user
    def has_module_perms(self,app_label):
        return True
    
class Userprofile(models.Model):
    #one user can have only one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    profile_picture=models.ImageField( upload_to='users/profile_pictures', blank = True,null=True)
    #cover_photo=models.ImageField( upload_to='users/cover_photos', blank = True,null=True)
    address_lines_1=models.CharField(max_length=50,blank=True,null=True)
    address_lines_2=models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=15,blank=True,null=True)
    state=models.CharField(max_length=15,blank=True,null=True)
    city = models.CharField(max_length=15,blank=True,null=True)
    pin_code = models.CharField(max_length=6,blank=True,null=True)
    longitude=models.CharField(max_length=20,blank=True,null=True)
    latitude=models.CharField(max_length=20,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email
    
    #create a receiver
    #"created returns true when user is created"
    # User is sender and the below function is receiver
    

    
    
    
    