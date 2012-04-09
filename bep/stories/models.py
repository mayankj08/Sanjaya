from django.db import models

class story(models.Model):
	title = models.CharField(max_length=100)
	date_submission = models.DateTimeField()
	user_submit = models.CharField(max_length=100)
	last_modify = models.DateTimeField()
	file_name = models.CharField(max_length=100)
	
class count(models.Model):
	title = models.CharField(max_length=100)
	counter = models.BigIntegerField()
	
class audio_story(models.Model):
    title = models.CharField(max_length=100)
    date_submission = models.DateTimeField()
    user_submit = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)

# Create your models here.\
