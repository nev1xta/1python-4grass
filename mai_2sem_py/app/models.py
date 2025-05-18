from django.db import models


class UploadFiles(models.Model):
    file = models.FileField(upload_to="")
    father_user = models.IntegerField()
    authorized_users = models.JSONField()