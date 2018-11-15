# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.files.storage import Storage

from django.utils.text import get_valid_filename

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging


class QcloudStorage(Storage):
    def __init__(self, option=None):
        if not option:
            self.option = settings.QCLOUD_STORAGE_OPTION

    def _open(self, name, mode='rb'):
        if name.startswith('http'):
            # 直接存的URL，直接返回，这类数据不支持取content
            return ''
        config = CosConfig(Region=self.option['region'], SecretId=self.option['SecretID'], SecretKey=self.option['SecretKey'], Token=self.option['token'], Scheme=self.option['Scheme'],Endpoint=self.option['Endpoint'])
        cos = CosS3Client(config)
        bucket = self.option['bucket'] + '-' + self.option['Appid']
        name = name.replace('\\', '/')
        response = cos.get_object(bucket, name)
        return response.content

    def _save(self, name, content):
        if name.startswith('http'):
            # 直接存的URL，直接返回，这类数据不支持取content
            return name
        
        name = name.replace('\\', '/')
        content = content.read()
        config = CosConfig(Region=self.option['region'], SecretId=self.option['SecretID'], SecretKey=self.option['SecretKey'], Token=self.option['token'], Scheme=self.option['Scheme'],Endpoint=self.option['Endpoint'])
        cos_object = CosS3Client(config)
        bucket = self.option['bucket'] + '-' + self.option['Appid']
        response = cos_object.put_object(bucket, content, name)
        return settings.COS_URL + '/' + name

    def exists(self, name):
        if name.startswith('http'):
            # 直接存的URL，直接返回，这类数据不支持取content
            return True
        config = CosConfig(Region=self.option['region'], SecretId=self.option['SecretID'], SecretKey=self.option['SecretKey'], Token=self.option['token'], Scheme=self.option['Scheme'],Endpoint=self.option['Endpoint'])
        cos = CosS3Client(config)
        bucket = self.option['bucket'] + '-' + self.option['Appid']
        name = name.replace('\\', '/')
        try:
            response = cos.head_object(bucket, name)
        except:
            return False
        else:
            return True
        
    def save(self, name, content, max_length=None):
        print 'aaa'
        """
        Saves new content to the file specified by name. The content should be
        a proper File object or any python file-like object, ready to be read
        from the beginning.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name

        if not hasattr(content, 'chunks'):
            content = File(content, name)
        if not self.exists(name):
             
            name = self.get_available_name(name, max_length=max_length)
            return self._save(name, content)        
        else:
            return self._save('xhxz.jpg', content)

    def url(self, name):
        if name.startswith('http'):
            # 直接存的URL，直接返回，这类数据不支持取content
            return name
        if getattr(settings, 'COS_URL', ''):
            url = "%s%s" % (
                settings.COS_URL,
                name,
            )
        else:
            if settings.COS_USE_CDN:
                cdn_host = 'file'
            else:
                cdn_host = 'cosgz'
            url = "http://%s-%s.%s.myqcloud.com%s" % (
                self.option['bucket'],
                self.option['Appid'],
                cdn_host,
                name,
            )

        return url

    def size(self, name):
        if name.startswith('http'):
            # 直接存的URL，直接返回，这类数据不支持取content
            return 0
        config = CosConfig(Region=self.option['region'], SecretId=self.option['SecretID'], SecretKey=self.option['SecretKey'], Token=self.option['token'], Scheme=self.option['Scheme'],Endpoint=self.option['Endpoint'])
        cos = CosS3Client(config)
        name = name.replace('\\', '/')
        bucket = self.option['bucket'] + '-' + self.option['Appid']
        response = cos.head_object(bucket, name)
        if response.status_code == 200:
            return response.headers['Content-Length']

    def delete(self, name):
        if name.startswith('http'):
            # 直接存的URL，直接返回，这类数据不支持取content
            return
        config = CosConfig(Region=self.option['region'], SecretId=self.option['SecretID'], SecretKey=self.option['SecretKey'], Token=self.option['token'], Scheme=self.option['Scheme'],Endpoint=self.option['Endpoint'])
        cos = CosS3Client(config)
        bucket = self.option['bucket'] + '-' + self.option['Appid']
        name = name.replace('\\', '/')
        cos.delete_object(name)
