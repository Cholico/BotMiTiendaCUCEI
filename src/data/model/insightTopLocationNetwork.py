from pydantic import BaseModel
from google.cloud.bigquery.table import Row
from domain.model.insightTopLocationDomain import InsightTopLocationDomain
from shapely.wkt import loads

class InsightTopLocationNetwork(BaseModel):
    geohash: str
    geopoint: dict[str, float]
    order_count: int

    @staticmethod
    def from_bq_row(row: Row) -> 'InsightTopLocationNetwork':
        geopoint = loads(row['geopoint'])
        return InsightTopLocationNetwork(
            geohash = row['geohash'],
            geopoint = { 'latitude': geopoint.y, 'longitude': geopoint.x },
            order_count = row['order_count']
        )
    
    def to_domain(self) -> InsightTopLocationDomain:
        return InsightTopLocationDomain(
            geohash = self.geohash,
            geopoint = self.geopoint,
            order_count = self.order_count
        )