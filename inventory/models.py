from django.db import models
from products.models import Product

class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('ml', 'Millilitre'),
        ('g', 'Gram'),
        ('pcs', 'Pieces'),
    )

    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"
    



class Recipe(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity_used = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        unique_together = ('product', 'ingredient')

    def __str__(self):
        return f"{self.product.name} → {self.ingredient.name}"