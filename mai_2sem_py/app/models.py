from django.db import models


class UploadFiles(models.Model):
    file = models.FileField(upload_to="")
    father_user = models.IntegerField()
    authorized_users = models.JSONField()

    def delete_file(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path

        super(UploadFiles, self).delete(*args, **kwargs)

        storage.delete(path)