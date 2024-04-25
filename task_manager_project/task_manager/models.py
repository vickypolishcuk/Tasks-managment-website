from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="To Do")

    def __str__(self):
        return self.title
