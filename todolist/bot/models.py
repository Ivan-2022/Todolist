from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField()
    username = models.CharField(max_length=100, null=True, blank=True, default=None)
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, null=True, default=None)
    verification_code = models.CharField(max_length=50, verbose_name="код подтверждения", null=True, blank=True,
                                         default=None)

    class Meta:
        verbose_name = "Tg пользователь"
        verbose_name_plural = "Tg пользователи"
