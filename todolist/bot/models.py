from django.db import models

from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.PositiveBigIntegerField()
    tg_user_id = models.PositiveBigIntegerField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, null=True)
    verification_code = models.CharField(max_length=50, verbose_name="код подтверждения")

    class Meta:
        verbose_name = "Tg пользователь"
        verbose_name_plural = "Tg пользователи"
