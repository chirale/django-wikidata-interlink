import requests

SPARQL_URL = """https://query.wikidata.org/sparql"""
SPARQL_QUERY = """PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX wd: <http://www.wikidata.org/entity/>

        SELECT ?item ?itemLabel ?type ?typeLabel ?num ?description ?altLabel  ?birthDate ?deathDate ?immagine ?itwikipedia  ?enwikipedia  WHERE {

            SERVICE wikibase:label { 
              bd:serviceParam wikibase:language "it,en,fr,de,nl". 
              ?item rdfs:label ?label .
              ?item skos:altLabel ?altLabel .    
              ?item schema:description ?description
            }

          SERVICE wikibase:mwapi {
            bd:serviceParam wikibase:api "EntitySearch" .
            bd:serviceParam wikibase:endpoint "www.wikidata.org" .
            bd:serviceParam mwapi:search "%s" .
            bd:serviceParam mwapi:language "en" .
            ?item wikibase:apiOutputItem mwapi:item .
            ?num wikibase:apiOrdinal true .
          }

           OPTIONAL {
          ?item wdt:P569 ?birthDate .
        }
        OPTIONAL {
          ?item wdt:P570 ?deathDate .
        }
        OPTIONAL {
         ?item wdt:P18 ?immagine .
        }
        OPTIONAL {
          ?itwikipedia schema:about ?item   .
          FILTER(CONTAINS(STR(?itwikipedia), 'it.wikipedia.org'))
          BIND(STR(?itwikipedia) as ?itwiki)
        }
        OPTIONAL {
          ?enwikipedia schema:about ?item   .
          FILTER(CONTAINS(STR(?enwikipedia), 'en.wikipedia.org'))
          BIND(STR(?enwikipedia) as ?enwiki)
        }


  ?item wdt:P31 ?type .


} ORDER BY ASC(?num) LIMIT 3
"""
ENTITY_DATA_URL = "https://www.wikidata.org/wiki/Special:EntityData/%s.json"


def getsuggestion(text):
    """ From text, get 3 matching results from Wikidata"""
    query = SPARQL_QUERY % text
    res = requests.get(
        """https://query.wikidata.org/sparql""",
        params=dict(
            query=query,
            # headers=SPARQL_HEADERS
            format="json"
        )
        # headers=SPARQL_HEADERS
    )
    try:
        assert res.status_code in [200, 304]
        risultato = res.json()
        assert risultato
        # logging.info("Result OK, saving JSON for %s (%s)", ne.text, ne.label)
        # ne.wikidata_json = risultato['results']['bindings']
        return dict(
            url=risultato['results']['bindings'][0]['item']['value'],
            img=risultato['results']['bindings'][0]['immagine']['value'],
            q=risultato['results']['bindings'][0]['item']['value'].split('/')[-1]
        )
        # ,
        #             wikipedia_url=risultato['results']['bindings'][0]['itwikipedia']['value']
        #            url=risultato['results']['bindings'][0]['enwikipedia']['value']
        """
        "item": "http://www.wikidata.org/entity/Q692",
        "type": "http://www.wikidata.org/entity/Q5",
        "num": "0",
        "description": "poeta inglese del XVI secolo",
        "altLabel": "Shakespeare",
        "birthDate": "1564-04-01T00:00:00Z",
        "deathDate": "1616-05-03T00:00:00Z",
        "immagine": "http://commons.wikimedia.org/wiki/Special:FilePath/Shakespeare.jpg",
        "itwikipedia": "https://it.wikipedia.org/wiki/William_Shakespeare",
        "enwikipedia": "https://en.wikipedia.org/wiki/William_Shakespeare"    
        """
    except:
        return None


def getentity(q):
    url = ENTITY_DATA_URL % q
    try:
        res = requests.get(url)
        assert res.status_code in [200, 304]
        risultato = res.json()['entities'][q]
        """
        for xdict in risultato['entities'][q].values():
            # language, value
            yield xdict
        """
        return risultato
    except:
        return None
