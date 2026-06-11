from django.conf import settings
from django.db import models

from .constants import (
    DESCRIPTION_MAX_LENGTH,
    NAME_MAX_LENGTH,
    STATUS_CHOICES,
    STATUS_MAX_LENGTH,
    STATUS_OPEN,
)


class Project(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    description = models.TextField(
        'Описание',
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    github_url = models.URLField('GitHub', blank=True)
    status = models.CharField(
        'Статус',
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_projects',
        blank=True,
        verbose_name='Участники',
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
