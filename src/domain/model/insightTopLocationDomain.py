from pydantic import BaseModel

class InsightTopLocationDomain(BaseModel):
    geohash: str
    geopoint: dict[str, float]
    order_count: int