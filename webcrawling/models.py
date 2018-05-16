# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):  # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.choice_text

class Select(models.Model):

    field1 = models.CharField(max_length=200)
    field2 = models.CharField(max_length=200)
    field3 = models.CharField(max_length=200)
    field4 = models.CharField(max_length=200)
    field5 = models.CharField(max_length=200)
    field6 = models.CharField(max_length=200)
    field7 = models.CharField(max_length=200)
    field8 = models.CharField(max_length=200)
    field9 = models.CharField(max_length=200)
    field10 = models.CharField(max_length=200)
    field11 = models.CharField(max_length=200)
    field12 = models.CharField(max_length=200)
    field13 = models.CharField(max_length=200)
    field14 = models.CharField(max_length=200)
    field15 = models.CharField(max_length=200)
    field16 = models.CharField(max_length=200)
    field17 = models.CharField(max_length=200)


class Items(models.Model):

    field1 = models.CharField(max_length=200)
    field2 = models.CharField(max_length=200)
    field3 = models.CharField(max_length=200)
    field4 = models.CharField(max_length=200)
    field5 = models.CharField(max_length=200)
    field6 = models.CharField(max_length=200)
    field7 = models.CharField(max_length=200)
    field8 = models.CharField(max_length=200)
    field9 = models.CharField(max_length=200)
    field10 = models.CharField(max_length=200)
    field11 = models.CharField(max_length=200)
    field12 = models.CharField(max_length=200)
    field13 = models.CharField(max_length=200)
    field14 = models.CharField(max_length=200)
    field15 = models.CharField(max_length=200)
    field16 = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    count = models.CharField(max_length=200)