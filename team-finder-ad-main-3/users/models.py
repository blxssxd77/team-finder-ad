from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from .utils import generate_avatar


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if not user.avatar:
            user.avatar = generate_avatar(user.name or 'U')
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', 'Admin')
        extra_fields.setdefault('surname', 'Admin')
        extra_fields.setdefault('phone', '+70000000000')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Имя', max_length=124)
    surname = models.CharField('Фамилия', max_length=124)
    avatar = models.ImageField('Аватар', upload_to='avatars/')
    phone = models.CharField('Телефон', max_length=12, blank=True, default='')
    github_url = models.URLField('GitHub', blank=True)
    about = models.TextField('О себе', max_length=256, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Администратор', default=False)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Избранные проекты',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = generate_avatar(self.name or 'U')
        super().save(*args, **kwargs)
