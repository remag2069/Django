from django.db import models
from django.utils import timezone

# Create your models here.

class student(models.Model):
    student_name=models.CharField(max_length=30)
    student_id=models.IntegerField()
    date_of_join=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return(self.student_name)
