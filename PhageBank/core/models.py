from __future__ import unicode_literals
from django.db import models
from datetime import datetime,date

class PhageData(models.Model):
    phage_name = models.CharField(max_length=30, default='none')
    phage_host_name = models.CharField(max_length=30, default='none')
    phage_isolator_name = models.CharField(max_length=30, default='none')
    phage_experimenter_name = models.CharField(max_length=30, default='none')
    phage_CPT_id = models.CharField(max_length=100, default='none')
    phage_isolator_loc = models.CharField(max_length=5000, default='none')
    phage_submitted_user = models.CharField(max_length=5000, default='none')
    phage_submitted_date = models.DateTimeField(default=datetime.now, blank=True)
    phage_all_links = models.CharField(max_length=5000, default='none')
    phage_lab = models.CharField(max_length=30, default='A')

class PreData(models.Model):
    testkey = models.ForeignKey(PhageData, related_name='PhageName')
    phagename = models.CharField(max_length=30, default='none')

class ExperimentData(models.Model):
    expkey = models.ForeignKey(PhageData, related_name='PName')
    owner = models.CharField(max_length=100, default='none')
    timestamp = models.DateField(null=True)
    category = models.CharField(max_length=100, default='none')
    short_name = models.CharField(max_length=100, default='none')
    full_name = models.CharField(max_length=5000, default='none')
    methods = models.CharField(max_length=5000, default='none')
    results = models.CharField(max_length=5000, default='none')

class IsolationData(models.Model):
    isokey = models.ForeignKey(PhageData, related_name='iso_phageName')
    owner_name = models.CharField(max_length=100, default='none')
    location = models.CharField(max_length=100, default='none')
    TimeStamp = models.DateField(null=True)
    type1 = models.CharField(max_length=100, default='none')




