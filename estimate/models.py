from django.db import models
from django.utils.translation import gettext_lazy as _
from management.models import Equipment
from user.models import User
from utils.models import BaseModel


def estimate_number_generator(estimate_id):
    estimate = Estimate.objects.get(id=estimate_id)
    estimator_long_id = estimate.created_by.id
    estimate_date_created = str(estimate.created_at).replace('-', '')[2:8]
    return estimate_date_created + str(estimator_long_id) + str(estimate.id).zfill(3)


class Estimate(BaseModel):
    note = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Note"), )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   blank=False, related_name="estimates", verbose_name=_("Created By"), )
    is_archived = models.BooleanField(default=False, verbose_name=_("Is Archived"), )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Estimate")
        verbose_name_plural = _("Estimates")

    def __str__(self):
        return estimate_number_generator(self.id)


class EstimateEquipment(BaseModel):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE,
                                 blank=False, null=True, related_name="equipments", verbose_name=_("Estimate"), )
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,
                                  blank=False, related_name="estimates",
                                  verbose_name=_("Equipment"))  # TODO: find a better related_name
    quantity = models.FloatField(blank=False, verbose_name=_("Quantity"), )
    price_override = models.DecimalField(max_digits=8, decimal_places=2,
                                         blank=True, null=True, verbose_name=_("Price Override"), )

    class Meta:
        verbose_name = _("Estimate Equipment")

    def __str__(self):
        return estimate_number_generator(self.estimate.id) + " " + self.equipment.name
