=========================
Django Wikidata Interlink
=========================

Django Wikidata Interlink is a simple Django app to retrieve information about a keyword with the power of SPARQL and Wikidata and cache its result.

Requirements
------------

* .. _Requests: https://2.python-requests.org/en/master/

Install
-------

1. Add to requirements.txt this line::

    -e git+https://github.com/chirale/django-wikidata-interlink.git#egg=django-wikidata-interlink

2. ``pip install -r requirements.txt``

Quick start
-----------

1. Add "wikidata_interlink" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wikidata_interlink',
    ]

2. Add to settings the label languages (order is relevant), e.g.::

    WIKIDATA_INTERLINK_LANGUAGES = ['it', 'en']

3. Run ``python manage.py migrate`` to create the wikidata_interlink models.

4. Visit the admin page and add a new Wikidata element filling the Keyword field with something like "Earth" or a person name.

5. Q, url and img will be autofilled with data retrieved from wikidata. It will be saved one Label for every language specified in settings.WIKIDATA_INTERLINK_LANGUAGES.

Labels
------

Labels are soft links to a Wikidata item and can be used for search. There comes in two flavours:

1. wd: real wikidata labels
2. keyword_as_label: a soft label assigned to a Wikidata item since it was produced by the search itself.

Usage inside admin commands
---------------------------

Since signals are used, this app can be easily used inside an admin command like this (NamedEntity is an example model)::

    def handle(self, *args, **options):
        today = timezone.now()
        # group by avoid duplicates
        for uniquel in NamedEntity.objects.filter(label='PER').values('id', 'text').annotate(dcount=Count('text')):
            ents = NamedEntity.objects.filter(id=uniquel['id'])
            wikidata_q = None
            try:
                # Label with this name exists
                mylabel = Label.objects.filter(nome=uniquel['text']).first()
                wikidata_q = mylabel.wikidata.q
            except IndexError:
                # Label doesn't exists
                # *** add a new Wikidata item ***
                new_wikidata = Wikidata(
                    keyword=uniquel['text']
                )
                new_wikidata.save()
                wikidata_q = new_wikidata.q
            for ent in ents:
                # save the q on your model
                ent.wd_q = wikidata_q
                ent.save()

