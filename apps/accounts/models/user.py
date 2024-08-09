import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,  related_name="users")
