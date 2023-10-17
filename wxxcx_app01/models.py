from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, username, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('手机号必须填写'))
        if not username:
            raise ValueError(_('用户名必须填写'))

        # 密码验证
        if not password:
            raise ValueError(_('密码必须填写'))
        if not (8 <= len(password) <= 16) or password.isdigit() or not password.isalnum():
            raise ValueError(_('密码格式不正确'))

        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('手机号'), max_length=11, unique=True, validators=[
        RegexValidator(regex='^.{11}$', message='手机号长度必须为11位', code='nomatch')])
    username = models.CharField(_('用户名'), max_length=8, validators=[
        RegexValidator(regex='^[\u4e00-\u9fa5]{1,8}$', message='用户名必须为1-8位汉字', code='nomatch')])
    avatar = models.ImageField(_('用户头像'), upload_to='avatars/')
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="customuser_groups",
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="customuser_user_permissions",
        help_text=_('Specific permissions for this user.'),
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')


class Task(models.Model):
    pickupAddress = models.CharField(max_length=255)
    deliveryAddress = models.CharField(max_length=255)
    pickupInfo = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    expressSize = models.CharField(max_length=255)
    expressWeight = models.CharField(max_length=255)
    totalPrice = models.DecimalField(max_digits=6, decimal_places=2)


class Courier(models.Model):
    realName = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)  # 使用class_name而不是class，因为class是保留关键字
    studentId = models.CharField(max_length=255)
    # imagePath = models.CharField(max_length=1024,null=True)  # 如果你使用ImageField存储图像，这里会有所不同
    imagePath = models.ImageField(upload_to='couriers/')
