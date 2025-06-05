from django.db import models
from django.utils import timezone

class Tag(models.Model):
    tag_name = models.CharField(max_length=30)
    date_added = models.DateTimeField("date_added")

class Termin(models.Model):
    termin_name = models.CharField(max_length=50)
    termin_description = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    tags = models.ManyToManyField(Tag)

# в файле с миграцией
# в отдельном файле текстом сохранить данные чтоб потом миграцию оттуда брать