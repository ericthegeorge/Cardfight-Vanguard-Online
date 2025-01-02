from django.db import models

# Create your models here.

class Card(models.Model):
    name = models.CharField(max_length = 100)
    rarity = models.CharField(max_length=10, choices = [
        ('C', 'Common'),
        ('R', 'Rare'),
        ('RR', 'Double Rare'),
        ('RRR', 'Triple Rare'),
        ('SP', 'Special')
    ])
    set_code = models.CharField(max_length = 10)
    
    def __str__(self):
        return self.name
