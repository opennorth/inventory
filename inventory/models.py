from django.db import models
from djorm_pgarray.fields import ArrayField
from jsonfield import JSONField
from uuidfield import UUIDField


class Dataset(models.Model):  # dcat:Dataset
    country_code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)  # @see https://github.com/ckan/ckan/blob/master/ckan/model/package.py#L27

    json = JSONField(default={})
    custom_properties = ArrayField(dbtype='text')
    source_url = models.URLField(unique=True)
    extras_keys = ArrayField(dbtype='text')

    # @see http://www.w3.org/TR/vocab-dcat/
    title = models.TextField(default='')  # dct
    description = models.TextField(default='')  # dct
    issued = models.DateTimeField(null=True)  # dct
    modified = models.DateTimeField(null=True)  # dct
    publisher = models.TextField(default='')  # dct
    identifier = models.TextField(default='')  # dct (not always a UUID)
    keyword = JSONField(default={})  # dcat
    maintainer = models.TextField(default='')
    maintainer_email = models.EmailField(default='')
    author = models.TextField(default='')
    author_email = models.EmailField(default='')
    landingPage = models.URLField(default='', max_length=500)  # dcat (length 401 observed)

    # License properties
    isopen = models.NullBooleanField()
    license_id = models.TextField(default='')
    license_url = models.URLField(default='')
    license_title = models.TextField(default='')

    class Meta:
        unique_together = (('country_code', 'name'),)


class Distribution(models.Model):  # dcat:Distribution
    dataset = models.ForeignKey('Dataset')
    _id = models.TextField(default='')  # (not always a UUID)

    json = JSONField(default={})
    custom_properties = ArrayField(dbtype='text')

    # @see http://www.w3.org/TR/vocab-dcat/
    name = models.TextField(default='')  # dct
    description = models.TextField(default='')  # dct
    created = models.DateTimeField(null=True)  # dct
    last_modified = models.DateTimeField(null=True)  # dct
    url = models.URLField(default='', max_length=2000)  # dcat (length 1692 observed)
    size = models.BigIntegerField(null=True)  # dcat
    mimetype = models.TextField(default='')  # dcat
    format = models.TextField(default='')  # dct

    class Meta:
        unique_together = (('dataset', '_id'),)
