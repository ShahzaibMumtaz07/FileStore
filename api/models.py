from django.db import models
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from cloudinary_storage.storage import RawMediaCloudinaryStorage



User = get_user_model()


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        # if instance.pk:
        #     filename = '{}_{}{}'.format(filename,instance.pk, ext)
        # else:
        filename = '{}_{}{}'.format(filename,uuid4().hex, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename('uploads')

class Topic(models.Model):
    name = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=1, default='A')
    created_on = models.DateTimeField(default=now)
    last_updated_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User,models.DO_NOTHING)
    short_description = models.TextField(max_length=512)
    long_description = models.TextField(max_length=2048)


    class Meta:
        
        db_table = 'topics'

    
class Folder(models.Model):
    name = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=1, default='A')
    created_on = models.DateTimeField(default=now)
    last_updated_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User,models.DO_NOTHING)
    topic = models.ManyToManyField(Topic)

    class Meta:
        
        db_table = 'folders'



class Document(models.Model):
    file = models.FileField(upload_to=path_and_rename, unique=True, storage=RawMediaCloudinaryStorage())
    status = models.CharField(max_length=1, default='A')
    created_on = models.DateTimeField(default=now)
    last_updated_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User,models.DO_NOTHING)
    folder = models.ManyToManyField(Folder)
    limit_access = models.BooleanField(default=False)

    class Meta:
        
        db_table = 'documents'