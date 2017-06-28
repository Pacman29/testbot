from django.db import models
from django.utils import timezone

TYPE_OF_TASK_CHOICES = (
    (u'C', u'Текущее'),
    (u'M', u'Модульное')
)

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    def __str__(self):
        return self.subject_name

class Task(models.Model):
    subject_name = models.ForeignKey(Subject)
    type = models.CharField(max_length=2,choices=TYPE_OF_TASK_CHOICES)
    task = models.TextField(max_length=1000)
    last_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.subject_name.__str__()+" "+self.type.__str__()+" "+self.task