from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.PositiveBigIntegerField(unique=True)
    user_ud = models.CharField(max_length=255, null=True, blank=True, default=None)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, verbose_name="код подтверждения", null=True, blank=True,
                                         default=None)

    class Meta:
        verbose_name = "Tg пользователь"
        verbose_name_plural = "Tg пользователи"
