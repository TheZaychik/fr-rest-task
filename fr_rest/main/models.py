from django.db import models
from jsonfield import JSONField


class Poll(models.Model):
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.id


class Question(models.Model):
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE)
    type = models.CharField(max_length=15)
    question = models.TextField()
    answers = JSONField()  # []

    def __str__(self):
        return self.id


class CUser(models.Model):
    user_id = models.IntegerField(unique=True)
    competed_polls = JSONField()  # { poll_id : { question: [answers] } }

    def __str__(self):
        return self.id
