from django.db import models

# Create your models here.

class UserActionLog(models.Model):
    method = models.CharField(max_length=45)
    content = models.TextField()
    ctime = models.DateTimeField(blank=True, null=True)
    user_id = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    uri = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_action_log'