from django.db import models


class UploadFiles(models.Model):
    file = models.FileField(upload_to="uploads_model")
    father_user = models.IntegerField()
    authorized_users = models.JSONField()