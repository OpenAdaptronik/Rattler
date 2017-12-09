from django.db import models
from django.conf import settings


class Projects(models.Model):
    userID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    typ = models.CharField(max_length=100)
    note = models.TextField(max_length=500)

# hier müssen wir uns noch überlegen, wie wir die verschiedenen Felder wie category und subcategory miteinander
# verknüpfen wollen, zur Auswahl stehen im Moment zwei Möglichkeiten, wer das bearbeitet bitte bei Alex oder Maren fragen welche :)
