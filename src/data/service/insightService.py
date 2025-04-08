import pytz
from datetime import datetime
from fastapi.params import Depends
from core.constants import BIGQUERY_DATASET_NAME
from core.constants import BIGQUERY_PROJECT_NAME
from core.constants import BIGQUERY_SP_GET_TOP_LOCATIONS_ON_MAP_NAME
from core.constants import BIGQUERY_SP_CALC_SALES_BY_DAY_OF_WEEK_NAME
from core.constants import BIGQUERY_SP_GET_TOP_SOLD_PRODUCTS_NAME
from google.cloud.bigquery import QueryJobConfig
from google.cloud.bigquery.query import ScalarQueryParameterType, ScalarQueryParameter
from google.api_core.exceptions import GoogleAPIError
from core.firebaseHelper import provide_bigquery_client
from data.model.insightTopLocationNetwork import InsightTopLocationNetwork
from data.model.insightCalculateSalesByDayOfWeekNetwork import InsightCalculateSalesByDayOfWeekNetwork
from data.model.insightTopSoldProductNetwork import InsightTopSoldProductNetwork

class InsightService:
    def __init__(self, bigquery_client = Depends(provide_bigquery_client)):
        self.bigquery_client = bigquery_client

    def get_top_locations_on_map(self, start_date: datetime, end_date: datetime) -> list[InsightTopLocationNetwork]:
        try:
            sp_query = f"CALL `{BIGQUERY_PROJECT_NAME}.{BIGQUERY_DATASET_NAME}.{BIGQUERY_SP_GET_TOP_LOCATIONS_ON_MAP_NAME}`(@start_date, @end_date)"
            job_config = QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("start_date", ScalarQueryParameterType("DATE"), start_date.astimezone(pytz.utc).date()),
                    ScalarQueryParameter("end_date", ScalarQueryParameterType("DATE"), end_date.astimezone(pytz.utc).date())
                ]
            )
            query_job = self.bigquery_client.query(sp_query, job_config=job_config)
            return [InsightTopLocationNetwork.from_bq_row(row) for row in query_job.result()]
        except GoogleAPIError as e:
            print(f"Error on insight service (get_top_locations_on_map): {e}")
            return []
        
    def calculate_sales_by_day_of_week(self, store_id: str, start_date: datetime, end_date: datetime) -> list[InsightCalculateSalesByDayOfWeekNetwork]:
        try:
            sp_query = f"CALL `{BIGQUERY_PROJECT_NAME}.{BIGQUERY_DATASET_NAME}.{BIGQUERY_SP_CALC_SALES_BY_DAY_OF_WEEK_NAME}`(@store_id, @start_date, @end_date)"
            job_config = QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("store_id", ScalarQueryParameterType("STRING"), store_id),
                    ScalarQueryParameter("start_date", ScalarQueryParameterType("DATE"), start_date.astimezone(pytz.utc).date()),
                    ScalarQueryParameter("end_date", ScalarQueryParameterType("DATE"), end_date.astimezone(pytz.utc).date())
                ]
            )
            query_job = self.bigquery_client.query(sp_query, job_config=job_config)
            return [InsightCalculateSalesByDayOfWeekNetwork.from_bq_row(row) for row in query_job.result()]
        except GoogleAPIError as e:
            print(f"Error on insight service (calculate_sales_by_day_of_week): {e}")
            return []
        
    def get_top_sold_products(self, start_date: datetime, end_date: datetime) -> list[InsightTopSoldProductNetwork]:
        try:
            sp_query = f"CALL `{BIGQUERY_PROJECT_NAME}.{BIGQUERY_DATASET_NAME}.{BIGQUERY_SP_GET_TOP_SOLD_PRODUCTS_NAME}`(@start_date, @end_date)"
            job_config = QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("start_date", ScalarQueryParameterType("DATE"), start_date.astimezone(pytz.utc).date()),
                    ScalarQueryParameter("end_date", ScalarQueryParameterType("DATE"), end_date.astimezone(pytz.utc).date())
                ]
            )
            query_job = self.bigquery_client.query(sp_query, job_config=job_config)
            return [InsightTopSoldProductNetwork.from_bq_row(row) for row in query_job.result()]
        except GoogleAPIError as e:
            print(f"Error on insight service (get_top_sold_products): {e}")
            return []