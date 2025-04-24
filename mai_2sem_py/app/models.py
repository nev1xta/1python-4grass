from django.db import models


class Files(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    mass = models.IntegerField()
    id_user = models.IntegerField()

    def __str__(self):
        return self.name
    
class UploadFiles(models.Model):
    file = models.FileField(upload_to="uploads_model")
    father_user = models.IntegerField()
    authorized_users = models.JSONField()