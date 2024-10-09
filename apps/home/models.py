from django.db import models
from django.db.models import Avg
from apps.accounts.models import Account
from apps.store.models import Product


# Create your models here.
class Reviews(models.Model):
    created_by = models.ForeignKey(
        Account, related_name="created_by", on_delete=models.CASCADE
    )
    reviewed_for = models.ForeignKey(
        Account, related_name="created_to", on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateField(auto_now=True)


class ProductReview(models.Model):
    created_by = models.ForeignKey(
        Account, related_name="product_created_by", on_delete=models.CASCADE
    )
    reviewed_for = models.ForeignKey(
        Product, related_name="product_created_to", on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    title=models.TextField()
    name=models.TextField()
    email=models.TextField()
    review = models.TextField()
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.name}"

    @classmethod
    def average_rating_for_product(cls, product_id):
        return cls.objects.filter(reviewed_for_id=product_id).aggregate(Avg('rating'))['rating__avg'] or 0
