from asyncore import write
from email.policy import default
import imp
from os import read
from django.forms import ValidationError
from rest_framework import serializers
from .models import Topic, Folder, Document
from django.utils.timezone import now


class TopicSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only = True)
    status = serializers.CharField(write_only = True, default='A')

    class Meta:
        model = Topic
        fields = ['id','name', 'short_description','long_description','status']

    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.last_updated_on=now()
        instance.save()
        return instance

    # def validate(self, data):
    #     if data.get('name',None) and not len(data.get('name').strip()) > 0:
    #         raise serializers.ValidationError('name cannot be empty/blank')
    #     if data.get('short_description',None) and not len(data.get('short_description').strip()) > 0:
    #         raise serializers.ValidationError('short_description cannot be empty/blank')
    #     if data.get('long_description',None) and not len(data.get('long_description').strip()) > 0:
    #         raise serializers.ValidationError('long_description cannot be empty/blank')
    #     return data



class FolderSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only = True)
    topic = serializers.PrimaryKeyRelatedField(read_only = False, many = True, queryset=Topic.objects.all())
    status = serializers.CharField(write_only = True, default='A')
    class Meta:
        model = Folder
        fields = ['id','name','topic','status']

    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.last_updated_on=now()
        instance.save()
        return instance



class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only = True)
    status = serializers.CharField(write_only = True, default='A')
    folder = serializers.PrimaryKeyRelatedField(read_only = False, many = True, queryset=Folder.objects.all())
    limit_access = serializers.BooleanField(write_only=True,default = False)
    # file_url = serializers.URLField(read_only = True,source = 'file.url')
    
    class Meta:
        model = Document
        fields = ['id','file','folder', 'status','limit_access']

    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.limit_access = validated_data.get('limit_access', instance.limit_access)
        instance.last_updated_on=now()
        instance.save()
        return instance


class GetDocumentSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField(required = False)
    folder_id = serializers.IntegerField(required = False)
    topic_name = serializers.CharField(max_length = 64, required = False)
    folder_name = serializers.CharField(max_length = 64, required = False)


    def validate(self, attrs):
        if attrs.get('topic_id',None) and not Topic.objects.filter(id = attrs.get('topic_id')).exists():
            raise serializers.ValidationError('No resource found')
        if attrs.get('folder_id',None) and not Folder.objects.filter(id = attrs.get('folder_id')).exists():
            raise serializers.ValidationError('No resource found')
        if attrs.get('topic_name',None) and not Topic.objects.filter(name = attrs.get('topic_name')).exists():
            raise serializers.ValidationError('No resource found')
        if attrs.get('folder_name',None) and not Folder.objects.filter(name = attrs.get('folder_name')).exists():
            raise serializers.ValidationError('No resource found')
        return super().validate(attrs)


