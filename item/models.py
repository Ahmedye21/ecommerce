from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Item(models.Model):
    category    = models.ForeignKey(Category, related_name='items', null=True, on_delete=models.CASCADE) 
    name        = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price       = models.FloatField()
    image       = models.ImageField(upload_to='items', blank=True, null=True)
    is_sold     = models.BooleanField(default=False)
    created_by  = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.name} ({self.category})"
    
    
    def mark_as_sold(self):
        self.is_sold = True
        self.save()



class Purchase(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)