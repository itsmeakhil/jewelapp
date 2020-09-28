from django.db import models


class BaseModel(models.Model):
    """
    model that will be inherited by all models to add common fields.
    """
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
