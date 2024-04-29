from django.db import models
from datetime import datetime, timedelta

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    final_date = models.DateTimeField(default=datetime.now() + timedelta(days=1))
    status = models.CharField(max_length=20, default="To Do")
    executor = models.CharField(max_length=100)

    def __str__(self):
        return self.title
