from django.db import models

# Create your models here.


class FileData(models.Model):
    name = models.CharField(max_length=255, default='NULL')
    file = models.FileField(upload_to='%Y/%m/%d', blank=True)
    tag = models.CharField(max_length=255, default='NULL')
    file_id = models.CharField(max_length=255, default='NULL')

    def __str__(self):
        return "{}-{}-{}".format(self.file, self.tag, self.file_id)