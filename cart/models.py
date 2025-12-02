from django.db import models
from listings.models import Meal
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)   # The product being added
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.meal.title} (Cart {self.cart.id})"

    @property
    def total_price(self):
        return self.quantity * self.meal.price
