from django.db import models

from django.db import models

class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

