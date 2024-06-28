import time
from elasticsearch import Elasticsearch
import subprocess

# Configurarea conexiunii către Elasticsearch
try:
    es = Elasticsearch(['http://localhost:9200'], timeout=30)
except Exception as e:
    print(f"Eroare la conectarea la Elasticsearch: {e}")
    exit(1)

# Suprimarea avertismentelor Elasticsearch
import logging
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

# Funcție pentru căutarea activității malitioase și trimiterea alertei
def search_and_alert():
    # Definirea căutării în Elasticsearch pentru activitate malitioasă
    query_body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"message": "DELETE"}},
                    {"match": {"message": "File: DELETE"}}
                ],
                "filter": {
                    "range": {
                        "@timestamp": {
                            "gte": "now-1m"  # Caută activitate în ultimul minut
                        }
                    }
                }
            }
        }
    }

    # Realizarea căutării în Elasticsearch
    try:
        results = es.search(index="user_commands-*", body=query_body)
    except Exception as e:
        print(f"Eroare la căutarea în Elasticsearch: {e}")
        return

    # Verificarea dacă s-au găsit rezultate
    if results['hits']['total']['value'] > 0:
        # Dacă există activitate malitioasă, trimite alerta prin email
        send_email_alert()

# Funcție pentru trimiterea alertei prin email
def send_email_alert():
    # Configurarea parametrilor pentru email
    recipient_email = "dragoscojocaru6@gmail.com"
    subject = "Alertă: Activitate malitioasă detectată în fișierele de log"
    body = "S-a detectat o activitate malitioasă în fișierele de log."

    # Trimiterea email-ului folosind mailutils
    subprocess.run(['echo', f'{body} | mail -s "{subject}" {recipient_email}'], shell=True)

# Buclă principală pentru monitorizarea continuă
while True:
    # Verificarea activității malitioase la fiecare 1 minut
    search_and_alert()
    # Așteptarea pentru următoarea verificare
    time.sleep(60)

