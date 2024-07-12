from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Museum(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'museum'


class Relics(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    date = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    museum = models.ForeignKey(Museum, models.DO_NOTHING)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relics'


class MuseumUsers(models.Model):
    name = models.CharField(max_length=100)
    gender = models.IntegerField()
    birthday = models.DateField()
    status = models.IntegerField()
    position = models.IntegerField()
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'museum_users'


class VisitorPrediction(models.Model):
    date_type = models.IntegerField()
    weather_condition = models.IntegerField()
    temperature = models.FloatField()
    promotion = models.IntegerField()
    visitors = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'visitor_predictions'
