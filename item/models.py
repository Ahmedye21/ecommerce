from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Profile of {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='items', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.name} ({self.category})"

    def mark_as_sold(self):
        self.is_sold = True
        self.save()

class Purchase(models.Model):
    buyer = models.ForeignKey(User, related_name='purchases_as_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='purchases_as_seller', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='purchases', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Purchase of {self.item.name} by {self.buyer.username}"

    def process_transaction(self):
        buyer_profile = self.buyer.profile
        seller_profile = self.seller.profile

        if buyer_profile.balance >= self.amount:
            buyer_profile.balance -= self.amount
            buyer_profile.save()

            seller_profile.balance += self.amount
            seller_profile.save()

            self.item.is_sold = True
            self.item.save()

            return True
        else:
            return False
