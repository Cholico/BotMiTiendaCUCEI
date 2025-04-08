from typing import Annotated
from fastapi.params import Depends
from firebase_admin import initialize_app, firestore
from google.cloud import bigquery
from core.config import Settings, get_settings

app = initialize_app()

db = firestore.client(app)

def provide_bigquery_client(settings: Annotated[Settings, Depends(get_settings)]) -> bigquery.Client:
    return bigquery.Client.from_service_account_json(settings.BIGQUERY_SERVICE_ACCOUNT_JSON)