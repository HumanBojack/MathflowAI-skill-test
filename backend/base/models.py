from django.db import models
from django.core.exceptions import ValidationError


class User(models.Model):
    username = models.CharField(max_length=50)
    money = models.IntegerField(default=0)


class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.BooleanField()
    money_value = models.IntegerField(default=10)

    def __str__(self):
        return self.question


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.answer)

    class Meta:
        unique_together = (("user", "question"),)

    def clean(self):
        if (
            self.pk is None
            and self.user.answers.filter(question=self.question).exists()
        ):
            raise ValidationError("User has already answered this question")
