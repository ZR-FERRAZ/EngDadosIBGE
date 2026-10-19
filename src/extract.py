import os

import truststore

truststore.inject_into_ssl()

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class Extract:
    URL_PNADC = (
        "https://servicodados.ibge.gov.br/api/v3/agregados/4093"
        "/periodos/201201-202601/variaveis/4099"
    )

    def extract_pnadc(self):
        """Extrai a taxa de desocupação (PE, por sexo) da API do IBGE."""
        params = {"localidades": "N3[26]", "classificacao": "2[all]"}
        resp = requests.get(self.URL_PNADC, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def extract_collection_from_mongo(self, db_name, collection_name):
        """Lê todos os documentos da camada bronze."""
        client = MongoClient(os.getenv("MONGO_URI"))
        try:
            # .find() é o que faltava no slide: sem ele você só tem a coleção
            return list(client[db_name][collection_name].find({}, {"_id": 0}))
        finally:
            client.close()