from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, PermissionsMixin, BaseUserManager )
from django.db.models.signals import post_save

def getCustomUserPerms(id):
    return CustomUser.objects.get(id=id).get_all_permissions()


def check_permission(user_id, perm_check):
    perms = getCustomUserPerms(user_id)
    x = perm_check in perms
    if not x:
        a = perm_check.split('.')[1].split('_')
        raise Exception("Not Authorised To " + " ".join(a))
    
DEPT_CHOICES = (
    ("Registration", "Registration"), ("Radiology", "Radiology"), ("Laboratory", "Laboratory"), ("Maternity", "Maternity"),
    ("Consultation", "Consultation"), ("Opthtamology", "Opthtamology"), ("Dental", "Dental"), ("Pharmacy", "Pharmacy"), 
    ("Payment", "Payment"), ("Procurement", "Procurement"), ("Shop", "Shop"),
    ("Technical", "Technical"), ("Administration", "Administration"), ("Finance", "Finance"), ("Physiotherapy", "Physiotherapy"),
)
ROLE_CHOICES = (
    ("superadmin", "superadmin"), ("admin", "admin"), ("hod", "hod"), ("staff", "staff"),
)

class CustomUserManager(BaseUserManager):
    def create_superuser(self, password, username, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser Must Have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser Must Have is_superuser=True")

        if not username:
            raise ValueError("Username Field Is Required")

        user = self.model(
            username=username, **extra_fields, 
        )
        user.set_password(password)
        user.save()

        return user
    

def create_profile(sender, **kwargs):
    created_item = kwargs['instance']
    if kwargs['created']:
        prof = UserProfile.objects.create(
                user = created_item,
                # created_by = created_item.created_by,
            )
        prof.save()


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["role",]
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} {self.id}"

    class Meta:
        ordering = ("created_at",)
    

post_save.connect(create_profile, sender=CustomUser)



class UserProfile(models.Model):
    user = models.OneToOneField( CustomUser, related_name="user_profile", null=True, on_delete=models.CASCADE )
    first_name = models.CharField(max_length=50, unique=False, null=True, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    about = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=6, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    # speciality = models.CharField(max_length=50, blank=True)
    # title = models.CharField(max_length=50, blank=True)
    # pob = models.CharField(max_length=25, null=True, blank=True)
    # dob = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.id} {self.user.username}"
    

class UserActivities(models.Model):
    username = models.CharField(max_length=50)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.username} {self.action} on {self.created_at}"


class CompanyProfile(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, null=False)
    # image = models.ImageField()
    niu = models.CharField(max_length=20, blank=False, null=False)
    telephone_one = models.CharField(max_length=15, blank=False, null=False)
    telephone_two = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=False, null=False)
    about = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=False, null=False)
    website = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} {self.niu}"
