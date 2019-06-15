from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .utils import fastsearch
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Wikidata(models.Model):
    keyword = models.CharField(max_length=255)
    q = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s [%s]" % (self.keyword, self.q if self.q else '?')


class Wikipedia(models.Model):
    nome = models.CharField(max_length=255)
    wikidata = models.ForeignKey("Wikidata", on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.nome


class Label(models.Model):
    wikidata = models.ForeignKey("Wikidata", on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    lang = models.CharField(max_length=3, blank=True, null=True)
    fonte = models.CharField("Fonte della Label/Sameas", max_length=255, default="wd")

    def __str__(self):
        return self.nome

# TODO: Alias? Simile a label ma ricavato dai sameas
@receiver(pre_save, sender=Wikidata)
def fetch_wikidata(sender, instance, *args, **kwargs):
    """
    Get data about this keyword mfrom Wikidata
    """
    try:
        res = fastsearch.getsuggestion(instance.keyword)
        assert res
        # assign every Wikidata properties to each value of getsuggestion() dictionary (through SPARQL)
        for k in res.keys():
            setattr(instance, k, res[k])
    except AssertionError:
        pass


@receiver(post_save, sender=Wikidata)
def keyword_as_label(sender, instance, *args, **kwargs):
    # Save the keyword used on search as a Label
    try:
        la = Label(
            wikidata=instance,
            nome=instance.keyword,
            lang="",
            fonte="keyword_as_label"
        )
        la.save()
    except AssertionError:
        pass


@receiver(post_save, sender=Wikidata)
def fetch_label(sender, instance, *args, **kwargs):
    # Get the exact information for this Q from Qxxx.json file
    try:
        entity = fastsearch.getentity(instance.q)
        assert entity
        for label in entity['labels'].values():
            if label['language'] in settings.WIKIDATA_INTERLINK_LANGUAGES:
                vals = dict(
                        wikidata=instance,
                        nome=label['value'],
                        lang=label['language']
                )
                try:
                    # do not create duplicates
                    Label.objects.get(**vals)
                except ObjectDoesNotExist:
                    la = Label(**vals)
                    la.save()
    except AssertionError:
        pass
