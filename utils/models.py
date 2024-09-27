from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SoftDeleteManager(models.Manager):
    """Manager that retrieves only non-deleted objects."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class DeletedManager(models.Manager):
    """Manager that retrieves only soft-deleted objects."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Deleted at'))

    class Meta:
        abstract = True

    objects = SoftDeleteManager()  # Manager for non-deleted objects
    all_objects = models.Manager()  # Manager for all objects (deleted and non-deleted)
    deleted_objects = DeletedManager()  # Manager for only soft-deleted objects

    def delete(self, using=None, keep_parents=False):
        """Soft delete the object by setting the deleted_at field."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete the object."""
        super().delete(using=using, keep_parents=keep_parents)
