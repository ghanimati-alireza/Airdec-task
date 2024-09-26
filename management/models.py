from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel


class Equipment(BaseModel):
    name = models.CharField(max_length=255, blank=False, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Price'))
    is_active = models.BooleanField(default=True, help_text="Whether its active or not", verbose_name=_('Is Active'))

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
