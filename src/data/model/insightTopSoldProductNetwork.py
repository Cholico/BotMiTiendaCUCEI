from pydantic import BaseModel
from google.cloud.bigquery.table import Row
from datetime import datetime
from domain.model.insightTopSoldProductDomain import InsightTopSoldProductDomain

class InsightTopSoldProductNetwork(BaseModel):
    id: str
    name: str
    description: str
    image: str
    category_name: str
    store_name: str
    store_owner_id: str
    discount_percentage: float
    discount_start_date: dict
    discount_end_date: dict
    rating: float
    total_reviews: int
    total_quantity_sold: int
    hits_on_orders: int

    @staticmethod
    def from_bq_row(row: Row) -> 'InsightTopSoldProductNetwork':
        return InsightTopSoldProductNetwork(
            id = row['product_id'],
            name = row['product_name'],
            description = row['product_description'],
            image = row['product_image'],
            category_name = row['product_category_name'],
            store_name = row['product_store_name'],
            store_owner_id = row['product_store_owner_id'],
            discount_percentage = row['product_discount_percentage'],
            discount_start_date = row['product_discount_start_date'],
            discount_end_date = row['product_discount_end_date'],
            rating = row['product_rating'],
            total_reviews = row['product_total_reviews'],
            total_quantity_sold = row['total_quantity'],
            hits_on_orders = row['product_hits_on_orders']
        )
    
    def to_domain(self) -> InsightTopSoldProductDomain:
        return InsightTopSoldProductDomain(
            id = self.id,
            name = self.name,
            description = self.description,
            image = self.image,
            category_name = self.category_name,
            store_name = self.store_name,
            store_owner_id = self.store_owner_id,
            discount_percentage = self.discount_percentage,
            discount_start_date = datetime.fromtimestamp(self.discount_start_date['_seconds'] + self.discount_start_date['_nanoseconds'] * 1e-9),
            discount_end_date = datetime.fromtimestamp(self.discount_end_date['_seconds'] + self.discount_end_date['_nanoseconds'] * 1e-9),
            rating = self.rating,
            total_reviews = self.total_reviews,
            total_quantity_sold = self.total_quantity_sold,
            hits_on_orders = self.hits_on_orders
        )